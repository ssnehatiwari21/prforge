import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def analyze_code_patch(patch):

    if not patch:
        return "No code changes found."

    prompt = f"""
You are an expert senior software engineer reviewing a pull request.

Analyze this code diff and provide:
- bugs
- bad practices
- security concerns
- improvements

Keep review concise and practical.

Code diff:
{patch}
"""

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    return completion.choices[0].message.content