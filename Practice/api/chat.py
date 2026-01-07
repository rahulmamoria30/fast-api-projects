from fastapi import APIRouter, HTTPException
from datetime import datetime
import google.generativeai as genai
from init_db import save_message, get_chat_history

router = APIRouter()
model = genai.GenerativeModel("models/gemini-2.5-flash")
chat = model.start_chat(history=[])


@router.get("/history")
def get_chat_history_endpoint(limit: int = 10):
    """ Get recent chat history """
    history = get_chat_history(limit=limit)
    result = [{"role": role, "message": msg} for role, msg in history]
    return {"history": result}


@router.get("/response")
def get_chat_response(message: str = None):
    """ Get AI response for a message """
    if not message:
        raise HTTPException(status_code=400, detail="Missing 'message' query parameter")

    save_message("user", message)

    # last 5 messages context
    history = get_chat_history(limit=5)
    context = "\n".join([f"{role}: {msg}" for role, msg in history])

    current_date = datetime.now().strftime("%A, %B %d, %Y")
    prompt = f"[Today is {current_date}]\n{context}\nUser: {message}"

    try:
        response = chat.send_message(prompt)
        bot_message = response.text
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    save_message("bot", bot_message)

    return {"response": bot_message}
