import streamlit as st
import google.generativeai as genai
import time

# Constants for better readability and maintainability
COMMAND = "다음 영문을 설명이나 요약을 덧붙이지 말고 그대로 한국어로 번역해줘: "
PASSWORD = st.secrets["passwd"]  # Store password securely in secrets
API_KEY = st.secrets["api_key"]  # Store API key securely in secrets

def configure_genai():
    """Configures and returns the Gemini generative model."""
    safety = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ]
    model = genai.GenerativeModel(
        "gemini-1.5-pro-latest",
        generation_config=genai.types.GenerationConfig(temperature=1),
        safety_settings=safety,
    )
    return model

def show(text):
    """Displays text line by line in Streamlit."""
    for line in text.splitlines():
        st.write(line)

def show_paragraph(chat, text):
    """Displays English text and its Korean translation side-by-side."""
    col1, col2 = st.columns([1, 1])
    with col1:
        show(text)
    with col2:
        response = chat.send_message(COMMAND + text)
        show(response.text)

def get_length(text):
    """Returns the number of non-space characters in the text."""
    return len(text) - text.count(' ') - text.count('\n')

def main():
    """Main function to run the Streamlit app."""
    st.set_page_config(page_title="Gemini Translator Eng2Kor", page_icon=":closed_book:")

    # Use st.session_state more effectively
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        # Authentication form
        st.title("Authentication Required")
        password_input = st.text_input("Enter Password", type="password")
        if st.button("Authenticate"):
            if password_input == PASSWORD:
                st.session_state.authenticated = True
                genai.configure(api_key=API_KEY)
                st.rerun()  # More efficient than st.rerun()
            else:
                st.error("Incorrect password. Please try again.")
    else:
        text = st.text_area("Input English text here")
        if st.button("Translate"):
            model = configure_genai()
            chat = model.start_chat()
            paragraphs = text.split('\n\n')
            for i, para in enumerate(paragraphs):
                if get_length(para):
                    show_paragraph(chat, para)
                    if i > 0:
                        sleep = i*5 if i < 6 else 30
                        time.sleep(sleep)

if __name__ == "__main__":
    main()