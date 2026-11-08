
from PIL import Image

from app.services.ocr import extract_text
from app.services.extraction import extract_receipt
from app.services.tools import execute_tool


# เปิดรูปใบเสร็จ
image = Image.open("samples/receipt_sample.jpg")


# อ่านข้อความด้วย OCR
ocr_text = extract_text(image)


# แยกข้อมูลด้วย LLM
receipt = extract_receipt(ocr_text)


# เรียกใช้ Calculation Tool
result = execute_tool(
    tool_name="calculate_receipt",
    arguments="{}",
    receipt=receipt
)


# แสดงผลลัพธ์
print("\n===== TOOL RESULT =====")
print(result)
