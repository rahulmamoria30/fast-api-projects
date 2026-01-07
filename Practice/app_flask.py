import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from datetime import datetime
import google.generativeai as genai
from init_db import init_db, save_message, get_chat_history
from flask_cors import CORS

app = Flask(__name__)
CORS(
    app,
    resources={r"/*": {"origins": "*"}},
    supports_credentials=False
)


# Load API key
load_dotenv(dotenv_path=".env")
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# Initialize Gemini model
model = genai.GenerativeModel("models/gemini-2.5-flash")
chat = model.start_chat(history=[])

# Initialize database
init_db()


@app.route("/chat/history", methods=["GET"])
def get_chat_response():
    """
    Query Params (optional):
    ?limit=10

    Returns:
    {
        "history": [
            {"role": "user", "message": "Hi"},
            {"role": "bot", "message": "Hello!"}
        ]
    }
    """
    limit = request.args.get("limit", default=10, type=int)

    history = get_chat_history(limit=limit)

    formatted_history = [
        {"role": role, "message": msg}
        for role, msg in history
    ]

    return jsonify({
        "history": formatted_history
    })
@app.route("/getresponse", methods=["GET"])
def get_response():
    """
    Example:
    GET /getresponse?message=Hello

    Response:
    {
        "response": "Hi! How can I help you?"
    }
    """
    user_input = request.args.get("message")

    if not user_input:
        return jsonify({"error": "Missing 'message' query parameter"}), 400

    # Save user message
    save_message("user", user_input)

    # Get last 5 messages for context
    history = get_chat_history(limit=5)
    context = "\n".join([f"{role}: {msg}" for role, msg in history])

    # Add current date for context
    current_date = datetime.now().strftime("%A, %B %d, %Y")
    prompt = f"[Today is {current_date}]\n{context}\nUser: {user_input}"

    # Send to Gemini
    response = chat.send_message(prompt)
    bot_message = response.text

    # Save bot response
    save_message("bot", bot_message)

    return jsonify({
        "response": bot_message
    })

if __name__ == "__main__":
    app.run(debug=True)
