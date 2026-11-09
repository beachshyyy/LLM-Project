from pydantic import BaseModel, Field, field_validator
from typing import Optional


class ReceiptItem(BaseModel):
    name: str = Field(description="Item name")
    quantity: float = Field(description="Quantity")
    unit_price: float = Field(description="Price per unit")
    total_price: float = Field(description="Total price")

    @field_validator(
        "quantity",
        "unit_price",
        "total_price",
        mode="before"
    )
    @classmethod
    def clean_item_numbers(cls, value):
        if isinstance(value, str):
            value = value.replace(",", "").strip()
        return value


class Receipt(BaseModel):
    merchant: Optional[str] = Field(
        default=None,
        description="Shop name"
    )

    items: list[ReceiptItem] = Field(
        default_factory=list,
        description="Items"
    )

    subtotal: Optional[float] = Field(
        default=None,
        description="Subtotal before discount"
    )

    discount: Optional[float] = Field(
        default=None,
        description="Discount amount"
    )

    total: Optional[float] = Field(
        default=None,
        description="Final amount paid"
    )

    @field_validator(
        "subtotal",
        "discount",
        "total",
        mode="before"
    )
    @classmethod
    def clean_receipt_numbers(cls, value):
        if isinstance(value, str):
            value = value.replace(",", "").strip()

            if value.lower() in ("", "null", "none"):
                return None

        return value