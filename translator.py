import streamlit as st
import google.generativeai as genai
import time

COMMAND = "다음 영문을 설명이나 요약을 덧붙이지 말고 그대로 한국어로 번역해줘: "
SLEEP_TIME = 20

def configure_genai():
    """Configures the Gemini AI model with current settings."""
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


def show_paragraph(chat, text):
    col1, col2 = st.columns([1, 1])
    with col1:
        st.write(text)
    with col2:
        response = chat.send_message(COMMAND + text)
        st.write(response.text)

def main():
    # Main function to control the app flow
    st.set_page_config(page_title="Gemini Translator Eng2Kor", page_icon=":closed_book:")
    if "auth" not in st.session_state:
        form = st.form(key="auth")
        passwd = form.text_input("Enter Password")
        submit = form.form_submit_button("Submit")
        if submit:
            if passwd == st.secrets["passwd"]
                st.session_state.auth = "OK"
            st.rerun()

    genai.configure(api_key=st.secrets["api_key"])
    # Text input interface
    form = st.form(key="box")
    text = form.text_area("Input English text here")
    submit = form.form_submit_button("Translate into Korean")
    if submit:
        model = configure_genai()
        chat = model.start_chat()
        paragraphs = text.split('\n\n')
        for para in paragraphs:
            show_paragraph(chat, para)
            time.sleep(SLEEP_TIME)

if __name__ == "__main__":
    main()