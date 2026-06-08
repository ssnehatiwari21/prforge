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
You are a Staff Software Engineer reviewing a GitHub Pull Request.

Review the git diff below.

For every issue found provide:

### Issue
Severity: Low / Medium / High
Approximate Line Number:
Problem:
Why it matters:
Suggested Fix:

If possible include improved code.

Focus on:
- Bugs
- Security vulnerabilities
- Performance issues
- Maintainability
- Code quality

If no issues exist, say:
No significant issues found.

Git Diff:
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
        temperature=0.2
    )

    return completion.choices[0].message.content


def answer_pr_question(history, pr_files, commenter):

    latest_question = history[-1].message

    system_prompt = f"""
You are PRForge, an AI code review assistant.

Files changed in this PR:

{pr_files}

The latest question from the user is:

{latest_question}

Answer only that question while using previous conversation as context.

Be concise.
Use Markdown.
Reference code when relevant.

Format exactly:

**@{commenter} asked:**

<answer>
"""

    messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]

    for entry in history:
        messages.append({
            "role": entry.role,
            "content": entry.message
        })

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.4
    )

    return completion.choices[0].message.content