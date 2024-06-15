import streamlit as st
import google.generativeai as genai
import re

# Constants for better readability and maintainability
TEMPERATURE = 0.5
COMMAND_ENG_TO_KOR = "다음 영문을 한국어로 번역해줘. 문장 번역 외에 제목이나 설명, 요약은 하지 말고: \n"
COMMAND_KOR_TO_ENG = "다음 한국어 문장을 영어로 번역해줘. 문장 번역 외에 제목이나 설명, 요약은 하지 말고: \n"
PASSWORD = st.secrets["passwd"]  # Store password securely in secrets
API_KEY = st.secrets["api_key"]  # Store API key securely in secrets

# Configure Gemini only once
@st.cache_resource 
def configure_genai():
    genai.configure(api_key=API_KEY)
    return genai.GenerativeModel(
        "gemini-1.5-pro-latest",
        generation_config=genai.types.GenerationConfig(temperature=TEMPERATURE),
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

def translate(model, text, command):
    response = model.generate_content(command + text)
    return response.text

def show_paragraph(left_text, right_text):
    """Displays english text in left and korean text in right."""
    left_text = left_text.split('\n')
    right_text = right_text.split('\n')
    len_left = len(left_text)
    len_right = len(right_text)
    length = max(len_left, len_right)
    for i in range(length):
        col1, col2 = st.columns([1, 1])
        with col1:
            if i < len_left:
                show(left_text[i])
        with col2:
            if i < len_right:
                show(right_text[i])

def main():
    """Main function to run the Streamlit app."""
    st.set_page_config(
        page_title="GemTranslator", 
        page_icon=":closed_book:",
        layout="wide"
    )

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
        model = configure_genai()
        st.title("Gemini Translator :closed_book:")
        if st.button("Clear Screen"):
            st.session_state.eng_text = ""
            st.session_state.kor_text = ""

        col1, col2 = st.columns([1, 1])

        # English to Korean Form
        with col1:
            st.subheader("English to Korean")
            with st.form(key="eng_to_kor_form"):
                eng_text = st.text_area("Input English text here", value=st.session_state.get("eng_text", ""))
                submit_eng_to_kor = st.form_submit_button("Translate into Korean")
                if submit_eng_to_kor:
                    if eng_text:
                        st.session_state.kor_text = translate(model, eng_text, COMMAND_ENG_TO_KOR)
                        st.session_state.eng_text = eng_text
                    else:
                        st.warning("Please input some text.")

        # Korean to English Form
        with col2:
            st.subheader("Korean to English")
            with st.form(key="kor_to_eng_form"):
                kor_text = st.text_area("Input Korean text here", value=st.session_state.get("kor_text", ""))
                submit_kor_to_eng = st.form_submit_button("Translate into English")
                if submit_kor_to_eng:
                    if kor_text:
                        st.session_state.eng_text = translate(model, kor_text, COMMAND_KOR_TO_ENG)
                        st.session_state.kor_text = kor_text
                    else:
                        st.warning("Please input some text.")

        # Display translations if available
        if st.session_state.get("kor_text") and st.session_state.get("eng_text"):
            show_paragraph(st.session_state.eng_text, st.session_state.kor_text)

if __name__ == "__main__":
    main()
