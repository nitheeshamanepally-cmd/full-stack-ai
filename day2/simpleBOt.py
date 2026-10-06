import ollama
question=input("Ask the question:")
response=ollama.chat(
    model="llama3.2:3b",
    messages=[
        {
            "role":"system",
            "content":"Give the answers in 2-3 lines only"
        },
        {
            "role":"user",
            "content":question
        }
    ],
    options={
        "temperature": 2,
    }

)
print(response["message"]["content"])