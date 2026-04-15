import streamlit as st
import os
from dotenv import load_dotenv
import re
import datetime

from langchain_groq import ChatGroq

# -----------------------------
# 🔐 LOAD API KEY
# -----------------------------
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("❌ GROQ_API_KEY missing in .env file")
    st.stop()

# -----------------------------
# 🤖 LLM
# -----------------------------
llm = ChatGroq(
    api_key=GROQ_API_KEY,
    model="llama-3.1-8b-instant"
)

# -----------------------------
# 🧠 SIMPLE MEMORY (SAFE)
# -----------------------------
MEMORY_FILE = "memory.txt"

def save_memory(user_input, response):
    try:
        with open(MEMORY_FILE, "a", encoding="utf-8") as f:
            f.write(f"User: {user_input}\nAI: {response}\n\n")
    except:
        pass

def load_memory():
    try:
        if not os.path.exists(MEMORY_FILE):
            return ""
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return f.read()[-800:]
    except:
        return ""

# -----------------------------
# 🧠 DATE/TIME EXTRACTOR (FIXED)
# -----------------------------
def extract_datetime(text):
    text = re.sub(r'(\d{1,2})([a-zA-Z])', r'\1 \2', text)
    text = re.sub(r'([a-zA-Z])(\d{4})', r'\1 \2', text)

    pattern = r'(\d{1,2}\s\w+\s\d{4}).*(\d{1,2}:\d{2}\s?(AM|PM|am|pm)?)'
    match = re.search(pattern, text)

    if match:
        date = match.group(1)
        time = match.group(2)
        return date, time

    return None, None

# -----------------------------
# 🛠️ TOOLS (SAFE MODE - NO CRASH)
# -----------------------------
def schedule_meeting(text):
    date, time = extract_datetime(text)

    return f"""
📅 MEETING SCHEDULED
------------------------
📌 Details: {text}
📆 Date: {date if date else "Not detected"}
⏰ Time: {time if time else "Not detected"}
🤖 AI Agent Active
"""

def training_plan(text):
    return f"""
🧑‍🏫 TRAINING PLAN CREATED
------------------------
📌 Plan: {text}
🤖 Status: Ready
"""

def delivery_task(text):
    return f"""
📦 DELIVERY TASK UPDATED
------------------------
📌 Task: {text}
🤖 Status: Tracking Enabled
"""

# -----------------------------
# 🧠 ROUTER (WITH MEMORY)
# -----------------------------
def router(user_input):
    text = user_input.lower()
    memory = load_memory()

    if "meeting" in text:
        response = schedule_meeting(user_input)

    elif "training" in text:
        response = training_plan(user_input)

    elif "delivery" in text:
        response = delivery_task(user_input)

    else:
        try:
            prompt = f"""
Previous context:
{memory}

User: {user_input}
"""
            response = llm.invoke(prompt).content
        except Exception as e:
            response = f"❌ Error: {str(e)}"

    save_memory(user_input, response)
    return response

# -----------------------------
# 🌐 UI
# -----------------------------
st.set_page_config(page_title="AI Agent Pro", page_icon="🤖")

st.title("🤖 AI Training & Scheduling Agent")
st.write("Meeting • Training • Delivery AI Assistant")

user_input = st.text_input("Enter your task")

if user_input:
    with st.spinner("Processing... 🤖"):
        response = router(user_input)

    st.success(response)