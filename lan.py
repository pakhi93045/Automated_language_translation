import streamlit as st
import speech_recognition
from gtts import gTTS
from googletrans import Translator
import googletrans
from langdetect import detect
from langcodes import Language
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# Text to Text Conversion Functions
def preprocess_text(text):
    tokens = word_tokenize(text.lower())
    cleaned_tokens = [token for token in tokens if token.isalpha() and token not in stopwords.words('english')]
    cleaned_text = ' '.join(cleaned_tokens)
    return cleaned_text

def detect_language_and_name(text):
    try:
        preprocessed_text = preprocess_text(text)
        language_code = detect(preprocessed_text)
        language_name = Language.get(language_code).language_name('en')
        return language_name
    except Exception as e:
        st.error(f"Error: {e}")
        return None

# Voice to Text Conversion Functions
def voice_to_text(target_language):
    recognizer = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        st.write("Speak now")
        voice = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(voice, language='en-US')  # Recognize speech in English
            st.write("You said:", text)

            translator = googletrans.Translator()
            translation = translator.translate(text, dest=target_language)
            st.write("Translation:", translation.text)
            return translation.text
        except speech_recognition.UnknownValueError:
            st.error("Sorry, could not understand audio.")
            return None
        except speech_recognition.RequestError as e:
            st.error("Error:", e)
            return None

# Voice to Voice Conversion Function
def voice_to_voice(target_language):
    recognizer = speech_recognition.Recognizer()
    with speech_recognition.Microphone() as source:
        st.write("Speak now")
        voice = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(voice, language='en')  # Recognize speech in English
            st.write("You said:", text)

            translator = Translator()
            translation = translator.translate(text, dest=target_language)
            st.write("Translation:", translation.text)

            # Get the corresponding gTTS language code
            gtts_language_code = translation.src  # Source language code
            tts_translation = gTTS(text=translation.text, lang=gtts_language_code)
            tts_translation.save("translated_output.mp3")

            # Play the translated text
            st.audio("translated_output.mp3", format='audio/mp3')
        except speech_recognition.UnknownValueError:
            st.error("Sorry, could not understand audio.")
        except speech_recognition.RequestError as e:
            st.error("Error:", e)

# Main Streamlit App
def main():
    st.title("Automated Language Translation")

    conversion_options = ["Text to Text", "Voice to Text", "Voice to Voice"]  # Add "Voice to Voice" option
    option = st.selectbox("Select Conversion Type:", conversion_options)

    target_language = st.selectbox("Select Target Language:", list(googletrans.LANGUAGES.values()))

    if option == "Text to Text":
        input_text = st.text_area("Enter text:")
        if st.button("Translate"):
            detected_language = detect_language_and_name(input_text)
            st.write("Detected Language:", detected_language)
            translator = Translator()
            translation = translator.translate(input_text, dest=target_language)
            st.write("Translated Text:", translation.text)
    
    elif option == "Voice to Text":
        if st.button("Speak now"):
            voice_to_text(target_language)
    
    elif option == "Voice to Voice":
        if st.button("Speak now"):
            voice_to_voice(target_language)

if __name__ == "__main__":
    main()
