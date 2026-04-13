import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask_ai(user_input):
    try:
        response = client.chat.completions.create(
  model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "Give short, fast and direct answers."},
                {"role": "user", "content": user_input}
            ]
        )
        return response.choices[0].message.content

    except Exception as e:
        return str(e)

st.title("🤖 Free Groq AI Agent")

user_input = st.text_input("Ask anything:")

if st.button("Send"):
    if user_input:
        st.write(ask_ai(user_input))
    else:
        st.warning("Type something!")