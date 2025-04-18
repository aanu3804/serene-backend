import os
from dotenv import load_dotenv
from groq import Groq
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
groq_client = Groq(api_key=api_key)

def get_bot_reply(query):
    try:
        instructions = (
            "You are Serene, an emotional support chatbot. Respond with warmth, empathy, and a natural, friendly tone. "
            "For simple greetings like 'hlo' or 'hello', respond with: 'hello im Serene - Your Emotional Support Chatbot how can i help you'. "
            "For other inputs, validate the user’s feelings and offer support in 2-3 lines. "
            "For exercise requests (e.g., breathing, meditation), provide a detailed, step-by-step guide (5-8 sentences). "
            "Avoid mentioning emotions or mood logging in the response."
        )

        response = groq_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": instructions},
                {"role": "user", "content": query}
            ],
            max_tokens=800 if "exercise" in query.lower() else 200,
            temperature=0.7,
            top_p=0.9
        )
        reply = response.choices[0].message.content.strip()

        if query.lower() in ["hlo", "hello"]:
            reply = "hlo im Serene - Your Emotional Support Chatbot how can i help you"

        return {"lines": [reply], "emotion": None}
    except Exception as e:
        logger.error(f"Groq API error: {e}")
        return {"lines": ["Sorry, I’m having trouble connecting. How can I help you?"], "emotion": None}
