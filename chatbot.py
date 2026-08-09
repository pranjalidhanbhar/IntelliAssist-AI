import os
import ast
import json
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI


# Load .env from the same folder as chatbot.py
ENV_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
load_dotenv(ENV_PATH, override=True)


def _get_llm():
    """Create the Gemini model only when a response is requested."""

    # Make sure .env is loaded every time
    load_dotenv(ENV_PATH, override=True)

    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GOOGLE_API_KEY is not configured. "
            "Please check the .env file."
        )

    return ChatGoogleGenerativeAI(
        model="gemini-3.5-flash",
        temperature=0.3,
        google_api_key=api_key,
    )


def get_response(question, context=""):
    """
    Generate an IntelliAssist AI response.

    Parameters
    ----------
    question : str
        User's question.
    context : str, optional
        Text extracted from the uploaded PDF. When provided, the model
        answers using this document context.
    """

    q = question.lower().strip()

    # Fixed responses
    if "your name" in q or "who are you" in q:
        return "I am IntelliAssist AI, your personal AI assistant."

    if q in ["hi", "hello", "hey"]:
        return "Hello! 👋 How can I help you today?"

    if q in ["thanks", "thank you"]:
        return "You're welcome! 😊"

    if q in ["bye", "goodbye"]:
        return "Goodbye! Have a great day. 👋"

    if context and context.strip():
        prompt = f"""
You are IntelliAssist AI, an AI-powered PDF document assistant.

Follow these rules strictly:
- Your name is IntelliAssist AI.
- Never say you are ChatGPT.
- Never say you are Google AI.
- Answer professionally, clearly, and concisely.
- Use ONLY the PDF content provided below to answer the user's question.
- Do not invent or assume information that is not present in the PDF.
- If the answer cannot be found in the PDF, say:
  "I couldn't find that information in the uploaded PDF."

PDF CONTENT:
--------------------
{context}
--------------------

USER QUESTION:
{question}
"""
    else:
        prompt = f"""
You are IntelliAssist AI, a professional AI assistant.

Follow these rules:
- Your name is IntelliAssist AI.
- Never say you are ChatGPT.
- Never say you are Google AI.
- Answer professionally.
- Keep answers short, clear, and useful.
- There is no PDF context available for this question.

USER:
{question}
"""    
    try:
        llm = _get_llm()
        response = llm.invoke(prompt)
        content = response.content

        if isinstance(content, str):
            return content

        if isinstance(content, list):
            text_parts = []

            for item in content:
                if isinstance(item, dict) and item.get("type") == "text":
                    text_parts.append(item.get("text", ""))
                elif isinstance(item, str):
                    text_parts.append(item)

            return "\n".join(text_parts).strip()

        return str(content)

    except Exception as e:
        return f"❌ Error: {e}"