import os

from groq import Groq

os.environ["GROQ_API_KEY"] = "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"

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

chat = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Explain the importance of fast language models",
        }
    ],
    model="llama-3.3-70b-versatile",
)

print(chat.choices[0].message.content)