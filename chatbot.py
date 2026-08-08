from langchain_ollama import ChatOllama

# Load AI Model
llm = ChatOllama(
    model="gemma:2b",
    temperature=0.3
)

def get_response(question):

    q = question.lower().strip()

    # Fixed Responses
    if "your name" in q or "who are you" in q:
        return "I am IntelliAssist AI, your personal AI assistant."

    if q in ["hi", "hello", "hey"]:
        return "Hello! 👋 How can I help you today?"

    if q in ["thanks", "thank you"]:
        return "You're welcome! 😊"

    if q in ["bye", "goodbye"]:
        return "Goodbye! Have a great day. 👋"

    prompt = f"""
You are IntelliAssist AI.

Rules:
- Your name is IntelliAssist AI.
- Never say you are ChatGPT.
- Never say you are Google AI.
- Answer professionally.
- Keep answers short and clear.
- If the user uploads a PDF, answer only from the PDF content provided.
- If the answer is not available, clearly say you couldn't find it.

User:
{question}
"""

    try:
        response = llm.invoke(prompt)
        return response.content

    except Exception as e:
        return f"❌ Error: {e}"