# ScreenText Translator

A small pipeline that captures screen regions (like UI text in games such as The Sims), performs OCR via Tesseract, and translates the recognized text using LibreTranslate.

Inspired by the fact that I accidentally installed Sims in Dutch and did not want to reinstall it.

---

## Architecture Overview

Unfortunately I couldn't make the entire app in a fully containerized network. This was because when I would run the screen capturing on the WSL, it didn't work (probably Docker just doesn't have access to the screen framebuffer).

Because of that the architecture is split in two parts.

### Local

Within the local folder you can find a `main.py` which takes the screenshot. The dependencies that are used are `mss`, `pyautogui`, `Pillow`, `dotenv`, `requests`, `keyboard`, `colorama`. The Python version used in locally was 3.13.0.

After you run the script in a terminal you can take a screenshot using the Ctrl + Shift + T shortcut. You will see the translation in there as well

```
Running... Press Ctrl+Shift+T to capture screen region.
Hotkey pressed: Capturing and sending image...
Capturing at (1706, 752)...

==================================================
📝 OCR Text:

Hallo wereld!
--------------------------------------------------
🌍 Translated Text:

Hello, world!
==================================================
```

### Docker containers

In the remote directory you can find the two containers that are used. One of the containers is using Tesseract to detect text while the other one is a LibreTranslate container. Once the local app sends the image (base64) to the Tesseract container, it detects the text and forwards it to the LibreTranslate container to be translated. After that the LibreTranslate responds to the Tesseract container and then finally the Tesseract returns it to the local app.

---

## Requirements

### Host (Windows)
- Anaconda (or any Python 3.12 environment)
- The following packages: `mss`, `pyautogui`, `Pillow`, `dotenv`, `requests`, `keyboard`, `colorama`
- Docker + Docker Compose

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/translator.git
cd translator
```

---

### 2. Run Docker Services

Build and run OCR API and LibreTranslate:

```bash
docker compose up
```

### 3. Configure & Run Local Client (Windows)

> The client runs locally on Windows to capture your screen.

#### Install dependencies

```bash
pip install mss pyautogui pillow requests dotenv requests keyboard colorama
```

#### Run the capture client

```bash
cd local
python main.py
```

---


## Tips & Troubleshooting

- If LibreTranslate gives `"nl is not supported"`: make sure `LT_LOAD_ONLY` includes `nl`.
- Use `localhost:5000` for OCR server and `localhost:5010` for LibreTranslate in development.
- Test OCR output with simple screenshots before using complex UI.
