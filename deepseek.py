import requests
import json

response = requests.post(
  url="https://openrouter.ai/api/v1/chat/completions",
  headers={
    "Authorization": "Bearer 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",
    "Content-Type": "application/json",
  },
  data=json.dumps({
    "model": "deepseek/deepseek-r1:free",
    "messages": [
      {
        "role": "user",
        "content": "What is the meaning of life?"
      }
    ],
    
  })
)

print(response.content)