import os
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from google import genai
from google.genai import types
from google.genai.errors import APIError

load_dotenv()

app = Flask(__name__)

# Initialize Gemini client (reads GEMINI_API_KEY from .env)
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None

MODEL_NAME = "gemini-3.5-flash-lite"
MAX_HISTORY_MESSAGES = 10  # Keeps the last 10 messages (5 user + 5 model turns)

SYSTEM_PROMPT = (
    "You are CodeBuddy, a friendly and concise Python programming tutor. "
    "Explain concepts simply, give short code examples when helpful, "
    "and remember details the user shares earlier in the conversation."
)

# In-memory store: { conversation_id: [ {"role": "user"|"model", "parts": [{"text": "..."}]} ] }
conversations: dict[str, list[dict]] = {}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    if client is None:
        return jsonify({"error": "Server is missing GEMINI_API_KEY in .env."}), 500

    data = request.get_json(silent=True) or {}
    user_message = (data.get("message") or "").strip()
    conversation_id = (data.get("conversation_id") or "default").strip()

    if not user_message:
        return jsonify({"error": "Please enter a message before sending."}), 400

    # Retrieve or initialize history for this conversation
    history = conversations.setdefault(conversation_id, [])

    # Append the new user message
    history.append({"role": "user", "parts": [{"text": user_message}]})

    # Context window management: truncate to the last N messages
    trimmed_history = history[-MAX_HISTORY_MESSAGES:]

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=trimmed_history,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                http_options=types.HttpOptions(timeout=20_000),  # 20s timeout
            ),
        )
        bot_reply = response.text or "I couldn't generate a response. Please try again."

        # Save the model's reply and keep stored history bounded
        history.append({"role": "model", "parts": [{"text": bot_reply}]})
        conversations[conversation_id] = history[-MAX_HISTORY_MESSAGES:]

        return jsonify({
            "reply": bot_reply,
            "history_length": len(conversations[conversation_id]),
        })

    except APIError as e:
        print("Gemini APIError:", e)
        history.pop()
        error_detail = getattr(e, "message", str(e))
        return jsonify({"error": f"LLM API error ({e.code}): {error_detail}"}), 502
    except Exception as e:
        print("Unexpected error:", e)
        history.pop()
        return jsonify({"error": "Request timed out or failed. Please check your connection and try again."}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)