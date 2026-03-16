import streamlit as st
import sys
import os
from dotenv import load_dotenv

sys.path.append(os.getcwd())
from src.agents.classification_agent import InsightsAgent
from app.components.charts import add_footer

load_dotenv()

st.set_page_config(page_title="AI Insights Agent", layout="wide")

st.title("🤖 AI Insights Agent")

st.markdown("""
Ask our AI Agent anything about the Peruvian GitHub ecosystem! 
The agent has access to the metadata of the 1,000 developers and repositories we analyzed.
""")

# Initialize agent
if "agent" not in st.session_state:
    api_key = st.session_state.get("openai_api_key")
    st.session_state.agent = InsightsAgent(api_key=api_key)
else:
    # Update key if it changed in sidebar
    new_key = st.session_state.get("openai_api_key")
    if st.session_state.agent.api_key != new_key:
        st.session_state.agent = InsightsAgent(api_key=new_key)

# Chat interface
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask about technical trends, top industries, or developer activity in Peru"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing ecosystem data..."):
            response = st.session_state.agent.answer_question(prompt)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

# Add Branding Footer
add_footer()
