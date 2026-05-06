import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

messages = []

print("Chat with Daniel (type 'exit' to quit)")
print("-" * 50)

while True:
    user_input = input("\nYou: ")
    if user_input.lower() == 'exit':
        break
    
    messages.append({"role": "user", "content": user_input})
    
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        messages=messages
    )
    
    assistant_message = response.content[0].text
    print(f"\nDaniel: {assistant_message}")
    messages.append({"role": "assistant", "content": assistant_message})
