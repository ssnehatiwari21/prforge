from fastapi import FastAPI
from app.routes.webhook import router as webhook_router

app = FastAPI()

app.include_router(webhook_router, prefix="/webhook")

@app.get("/")
def home():
    return {
        "message": "PRForge Backend Running"
    }