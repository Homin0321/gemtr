# GemTr: An English-to-Korean Translation App using Google Gemini

This Streamlit application leverages the power of Google's Gemini Pro model to provide accurate and efficient English-to-Korean translations. 

## Features

- **Paragraph Translation:** Translate entire paragraphs of English text into Korean.
- **Side-by-Side Display:** View the original English text and its Korean translation conveniently arranged side-by-side.
- **Temperature Control:** Adjust the "temperature" parameter to control the creativity and randomness of the translation.
- **Password Protection:** Secure your application with password authentication to restrict access.
- **Streamlit Interface:** Enjoy a user-friendly and interactive translation experience within your web browser.

## Installation and Setup

1. **Prerequisites:** Ensure you have Python and pip installed on your system.
2. **Install Dependencies:** Install the required libraries using the following command:
   ```bash
   pip install streamlit google-generativeai
   ```
3. **Obtain API Key:**
   - Sign up for a Google Cloud Platform account and create a project.
   - Enable the "Gemini API" for your project.
   - Create an API key and store it securely.
4. **Store Credentials:**
   - Create a `secrets.toml` file in the same directory as your Python script.
   - Add your API key and desired password to the `secrets.toml` file in the following format:
     ```toml
     api_key = "YOUR_API_KEY_HERE"
     passwd = "YOUR_PASSWORD_HERE"
     ```
5. **Run the App:** Execute the following command in your terminal to launch the Streamlit app:
   ```bash
   streamlit run translator.py
   ```

## Usage

1. **Authentication:** Upon launching the app, you'll be prompted to enter the password you set in the `secrets.toml` file.
2. **Input Text:** Enter the English text you want to translate into the provided text area.
3. **Adjust Temperature (Optional):** Use the slider to modify the temperature parameter. Higher values (closer to 1.0) result in more creative and less predictable translations.
4. **Translate:** Click the "Translate" button to initiate the translation process.
5. **View Translation:** The translated Korean text will be displayed alongside the original English text.

## Notes

- The application utilizes the `gemini-1.5-pro-latest` model for translation.
- Ensure that you have an active internet connection for the app to function correctly.
- The quality of the translation may vary depending on the complexity and clarity of the input text.

## Disclaimer

This application is provided as-is and is intended for educational and demonstration purposes only. The developers are not responsible for any consequences arising from its use.

## License

This project is licensed under the MIT License.