import mss
import pyautogui
from PIL import Image

def capture_mouse_area():
    x, y = pyautogui.position()
    width = 300
    height = 150

    region = {
        "left": x - int(width / 2),
        "top": y - int(height / 2),
        "width": width,
        "height": height
    }

    print(f"Capturing at ({region['left']}, {region['top']})...")
    with mss.mss() as sct:
        img = sct.grab(region)
        img_pil = Image.frombytes("RGB", img.size, img.rgb)
        img_pil.save("capture.png")
        print("Saved as capture.png")

if __name__ == "__main__":
    capture_mouse_area()
