import os
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

def test_chat():
    try:
        llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash", temperature=0.3)
        msg = HumanMessage(content="Hello")
        response = llm.invoke([msg])
        print("Success! Response:", response.content)
    except Exception as e:
        print("Error:", str(e))

if __name__ == "__main__":
    # We must mock an API key or use the user's API key
    test_chat()
