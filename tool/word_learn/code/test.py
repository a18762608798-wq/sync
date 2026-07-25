# Please install OpenAI SDK first: `pip3 install openai`
from openai import OpenAI
import sys

client = OpenAI(
    api_key="sk-07eee6e7069e4b7b907a8c2d56f72577", base_url="https://api.deepseek.com"
)

response = client.chat.completions.create(
    model="deepseek-reasoner",
    messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello"},
    ],
    stream=False,
)

print(sys.executable)
print(response.choices[0].message.content)
