from openai import OpenAI
client = OpenAI()

completion = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {"role": "developer", "content": "You are a helpful assistant."},
    {"role": "user", "content": "why is the sky blue?"}
  ]
)

# Extract and format the response nicely
response = completion.choices[0].message.content
print("\n" + "="*50)
print("CHATBOT RESPONSE:")
print("="*50)
print(response)
print("="*50 + "\n")