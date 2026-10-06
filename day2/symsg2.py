import ollama
response=ollama.chat(
    model="llama3.2:3b",
    messages=[
        {
            "role":"system",
            "content":"Give the answers in 2-3 lines only"
        },
        {
            "role":"user",
            "content":"give ur giving 5 year chiild wt is ai?"
        }
    ],
    options={
        "temperature": 0.7,
    }

)
print(response["message"]["content"])