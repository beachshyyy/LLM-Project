
import json

from app.receipt import Receipt
from app.services.calculation import calculate_receipt


# รายการเครื่องมือที่เปิดให้ LLM เรียกใช้
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "calculate_receipt",
            "description": (
                "Calculate receipt totals and validate "
                "the extracted receipt data."
            ),
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
                "additionalProperties": False
            }
        }
    }
]


def execute_tool(
    tool_name: str,
    arguments: str,
    receipt: Receipt
) -> str:

    # ตรวจสอบชื่อเครื่องมือ
    if tool_name != "calculate_receipt":
        raise ValueError(f"Unknown tool: {tool_name}")

    # ตรวจสอบ arguments ที่ LLM ส่งมา
    try:
        args = json.loads(arguments or "{}")
    except json.JSONDecodeError:
        raise ValueError("Invalid tool arguments.")

    if not isinstance(args, dict):
        raise ValueError("Tool arguments must be a JSON object.")

    if args:
        print("Warning: Ignoring unexpected tool arguments:", args)

    # เรียกใช้ฟังก์ชันคำนวณที่เราเขียนไว้
    result = calculate_receipt(receipt)

    # ส่งผลลัพธ์กลับเป็น JSON string
    return json.dumps(result, ensure_ascii=False)
