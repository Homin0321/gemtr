import streamlit as st
import google.generativeai as genai
import re

# Constants for better readability and maintainability
COMMAND = "다음 영문을 한국어로 번역해줘. 문장 번역 외에 제목이나 설명, 요약은 하지 말고: \n"
PASSWORD = st.secrets["passwd"]  # Store password securely in secrets
API_KEY = st.secrets["api_key"]  # Store API key securely in secrets

# Configure Gemini only once
@st.cache_resource 
def configure_genai(temperature):
    genai.configure(api_key=API_KEY)
    return genai.GenerativeModel(
        "gemini-1.5-pro-latest",
        generation_config=genai.types.GenerationConfig(temperature=temperature),
        safety_settings=[
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ],
    )

def show(text):
    """Removes markdown formatting from text and displays it."""
    text = re.sub(r"#{1,6} |(\*\*|__)|\*|_", "", text)
    st.write(text)

def show_paragraph(model, text):
    """Displays English text and its Korean translation side-by-side."""
    response = model.generate_content(COMMAND + text)

    engs = text.split('\n')
    kors = response.text.split('\n')
    len_eng = len(engs)
    len_kor = len(kors)
    length = max(len_eng, len_kor)
    for i in range(length):
        col1, col2 = st.columns([1, 1])
        with col1:
            if i < len_eng:
                show(engs[i])
        with col2:
            if i < len_kor:
                show(kors[i])

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
            temperature = st.slider("Temperature", 0.0, 1.0, 0.5)

        if st.button("Translate"):
            model = configure_genai(temperature)

            if text:
                show_paragraph(model, text)
            else:
                st.warning("Please input some text.")

if __name__ == "__main__":
    main()