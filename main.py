from fastapi import FastAPI, UploadFile, File, HTTPException
from PIL import Image, UnidentifiedImageError
from io import BytesIO

from app.services.ocr import extract_text


app = FastAPI(
    title="Receipt Analyzer",
    description="LLM-Powered Receipt Extraction and Calculation System"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to Receipt Analyzer!",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.post("/ocr")
async def read_receipt(file: UploadFile = File(...)):

    # อ่านข้อมูลไฟล์ที่ผู้ใช้อัปโหลด
    contents = await file.read()

    try:
        # เปิดข้อมูลภาพ
        image = Image.open(BytesIO(contents))

        # เรียกใช้ระบบ OCR
        text = extract_text(image)

        # ส่งข้อความกลับไป
        return {
            "filename": file.filename,
            "extracted_text": text
        }

    except UnidentifiedImageError:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is not a valid image."
        )