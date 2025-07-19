import sys
import subprocess
import pytesseract
import pyautogui
from PIL import Image
import time

REGION_WIDTH = 200
REGION_HEIGHT = 100

def system_check():
    try:
        version = subprocess.check_output(["tesseract", "--version"]).decode("utf-8").splitlines()[0]
        print(f"Tesseract version: {version}")
    except Exception as e:
        print("❌ Failed to check Tesseract version:", e)   
    print(f"Python version: {sys.version}")

def main():
    system_check()

    result = run_ocr_on_capture()
    print("📝 OCR Result (Dutch):")
    print(result)

def capture_mouse_region():
    x, y = pyautogui.position()
    left = x - REGION_WIDTH // 2
    top = y - REGION_HEIGHT // 2

    print(f"📸 Capturing region at ({left}, {top}, {REGION_WIDTH}, {REGION_HEIGHT})...")
    screenshot = pyautogui.screenshot(region=(left, top, REGION_WIDTH, REGION_HEIGHT))
    return screenshot

def run_ocr_on_capture():
    img = capture_mouse_region()
    text = pytesseract.image_to_string(img, lang='nld')
    return text.strip()


if __name__ == "__main__":
    main()
