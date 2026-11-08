import pytesseract
from PIL import Image, ImageOps, ImageEnhance

# ระบุตำแหน่งโปรแกรม Tesseract ใน Windows
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


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