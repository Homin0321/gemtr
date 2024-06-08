import streamlit as st
import google.generativeai as genai

# Constants for better readability and maintainability
COMMAND = "다음 영문을 설명이나 요약을 덧붙이지 말고 그대로 한국어로 번역해줘: "
PASSWORD = st.secrets["passwd"]  # Store password securely in secrets
API_KEY = st.secrets["api_key"]  # Store API key securely in secrets

# Configure Gemini only once
if "model" not in st.session_state:
    genai.configure(api_key=API_KEY)
    st.session_state.model = genai.GenerativeModel(
        "gemini-1.5-pro-latest",
        generation_config=genai.types.GenerationConfig(temperature=1),
        safety_settings=[
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ],
    )

def show_paragraph(text):
    """Displays English text and its Korean translation side-by-side."""
    response = st.session_state.model.generate_content(COMMAND + text)
    text_para = text.split('\n\n')
    resp_para = response.text.split('\n\n')

    # Handle cases where paragraph counts don't match
    if len(text_para) != len(resp_para):
        st.warning("The translation might be misaligned due to paragraph structure differences.")
        col1, col2 = st.columns([1, 1])
        with col1:
            for para in text_para:
                st.write(para)
        with col2:
            for para in resp_para:
                st.write(para)
        return

    for i, para in enumerate(text_para):
        col1, col2 = st.columns([1, 1])
        with col1:
            st.write(para)
        with col2:
            st.write(resp_para[i])

def main():
    """Main function to run the Streamlit app."""
    st.set_page_config(
        page_title="GemTranslator ", 
        page_icon=":closed_book:",
        layout="wide") 

    # Use st.session_state more effectively
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        # Authentication form
        st.title("Authentication Required")
        col1, col2 = st.columns([1, 4])
        with col1:
            password_input = st.text_input("Enter Password", type="password")
            if st.button("Authenticate"):
                if password_input == PASSWORD:
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Incorrect password. Please try again.")

    else:
        col1, col2 = st.columns([1, 1])
        with col1:
            text = st.text_area("Input English text here")

        if st.button("Translate"):
            if text:
                show_paragraph(text)
            else:
                st.warning("Please input some text.")

if __name__ == "__main__":
    main()