from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
import os

app = FastAPI()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Use stable working model
model = genai.GenerativeModel("gemini-1.5-pro")

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
    full_prompt = SYSTEM_PROMPT + "\nUser: " + req.message
    response = model.generate_content(full_prompt)
    return {"response": response.text}
