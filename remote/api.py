from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from PIL import Image
import pytesseract
import io
import base64

app = FastAPI()

class OCRRequest(BaseModel):
    image: str 

@app.post("/ocr-tr")
async def ocr(request: OCRRequest):
    try:
        img_bytes = base64.b64decode(request.image)
        image = Image.open(io.BytesIO(img_bytes))
        text = pytesseract.image_to_string(image, lang="nld")
        return {"text": text.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
