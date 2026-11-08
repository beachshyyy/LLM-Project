from app.receipt import Receipt

sample_data = {
    "merchant": "7-Eleven",
    "items": [
        {
            "name": "ข้าวผัดไส้กรอก",
            "quantity": 1,
            "unit_price": 29.00,
            "total_price": 29.00
        }
    ],
    "subtotal": 29.00,
    "discount": 0.00,
    "total": 29.00
}

receipt = Receipt(**sample_data)

print("===== RECEIPT DATA =====")
print(receipt.model_dump_json(indent=2))
print("========================")