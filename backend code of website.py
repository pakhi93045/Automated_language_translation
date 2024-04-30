import streamlit as st
import speech_recognition
from gtts import gTTS
from googletrans import Translator
import googletrans

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

# Text to Voice Conversion Function
def text_to_voice(text, target_language):
    translator = Translator()
    translation = translator.translate(text, dest=target_language)
    gtts_language_code = translation.src  # Source language code
    tts_translation = gTTS(text=translation.text, lang=gtts_language_code)
    tts_translation.save("text_to_voice_output.mp3")
    st.audio("text_to_voice_output.mp3", format='audio/mp3')

# Main Streamlit App
def main():
    st.title("Automated Language Translation")

    conversion_options = ["Text to Text", "Voice to Text", "Voice to Voice", "Text to Voice"]  # Add "Text to Voice" option
    option = st.selectbox("Select Conversion Type:", conversion_options)

    target_language = st.selectbox("Select Target Language:", list(googletrans.LANGUAGES.values()))

    if option == "Text to Text":
        input_text = st.text_area("Enter text:")
        if st.button("Translate"):
            translator = Translator()
            translation = translator.translate(input_text, dest=target_language)
            st.write("Translated Text:", translation.text)
    
    elif option == "Voice to Text":
        if st.button("Speak now"):
            voice_to_text(target_language)
    
    elif option == "Voice to Voice":
        if st.button("Speak now"):
            voice_to_voice(target_language)
    
    elif option == "Text to Voice":
        input_text = st.text_area("Enter text:")
        if st.button("Convert to Voice"):
            text_to_voice(input_text, target_language)

if __name__ == "__main__":
    main()
