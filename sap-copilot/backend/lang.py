import os
from langchain_google_genai import ChatGoogleGenerativeAI

os.environ["GOOGLE_API_KEY"] = "" #Paste Gemini API key into the quotations

chat_model = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
response = chat_model.invoke("Hello, world!")
print(response.content)
