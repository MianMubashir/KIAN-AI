import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
import os

# Set OpenAI API key

def generate_email(transcript: str, scenario: str) -> str:
    prompt = f"""
You are a professional business writer for a property consultancy firm. Based on the following meeting transcript and client scenario, generate a follow-up email.

Client Scenario: {scenario}
Meeting Transcript: {transcript}

The email should:
- Summarize key discussion points
- Address the clients business needs
- Include clear next steps
- Keep a helpful, professional tone
"""

    # Use the correct OpenAI method for chat completions
    response = client.chat.completions.create(model="gpt-4",  # You can also use "gpt-3.5-turbo" for a more cost-effective solution
    messages=[
        {"role": "system", "content": "You are a professional follow-up email generator."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.7)

    # Return the generated email content
    return response.choices[0].message.content.strip()
