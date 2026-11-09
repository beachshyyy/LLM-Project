
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

    # คำนวณยอดสุทธิและตรวจสอบกับ Total บนใบเสร็จ
    if subtotal is not None and printed_total is not None:

        effective_discount = (
            discount if discount is not None
            else Decimal("0.00")
        )

        calculated_total = subtotal - effective_discount

        total_difference = calculated_total - printed_total
        total_match = total_difference == Decimal("0.00")

    elif subtotal is None and printed_total is not None:

        # กรณีไม่มี Subtotal ให้ตรวจสอบ Items Total กับ Total โดยตรง
        calculated_total = items_total

        total_difference = calculated_total - printed_total
        total_match = total_difference == Decimal("0.00")

    else:
        calculated_total = None
        total_difference = None
        total_match = None

    # สรุปผลการตรวจสอบ
    if subtotal_match is False or total_match is False:
        overall_status = "MISMATCH"

    elif total_match is True:
        overall_status = "MATCH"

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
