import os
from dotenv import load_dotenv
from datetime import datetime
import google.generativeai as genai
from init_db import init_db, save_message, get_chat_history

# Load API key
load_dotenv(dotenv_path=".env")
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# Initialize Gemini model
model = genai.GenerativeModel("models/gemini-2.5-flash")
chat = model.start_chat(history=[])

# Initialize database
init_db()

print("🤖 Gemini Chatbot (type 'exit' to quit)\n")

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        print("Bot: Goodbye 👋")
        break

    save_message("user", user_input)

    # Build context from last 5 messages
    history = get_chat_history(limit=5)
    context = "\n".join([f"{role}: {msg}" for role, msg in history])
    current_date = datetime.now().strftime("%A, %B %d, %Y")
    prompt = f"[Today is {current_date}]\n{context}\nYou: {user_input}"

    response = chat.send_message(prompt)
    bot_message = response.text
    print("Bot:", bot_message)

    save_message("bot", bot_message)
