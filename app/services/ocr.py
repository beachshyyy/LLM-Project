import os
import shutil

import pytesseract
from PIL import Image, ImageOps, ImageEnhance


# ค้นหาตำแหน่ง Tesseract ตามระบบปฏิบัติการ
tesseract_path = os.getenv("TESSERACT_CMD") or shutil.which("tesseract")

# รองรับ Windows กรณีไม่ได้เพิ่ม Tesseract ไว้ใน PATH
if not tesseract_path and os.name == "nt":
    windows_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    if os.path.exists(windows_path):
        tesseract_path = windows_path

if tesseract_path:
    pytesseract.pytesseract.tesseract_cmd = tesseract_path


def extract_text(image: Image.Image) -> str:
    """
    รับภาพใบเสร็จ แล้วอ่านข้อความด้วย Tesseract OCR
    รองรับภาษาไทยและภาษาอังกฤษ
    """

    # แก้ทิศทางภาพตามข้อมูล EXIF
    image = ImageOps.exif_transpose(image)

    # แปลงภาพเป็นขาวดำ
    image = ImageOps.grayscale(image)

    # เพิ่มความคมชัดของภาพ
    image = ImageEnhance.Contrast(image).enhance(2)

    # ขยายภาพ 2 เท่า
    image = image.resize(
        (image.width * 2, image.height * 2)
    )

    # อ่านข้อความจากภาพ
    text = pytesseract.image_to_string(
        image,
        lang="tha+eng",
        config="--psm 6"
    )

    return text.strip()
