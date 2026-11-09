from pydantic import BaseModel, Field, field_validator
from typing import Optional


class ReceiptItem(BaseModel):
    name: str = Field(description="Item name")
    quantity: float = Field(description="Quantity")
    unit_price: float = Field(description="Price per unit")
    total_price: float = Field(description="Total price")


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