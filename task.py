import google.generativeai as genai
import streamlit as st

class AiCodeReviewer:
    def __init__(self):
        self.key = "AIzaSyCD36In7eRsq-0nx6jOrgCQbaUViP3Ls2I"

    def chatbot(self, system_instruction: str = None) -> object:
        genai.configure(api_key=self.key)
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=system_instruction
        )
        return model

    def streamlit_app(self) -> None:
        st.markdown(
            """
            <style>
            .stChatMessage { 
                border-radius: 10px; 
                padding: 10px; 
                margin: 5px 0; 
                font-weight: bold; 
                font-family: Arial, sans-serif;
            }
            .stChatMessage.user { 
                background-color: #f5f5f5; 
                color: #000000; 
                border: 1px solid #dcdcdc;
            }
            .stChatMessage.ai { 
                background-color: #ffffff; 
                color: #000000; 
                border: 1px solid #dcdcdc;
            }
            .code-container { 
                background-color: #f4f4f4; 
                padding: 10px; 
                border-radius: 10px; 
                font-family: monospace;
            }
            </style>
            """, 
            unsafe_allow_html=True
        )

        st.title("🚀 AI Code Reviewer")

        if "chat_history" not in st.session_state:
            st.session_state["chat_history"] = []

        instruction = """You are an expert AI code reviewer. Analyze the provided code for clarity, efficiency, and maintainability.
        Identify potential errors, suggest improvements, and provide clear, actionable feedback."""
        
        model = self.chatbot(instruction)
        chat = model.start_chat(history=st.session_state["chat_history"])

        for msg in chat.history:
            role_class = "user" if msg.role == "user" else "ai"
            st.markdown(f'<div class="stChatMessage {role_class}">{msg.parts[0].text}</div>', unsafe_allow_html=True)

        st.subheader("📝 Submit Your Code for Review")
        user_code = st.text_area("Paste your Python code here:", height=150)
        submit = st.button("🔍 Analyze Code")

        if submit and user_code:
            st.markdown(f'<div class="stChatMessage user">{user_code}</div>', unsafe_allow_html=True)
            response = chat.send_message(user_code)
            st.markdown(f'<div class="stChatMessage ai">{response.text}</div>', unsafe_allow_html=True)
            st.session_state["chat_history"] = chat.history

if __name__ == "__main__":
    ai = AiCodeReviewer()
    ai.streamlit_app()
