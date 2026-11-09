# Receipt Analyzer

ระบบวิเคราะห์ข้อมูลใบเสร็จรับเงินด้วยปัญญาประดิษฐ์ (AI) โดยผู้ใช้สามารถอัปโหลดรูปภาพใบเสร็จเพื่อให้ระบบอ่านข้อความ แยกข้อมูลรายการสินค้า และตรวจสอบความถูกต้องของยอดเงินได้โดยอัตโนมัติ

## ความสามารถของระบบ - What it does?

- **OCR:** อ่านข้อความจากภาพใบเสร็จภาษาไทยและภาษาอังกฤษด้วย Tesseract OCR
- **Structured Data Extraction:** ใช้ LLM แยกข้อมูลใบเสร็จ เช่น ชื่อร้านค้า รายการสินค้า จำนวน ราคา และยอดรวม
- **Schema Validation:** ตรวจสอบรูปแบบและความถูกต้องของข้อมูลด้วย Pydantic
- **RAG:** ค้นหาความรู้เกี่ยวกับใบเสร็จจากฐานข้อมูลความรู้ เพื่อนำมาเป็นบริบทประกอบการสกัดข้อมูล
- **Agentic Tool Calling:** ใช้ AI Agent เรียกเครื่องมือคำนวณเพื่อตรวจสอบยอดเงินและความสอดคล้องของข้อมูล

## เทคโนโลยีที่ใช้

- Python & FastAPI
- Tesseract OCR & Pillow
- OpenAI Python SDK & Gemma 4 E4B IT
- bge-m3 สำหรับสร้าง Embeddings
- Pydantic สำหรับตรวจสอบข้อมูล
- HTML, CSS, JavaScript สำหรับ Frontend

## วิธีติดตั้งและตั้งค่า

**1. Clone Repository**

```bash
git clone https://github.com/beachshyyy/LLM-Project.git
cd LLM-Project
```

**2. สร้าง Virtual Environment และติดตั้ง Dependencies**

```bash
python -m venv .venv
```

เปิดใช้งานบน Windows:

```bash
.venv\Scripts\activate
```

ติดตั้ง Packages:

```bash
pip install fastapi "uvicorn[standard]" pytesseract Pillow python-multipart openai python-dotenv openpyxl
```

**3. ตั้งค่า Environment Variables**

สร้างไฟล์ `.env` ในโฟลเดอร์หลักของโปรเจกต์ โดยอ้างอิงจาก `.env.example`

```env
OPENAI_API_KEY=your_api_key
OPENAI_BASE_URL=your_class_proxy_url
```

หมายเหตุ: ต้องติดตั้ง Tesseract OCR และมีภาษาไทย (`tha`) และภาษาอังกฤษ (`eng`) ด้วย

## วิธีใช้งาน - How to run it

**1. เปิด Backend และ Frontend**

รันคำสั่งต่อไปนี้จากโฟลเดอร์หลักของโปรเจกต์

```bash
uvicorn main:app --reload
```

**2. เปิดหน้าเว็บไซต์**

เปิดเบราว์เซอร์และเข้าไปที่

```text
http://127.0.0.1:8000
```

**3. วิเคราะห์ใบเสร็จ**

อัปโหลดรูปภาพใบเสร็จผ่านหน้าเว็บไซต์ ระบบจะอ่านข้อความ สกัดข้อมูล และแสดงผลการวิเคราะห์โดยอัตโนมัติ

## การประเมินผล (Evaluation)

ใช้ชุดข้อมูลใบเสร็จจำนวน 30 ภาพ พร้อมข้อมูลยอดรวมที่ถูกต้อง (Ground Truth) เพื่อเปรียบเทียบความแม่นยำในการสกัดยอดรวมระหว่างระบบที่ไม่มี Retrieval และระบบที่ใช้ RAG

**Metric:** Total Exact Match Accuracy

| วิธีการ | ความแม่นยำ |
|---|---:|
| Baseline (ไม่ใช้ Retrieval) | 63.33% |
| RAG (Top-K = 1) | 63.33% |
| RAG (Top-K = 2) | 70.00% |

ผลการทดลองพบว่า RAG ที่ใช้ Top-K = 2 มีความแม่นยำสูงกว่า Baseline อยู่ 6.67 จุดเปอร์เซ็นต์

**วิธีรัน Evaluation**

สร้าง Retrieval Index:

```bash
python evaluation/build_index.py
```

รันการประเมินผล:

```bash
python evaluation/evaluate.py
```

