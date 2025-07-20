import mss
import pyautogui
from PIL import Image
from dotenv import load_dotenv
import os
import io
import base64
import requests
import keyboard
import time
from colorama import init, Fore, Style
import random

load_dotenv()
OCR_TR_URL = os.getenv("OCR_TR_URL")

COLORS = [
    Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE,
    Fore.MAGENTA, Fore.CYAN, Fore.LIGHTRED_EX,
    Fore.LIGHTGREEN_EX, Fore.LIGHTBLUE_EX, Fore.LIGHTMAGENTA_EX
]


def capture_mouse_area():
    x, y = pyautogui.position()
    width = 500
    height = 300

    region = {
        "left": x - int(width / 2),
        "top": y - int(height / 2),
        "width": width,
        "height": height
    }

    print(f"Capturing at ({region['left']}, {region['top']})...")
    with mss.mss() as sct:
        img = sct.grab(region)
        return Image.frombytes("RGB", img.size, img.rgb)

def send_to_ocr(image):
    buf = io.BytesIO()
    image.save(buf, format='PNG')
    base64_str = base64.b64encode(buf.getvalue()).decode()

    response = requests.post(
        OCR_TR_URL,
        json={"image": base64_str}
    )

    if response.ok:
        data = response.json()
        border_color = random.choice(COLORS)

        print("\n" + border_color + "=" * 50)
        print("📝 OCR Text:\n")
        print(data.get("originalText", "<no text>"))

        print(border_color + "-" * 50)
        print("🌍 Translated Text:\n")
        print(data.get("translatedText", "<no text>"))
        print(border_color + "=" * 50 + "\n")

        print(Style.RESET_ALL)
    else:
        print("Error:", response.status_code, response.text)

def handle_ocr_trigger():
    print("Hotkey pressed: Capturing and sending image...")
    image = capture_mouse_area()
    send_to_ocr(image)

if __name__ == "__main__":
    print("Running... Press Ctrl+Shift+T to capture screen region.")

    keyboard.add_hotkey('ctrl+shift+t', handle_ocr_trigger)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting...")