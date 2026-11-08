from PIL import Image

from app.services.ocr import extract_text
from app.services.extraction import extract_receipt
from app.services.calculation import calculate_receipt


# เปิดรูปใบเสร็จ
image = Image.open("samples/receipt_sample.jpg")


# อ่านข้อความด้วย OCR
ocr_text = extract_text(image)

print("===== OCR TEXT =====")
print(ocr_text)


# ส่งข้อความ OCR ให้ LLM วิเคราะห์
receipt = extract_receipt(ocr_text)


# แสดงข้อมูลใบเสร็จ
print("\n===== EXTRACTED RECEIPT =====")
print(receipt.model_dump_json(indent=2))


print("\n===== DEBUG RECEIPT VALUES =====")
print("subtotal:", receipt.subtotal)
print("discount:", receipt.discount)
print("total:", receipt.total)

# คำนวณและตรวจสอบยอดเงิน
calculation = calculate_receipt(receipt)

print("\n===== CALCULATION RESULT =====")

for key, value in calculation.items():
    print(f"{key}: {value}")