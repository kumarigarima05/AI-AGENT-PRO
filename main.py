import os
import streamlit as st
from groq import Groq

from langchain_core.tools import tool
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("Missing GROQ_API_KEY in Secrets")
    st.stop()

client = Groq(api_key=api_key)

# ---------------- TOOLS ---------------- #

@tool
def training_planner(topic: str):
    """Creates a learning/training plan"""
    return f"Training Plan for {topic}:\n1. Basics\n2. Intermediate\n3. Advanced\n4. Projects"

@tool
def schedule_meeting(task: str):
    """Creates a meeting schedule plan"""
    return f"Meeting Scheduled:\nTopic: {task}\nDuration: 1 hour\nStatus: Planned (AI simulated)"

@tool
def task_breakdown(task: str):
    """Breaks task into steps"""
    return f"Task Breakdown:\n- Understand {task}\n- Plan execution\n- Implement\n- Review"

tools = [training_planner, schedule_meeting, task_breakdown]

# ---------------- SIMPLE AGENT LOGIC ---------------- #

def run_agent(user_input):
    if "train" in user_input.lower():
        return training_planner(user_input)
    elif "schedule" in user_input.lower():
        return schedule_meeting(user_input)
    elif "task" in user_input.lower():
        return task_breakdown(user_input)
    else:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are an AI productivity agent."},
                {"role": "user", "content": user_input}
            ]
        )
        return response.choices[0].message.content

# ---------------- UI ---------------- #

st.title("🤖 AI Productivity Agent (LangChain + Groq)")

user_input = st.text_input("Ask me anything (training, schedule, tasks)")

if st.button("Run"):
    if user_input:
        st.write(run_agent(user_input))