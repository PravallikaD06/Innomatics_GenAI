import streamlit as st
import os
from langchain_google_genai import GoogleGenerativeAI
from langchain.memory import ChatMessageHistory

GOOGLE_API_KEY = "AIzaSyBfBoBNLxDtfaCCDmNa1NsWZVx2ABMkNUc"
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

llm = GoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.7, google_api_key=GOOGLE_API_KEY)

memory = ChatMessageHistory()

def is_data_science_related(query):
    check_prompt = f"Is the following question related to Data Science? Answer only with 'yes' or 'no': {query}"
    try:
        response = llm(check_prompt).strip().lower()
        return response == "yes"
    except Exception:
        return False

st.set_page_config(page_title="AI Data Science Tutor", layout="wide")

st.markdown("""
    <style>
        .stChatMessage {
            border-radius: 12px;
            padding: 12px;
            margin-bottom: 10px;
        }
        .user-message {
            background-color: #D3E4CD;
            color: #2F3E46;
            text-align: left;
        }
        .assistant-message {
            background-color: #CAD2C5;
            color: #2F3E46;
            text-align: left;
        }
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("📝 Chat Settings")
    if st.button("🗑️ Clear Chat History"):
        st.session_state["messages"] = []
        st.session_state["memory"] = ChatMessageHistory()
        st.success("Chat history cleared!")

st.title("🤖 Conversational AI Data Science Tutor")

if "memory" not in st.session_state:
    st.session_state["memory"] = memory

if "messages" not in st.session_state:
    st.session_state["messages"] = []

for message in st.session_state["messages"]:
    role_class = "user-message" if message["role"] == "user" else "assistant-message"
    st.markdown(f'<div class="stChatMessage {role_class}">{message["content"]}</div>', unsafe_allow_html=True)

user_input = st.text_input("💬 Ask a Data Science doubt...", key="user_input")

if user_input:
    if is_data_science_related(user_input):
        try:
            response = llm(user_input)
        except Exception as e:
            response = f"⚠️ Error: {str(e)}"

        st.session_state["memory"].add_user_message(user_input)
        st.session_state["memory"].add_ai_message(response)

        st.session_state["messages"].append({"role": "user", "content": user_input})
        st.session_state["messages"].append({"role": "assistant", "content": response})

        st.markdown(f'<div class="stChatMessage user-message">{user_input}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="stChatMessage assistant-message">{response}</div>', unsafe_allow_html=True)
    else:
        st.warning("❌ I can only assist with Data Science-related questions.")
