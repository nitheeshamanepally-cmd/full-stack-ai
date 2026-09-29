import ollama
response=ollama.chat(
    model="llama3.2:3b",
    messages=[
        {
            "role":"user",
            "content":"Explain the use of llama in 6lines"
        }
    ],
    options={
        "temperature": 0.7,
    },

)
print(response["message"]["content"])