
from app.services.llm import client, MODEL_NAME
from app.services.tools import TOOLS, execute_tool
from app.receipt import Receipt


def run_agent(receipt: Receipt) -> str:
    """
    ให้ LLM ตัดสินใจเรียกใช้ Tool
    และนำผลลัพธ์กลับมาวิเคราะห์
    """

    messages = [
        {
            "role": "system",
            "content": """
You are a receipt analysis agent.

Your task is to verify receipt information.

Rules:
1. You must use the calculate_receipt tool
   to calculate and validate the receipt.
2. Do not calculate monetary values yourself.
3. Use the tool result as the source of truth
   for calculation results.
4. Explain whether the receipt data is consistent.
5. Do not invent missing information.
"""
        },
        {
            "role": "user",
            "content": f"""
Please analyze this receipt:

{receipt.model_dump_json(indent=2)}

Use the available tool to verify the receipt.
"""
        }
    ]

    # จำกัดจำนวนรอบเพื่อป้องกัน Agent ทำงานวนไม่สิ้นสุด
    max_iterations = 5

    for iteration in range(max_iterations):

        # ส่งข้อความให้ LLM พร้อมรายการ Tools
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto"
        )

        assistant_message = response.choices[0].message

        print("\n===== AGENT DEBUG =====")
        print("Tool calls:", assistant_message.tool_calls)
        print("LLM response:", assistant_message.content)
        print("=======================")

        # ถ้า LLM ไม่เรียก Tool แสดงว่าต้องการตอบกลับ
        if not assistant_message.tool_calls:
            return assistant_message.content or "Agent returned no response."

        # บันทึกคำสั่งของ LLM ลงใน Conversation
        messages.append(
            assistant_message.model_dump(exclude_none=True)
        )

        # ประมวลผล Tool Calls
        for tool_call in assistant_message.tool_calls:

            tool_name = tool_call.function.name
            arguments = tool_call.function.arguments

            try:
                tool_result = execute_tool(
                    tool_name=tool_name,
                    arguments=arguments,
                    receipt=receipt
                )

                print("\n===== TOOL EXECUTION =====")
                print("Tool name:", tool_name)
                print("Tool result:", tool_result)
                print("==========================")

            except Exception as error:
                tool_result = str(error)

            # ส่งผลลัพธ์กลับไปให้ LLM
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": tool_result
            })

    raise RuntimeError(
        "Agent exceeded the maximum number of iterations."
    )
