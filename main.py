from fastapi import FastAPI, UploadFile, File, HTTPException
from PIL import Image, UnidentifiedImageError
from io import BytesIO

from app.services.ocr import extract_text
from app.services.extraction import extract_receipt
from app.services.agent import run_agent
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Receipt Analyzer",
    description="LLM-Powered Receipt Extraction and Calculation System"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

@app.post("/analyze")
async def analyze_receipt(file: UploadFile = File(...)):

    # อ่านไฟล์ภาพที่ upload
    contents = await file.read()

    try:
        # เปิดภาพใบเสร็จ
        image = Image.open(BytesIO(contents))

        # อ่านข้อความด้วย OCR
        ocr_text = extract_text(image)

        # แยกข้อมูลใบเสร็จด้วย LLM
        receipt, sources = extract_receipt(
            ocr_text,
            return_sources=True
        )

        # วิเคราะห์ข้อมูลด้วย Agent
        agent_result = run_agent(receipt)
        analysis = agent_result["message"]
        calculation = agent_result["calculation"]

        # ส่งผลลัพธ์กลับไป
        return {
            "filename": file.filename,
            "ocr_text": ocr_text,
            "receipt": receipt.model_dump(),
            "analysis": analysis,
            "calculation": calculation,
            "sources": sources
        }

    except UnidentifiedImageError:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is not a valid image."
        )

    except Exception as e:
        print(f"Error analyzing receipt: {e}")
        raise HTTPException(
            status_code=500,
            detail="An error occurred while analyzing the receipt. Please try again."
        )