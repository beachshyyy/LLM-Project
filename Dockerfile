FROM python:3.13-slim

WORKDIR /app

# ติดตั้ง Tesseract OCR และชุดภาษาไทย/อังกฤษ
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    tesseract-ocr-tha \
    tesseract-ocr-eng \
    && rm -rf /var/lib/apt/lists/*

# ติดตั้ง Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# คัดลอกไฟล์โปรเจกต์
COPY . .

# เปิดใช้งาน FastAPI
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-10000}"]
