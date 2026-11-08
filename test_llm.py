from app.services.llm import client, BASE_URL, MODEL_NAME

print("===== LLM CONNECTION TEST =====")

try:
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": "Hello! Please introduce yourself briefly."
            }
        ]
    )

    print("Model:", MODEL_NAME)
    print("Response:", response.choices[0].message.content)

    print("===============================")
    print("LLM connection successful!")

except Exception as e:
    print("LLM connection failed!")
    print("Error:", e)