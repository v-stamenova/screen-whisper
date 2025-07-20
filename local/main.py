import mss
import pyautogui
from PIL import Image
from dotenv import load_dotenv
import os
import io
import base64
import requests

load_dotenv()
OCR_TR_URL = os.getenv("OCR_TR_URL")

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
        print("OCR Text:", data.get("text", "<no text>"))
    else:
        print("Error:", response.status_code, response.text)

if __name__ == "__main__":
    image = capture_mouse_area()
    send_to_ocr(image)