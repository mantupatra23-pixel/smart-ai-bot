from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import google.generativeai as genai
import os

app = FastAPI()

# Configure API Key
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

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
    try:
        full_prompt = SYSTEM_PROMPT + "\nUser: " + req.message

        # FIX: Using 'generate_content_async' instead of 'generate_content'
        # with 'await' to prevent blocking the FastAPI event loop
        response = await model.generate_content_async(full_prompt)

        return {"response": response.text}

    except Exception as e:
        # FIX: Added error handling to catch and display the exact API error
        raise HTTPException(status_code=500, detail=f"Gemini API Error: {str(e)}")

