# PRForge — Automated AI GitHub PR Review System

PRForge is an automated GitHub pull request review system that uses large language models to analyze code changes and generate structured, line-by-line feedback directly in PR comments. It also supports interactive Q&A using `@prforge` mentions and stores all reviews and conversations in Supabase for persistent per-PR history.

---

## Features

- Automated pull request review on `pull_request` events  
- Line-by-line diff analysis with structured feedback  
- Interactive Q&A using `@prforge` mentions  
- Context-aware responses using PR diff + history  
- Stores all reviews and conversations in Supabase  
- Maintains per-PR history across commits  
- FastAPI backend with GitHub webhooks  
- AI-powered analysis using Groq (LLaMA 3.3 70B)  
- GitHub REST API integration  

---

## Architecture

GitHub PR / Comments  
↓  
FastAPI Webhooks  
↓  
Groq LLM Review Engine  
↓  
GitHub API (PR Comments)  
↓  
Supabase (History Storage)  


---

## Setup

### Clone repo

git clone https://github.com/your-username/prforge.git  
cd prforge  

### Create environment

python -m venv venv  
venv\Scripts\activate   # Windows  
source venv/bin/activate  

### Install dependencies

pip install -r requirements.txt  

### Environment variables

GROQ_API_KEY=your_key  
GITHUB_TOKEN=your_token  
DATABASE_URL=your_supabase_url  

### Run

uvicorn app.main:app --reload  

### Expose (Ngrok)

ngrok http 8000  

---

## Webhook URLs

https://your-ngrok-url/webhook/github  
https://your-ngrok-url/webhook/github/comments  

---

## GitHub Events

| Event | Trigger |
|------|--------|
| pull_request | opened, synchronize |
| issue_comment | @prforge mention |

---

## Example

### PR Review Output

Line 42:  
Missing input validation  
Risk: SQL injection  
Fix: Use parameterized queries  

---

### Q&A

@prforge why is this unsafe?

It is unsafe because it processes unvalidated user input, which may lead to injection attacks.

---

## Tech Stack

FastAPI • Groq LLM • GitHub API • Supabase • SQLAlchemy • Ngrok  

---

## Known Issues

- Bot must ignore its own messages to prevent loops  
- GitHub rate limits apply  
- Large PRs may take longer  

---

## Author

Sneha Tiwari  
GitHub: https://github.com/ssnehatiwari21  
