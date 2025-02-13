import streamlit as st
import google.generativeai as genai

genai.configure(api_key="AIzaSyCD36In7eRsq-0nx6jOrgCQbaUViP3Ls2I")

def review_code(code):
    prompt = f"""
    You are an AI code reviewer. Analyze the following Python code thoroughly and provide structured feedback in Markdown format. Your review should include:
    
    ### 1. Errors & Bugs
    - Identify **syntax errors**, **logical issues**, and **runtime exceptions**.
    - Provide explanations for why these errors occur.

    ### 2. Performance & Optimization
    - Suggest improvements for **speed**, **memory efficiency**, and **best practices**.
    - Identify **redundant operations** or **complexity improvements**.

    ### 3. Security Issues
    - Check for vulnerabilities such as **unsafe input handling**, **hardcoded secrets**, or **insecure API usage**.

    ### 4. Best Practices & Readability
    - Recommend improvements in **code structure, naming conventions, and comments**.

    ### 5. Fixed Code
    - Provide a fully **corrected and optimized version** of the code.

    **Code to review:**
    ```python
    {code}
    ```
    """
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

st.title("AI Code Reviewer (Google Gemini)")
st.write("Submit your Python code for an AI-powered, detailed review!")

code = st.text_area("Enter Python code here:", height=220)

if st.button("Review Code"):
    if code.strip():
        with st.spinner("Reviewing code..."):
            feedback = review_code(code)
        st.subheader("Detailed AI Review:")
        st.markdown(feedback)
    else:
        st.warning("Please enter some Python code.")
