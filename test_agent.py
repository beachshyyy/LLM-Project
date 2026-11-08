
from PIL import Image

from app.services.ocr import extract_text
from app.services.extraction import extract_receipt
from app.services.agent import run_agent


# เปิดรูปใบเสร็จ
image = Image.open("samples/receipt_sample.jpg")


# อ่านข้อความด้วย OCR
ocr_text = extract_text(image)


# แยกข้อมูลด้วย LLM
receipt = extract_receipt(ocr_text)

print("\n===== RECEIPT DATA =====")
print(receipt.model_dump_json(indent=2))
# ส่งข้อมูลให้ Agent วิเคราะห์
result = run_agent(receipt)


# แสดงคำตอบจาก Agent
print("\n===== AGENT RESULT =====")
print(result)
