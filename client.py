from openai import OpenAI

client = OpenAI(
    api_key="<Your Key Here>"
)  # Pass key explicitly

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named Sam skilled in general tasks like Alexa and Google Cloud."},
        {"role": "user", "content": "What is coding?"}
    ]
)

print(completion.choices[0].message["content"])

