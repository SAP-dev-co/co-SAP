import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chat_models.base import BaseChatModel

load_dotenv()

def get_llm() -> BaseChatModel:

    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        raise EnvironmentError("Missing GOOGLE_API_KEY in .env file.")

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=api_key,
        temperature=0.3,
        max_output_tokens=2048
    )
    return llm