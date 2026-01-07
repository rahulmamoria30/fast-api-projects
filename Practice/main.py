import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import google.generativeai as genai
from init_db import init_db
from api.chat import router as chat_router

# Load env
load_dotenv(".env")

# Create FastAPI app
app = FastAPI(title="Chat API with FastAPI")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],

)

# Configure Gemini API
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# Include API router
app.include_router(chat_router, prefix="/chat")

# Init DB
init_db()
