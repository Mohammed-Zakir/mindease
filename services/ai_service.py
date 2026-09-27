import os
import time

from dotenv import load_dotenv
from google import genai
from google.genai.errors import ClientError

from services.crisis_service import detect_crisis
from services.rag_service import retrieve_context

load_dotenv()

# ---------------------------------------------------
# Gemini Setup (lazy init)
# ---------------------------------------------------

_client = None

def get_client():
    global _client
    if _client is None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is missing from your .env file")
        _client = genai.Client(api_key=api_key)
    return _client


# ---------------------------------------------------
# System Prompt
# ---------------------------------------------------

SYSTEM_PROMPT = """
You are Dr. MindEase, a compassionate AI mental wellness companion.

RULES:
- Be calm and supportive
- Never diagnose medical conditions
- Encourage healthy habits
- Suggest professional help when needed
- Keep responses conversational and brief
"""

CRISIS_MESSAGE = """
I'm really sorry you're going through this.

Please consider reaching out to someone you trust or a mental health professional.

India Crisis Support:
- iCall: 9152987821
- Vandrevala Foundation: 1860-2662-345
"""

QUOTA_MESSAGE = """
I'm taking a short breather — our AI service has hit its hourly limit.

Please try again in a few minutes. I'll be right back! 🙏
"""


# ---------------------------------------------------
# Generate AI Response  (retries on 429)
# ---------------------------------------------------

def generate_response(user_message):

    if detect_crisis(user_message):
        return CRISIS_MESSAGE

    context_docs = retrieve_context(user_message)
    context = "\n".join(context_docs)

    final_prompt = f"""
    {SYSTEM_PROMPT}

    Context:
    {context}

    User:
    {user_message}
    """

    for attempt in range(2):          # try twice before giving up
        try:
            response = get_client().models.generate_content(
                model="gemini-1.5-flash",   # higher free-tier quota than 2.0-flash
                contents=final_prompt
            )
            return response.text

        except ClientError as e:
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                if attempt == 0:
                    time.sleep(5)     # wait 5 s then retry once
                    continue
                return QUOTA_MESSAGE
            print("GEMINI ERROR:", e)
            return "I'm having a moment of difficulty. Please try again shortly. 🙏"

        except Exception as e:
            print("GEMINI ERROR:", e)
            return "I'm having a moment of difficulty. Please try again shortly. 🙏"
