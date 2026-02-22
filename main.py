from fastapi import FastAPI
from pydantic import BaseModel
from google import genai
import os

app = FastAPI()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

class ChatRequest(BaseModel):
    message: str

SYSTEM_PROMPT = """
You are a Smart AI Business Assistant.
You handle:
- Hotel bookings
- E-commerce support
- SaaS queries
- General AI help
Respond professionally.
"""

@app.get("/")
def home():
    return {"message": "Gemini AI Bot Running 🚀"}

@app.post("/chat")
async def chat(req: ChatRequest):
    response = client.models.generate_content(
       model="gemini-1.5-flash-001",
        contents=SYSTEM_PROMPT + "\nUser: " + req.message
    )

    return {"response": response.text}
