from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from PIL import Image
from dotenv import load_dotenv
import pytesseract
import io
import base64
import httpx
import os
import json

load_dotenv()
LIBRETRANSLATE_URL = os.getenv("LIBRETRANSLATE_URL")

app = FastAPI()

class OCRRequest(BaseModel):
    image: str #base64

class TranslationResponse(BaseModel):
    originalText: str
    translatedText: str

@app.post("/ocr-tr")
async def ocr(request: OCRRequest):
    try:
        img_bytes = base64.b64decode(request.image)
        image = Image.open(io.BytesIO(img_bytes))
        ocr_text = pytesseract.image_to_string(image, lang="nld")

        if not ocr_text:
            return {"text": ""}

        async with httpx.AsyncClient() as client:
            payload = {
                "q": str(ocr_text).strip(),
                "source": "nl",
                "target": "en",
                "format": "text"
            }
            headers = {"Content-Type": "application/json"}

            resp = await client.post(LIBRETRANSLATE_URL,     data=json.dumps(payload), headers=headers)
            resp.raise_for_status()
            translated = resp.json()

        return {"originalText": ocr_text, "translatedText": translated.get("translatedText", "")}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
