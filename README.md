CodeBuddy — Multi-Turn LLM Chatbot

A lightweight multi-turn chatbot built with Python, Flask, and the Google Gemini API (google-genai). It maintains per-conversation history, manages context window size with sliding-window truncation, uses a custom system prompt, and handles API/network errors gracefully.

Features

Backend Chat Endpoint (POST /chat): Sends user messages and conversation history to Gemini and returns structured JSON responses.

Per-Conversation History: Tracks separate chat histories in memory using a unique conversation_id per browser session.

Context Window Management: Uses a sliding window (MAX_HISTORY_MESSAGES = 10, keeping the last 5 user/model turns) so prompts stay bounded.

Custom System Prompt: Configures the assistant as CodeBuddy, a friendly, concise Python programming tutor.

Error Handling: Catches Gemini API errors and timeouts on the backend and displays clear error banners in the UI.

Secure Key Management: Loads GEMINI_API_KEY from environment variables (.env) and excludes .env and venv/ via .gitignore.

Tech Stack

Backend: Python, Flask

LLM SDK: google-genai (gemini-3.5-flash-lite)

Environment: python-dotenv

Frontend: HTML, CSS, Vanilla JavaScript (templates/index.html)

Project Structure

.
├── app.py
├── requirements.txt
├── .gitignore
└── templates/
    └── index.html


Setup & Run Locally

Clone the repository

git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME


Create and activate a virtual environment

python -m venv venv
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# macOS / Linux:
source venv/bin/activate


Install dependencies

pip install -r requirements.txt


Add your Gemini API key
Create a .env file in the project root:

GEMINI_API_KEY=your_actual_gemini_api_key_here


Run the app

python app.py


Open http://127.0.0.1:5000 in your browser.
