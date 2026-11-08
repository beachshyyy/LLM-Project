from PIL import Image
from app.services.ocr import extract_text


# เปิดรูปใบเสร็จ
image = Image.open("samples/receipt_sample.jpg")

# เรียกใช้ระบบ OCR
text = extract_text(image)

# แสดงผลลัพธ์
print("===== OCR RESULT =====")
print(text)
print("======================")