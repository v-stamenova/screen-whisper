import sys
import subprocess

def main():
    try:
        version = subprocess.check_output(["tesseract", "--version"]).decode("utf-8").splitlines()[0]
        print(f"Tesseract version: {version}")
    except Exception as e:
        print("❌ Failed to check Tesseract version:", e)   
    print(f"Python version: {sys.version}")

if __name__ == "__main__":
    main()
