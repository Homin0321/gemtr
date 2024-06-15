# Gemini Translator

This is a simple Streamlit web application that leverages Google's Gemini Pro model for English-Korean and Korean-English translation.

## Features

- **English to Korean Translation:** Input English text and get a Korean translation.
- **Korean to English Translation:** Input Korean text and get an English translation.
- **Side-by-Side Display:** View both the original and translated text in a clear, side-by-side format.
- **Password Protection:** Secure your application with password authentication.
- **Streamlit Framework:** Built using Streamlit for an interactive and user-friendly experience.

## Requirements

- Python 3.7 or higher
- Streamlit (`pip install streamlit`)
- Google `generativeai` library (`pip install google-generativeai`)

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/gemtranslator.git
   cd gemtranslator
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your secrets:**
   - Create a `secrets.toml` file in your application directory.
   - Add your Google Gemini API key and a password for authentication:
     ```toml
     api_key = "YOUR_GEMINI_API_KEY"
     passwd = "YOUR_PASSWORD"
     ```

4. **Run the app:**
   ```bash
   streamlit run app.py
   ```

## Usage

1. **Access the app:** Open your web browser and navigate to the address displayed in your terminal after running the app (usually `http://localhost:8501`).

2. **Authenticate:** Enter the password you set in the `secrets.toml` file.

3. **Translate:**
   - Paste or type your English or Korean text into the corresponding text area.
   - Click the "Translate" button below the text area.
   - The translated text will appear in the opposite text area, and both texts will be displayed side-by-side for easy comparison.

## Notes

- The translation quality may vary depending on the complexity and length of the text.
- This application is for demonstration purposes and can be further customized and enhanced.
- Ensure that you have a valid Google Gemini API key and have enabled the Gemini API in your Google Cloud Platform project.
- **Remember to replace the placeholders in the `secrets.toml` file with your actual API key and password.** 

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.

