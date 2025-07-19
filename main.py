import sys
import subprocess
import pytesseract
import pyautogui
from PIL import Image
import time
import mss

REGION_WIDTH = 200
REGION_HEIGHT = 100

def system_check():
    try:
        version = subprocess.check_output(["tesseract", "--version"]).decode("utf-8").splitlines()[0]
        print(f"Tesseract version: {version}")
    except Exception as e:
        print("Failed to check Tesseract version:", e)   
    print(f"Python version: {sys.version}")

def main():
    system_check()

    capture_fullscreen()

    result = run_ocr_on_capture()
    print("OCR Result (Dutch):")
    print(result)

def capture_mouse_region():
    x, y = pyautogui.position()
    left = x - REGION_WIDTH // 2
    top = y - REGION_HEIGHT // 2

    region = {
        "top": top,
        "left": left,
        "width": REGION_WIDTH,
        "height": REGION_HEIGHT
    }

    print(f"Capturing region at ({left}, {top}, {REGION_WIDTH}, {REGION_HEIGHT})...")

    with mss.mss() as sct:
        img = sct.grab(region)
        img_pil = Image.frombytes("RGB", img.size, img.rgb)
        img_pil.save("debug_capture.png") 
        return img_pil

def run_ocr_on_capture():
    img = capture_mouse_region()
    text = pytesseract.image_to_string(img, lang='nld')
    return text.strip()

def capture_fullscreen():
    print("Capturing full screen...")
    with mss.mss() as sct:
        monitor = sct.monitors[0] 
        img = sct.grab(monitor)
        img_pil = Image.frombytes("RGB", img.size, img.rgb)
        img_pil.save("debug_fullscreen.png")
        print("Saved full screen to debug_fullscreen.png")

if __name__ == "__main__":
    main()
