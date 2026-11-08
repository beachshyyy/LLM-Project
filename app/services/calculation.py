
from decimal import Decimal

from app.receipt import Receipt


def calculate_receipt(receipt: Receipt) -> dict:
    """
    คำนวณยอดรวมจากรายการสินค้า
    และตรวจสอบความถูกต้องกับข้อมูลบนใบเสร็จ
    """

    # รวมราคาสินค้าทั้งหมด
    items_total = sum(
        (
            Decimal(str(item.total_price))
            for item in receipt.items
        ),
        Decimal("0.00")
    )

    # อ่าน Subtotal, Discount และ Total
    subtotal = (
        Decimal(str(receipt.subtotal))
        if receipt.subtotal is not None
        else None
    )

    discount = (
        Decimal(str(receipt.discount))
        if receipt.discount is not None
        else None
    )

    printed_total = (
        Decimal(str(receipt.total))
        if receipt.total is not None
        else None
    )

    # ตรวจสอบผลรวมรายการสินค้ากับ Subtotal
    if subtotal is not None:
        subtotal_difference = items_total - subtotal
        subtotal_match = subtotal_difference == Decimal("0.00")
    else:
        subtotal_difference = None
        subtotal_match = None

    # คำนวณยอดสุทธิจาก Subtotal และส่วนลด
    if subtotal is not None and discount is not None:
        calculated_total = subtotal - discount
    else:
        calculated_total = None

    # ตรวจสอบยอดสุทธิกับ Total บนใบเสร็จ
    if calculated_total is not None and printed_total is not None:
        total_difference = calculated_total - printed_total
        total_match = total_difference == Decimal("0.00")
    else:
        total_difference = None
        total_match = None

    # สรุปผลการตรวจสอบ
    checks = [
        subtotal_match,
        total_match
    ]

    if all(result is True for result in checks):
        overall_status = "MATCH"
    elif any(result is False for result in checks):
        overall_status = "MISMATCH"
    else:
        overall_status = "INCOMPLETE"

    return {
        "items_total": float(items_total),
        "subtotal": float(subtotal) if subtotal is not None else None,
        "subtotal_difference": (
            float(subtotal_difference)
            if subtotal_difference is not None
            else None
        ),
        "subtotal_match": subtotal_match,
        "discount": float(discount) if discount is not None else None,
        "calculated_total": (
            float(calculated_total)
            if calculated_total is not None
            else None
        ),
        "printed_total": (
            float(printed_total)
            if printed_total is not None
            else None
        ),
        "total_difference": (
            float(total_difference)
            if total_difference is not None
            else None
        ),
        "total_match": total_match,
        "overall_status": overall_status
    }
