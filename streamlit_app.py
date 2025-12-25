import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import os

# 1. Setup the Page
st.title("📖 Dastaan: Your Urdu Audio Bridge")
st.write("Upload your book pages, and I'll read them to your friend!")

# 2. Securely add your API Key
api_key = st.sidebar.text_input("Paste your Gemini API Key here:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('models/gemini-1.5-pro')

    # 3. File Uploader
    uploaded_files = st.file_uploader("Upload Urdu Pages (Images/PDF)", accept_multiple_files=True)

    if st.button("Generate Chapter Audio"):
        if uploaded_files:
            with st.spinner("Gemini is reading the pages..."):
                # Feed images to Gemini
                content = ["Transcribe this Urdu text into one continuous story:"]
                for uploaded_file in uploaded_files:
                    bytes_data = uploaded_file.getvalue()
                    content.append({"mime_type": "image/jpeg", "data": bytes_data})
                
                # Get response
                response = model.generate_content(content)
                urdu_text = response.text
                st.subheader("Transcribed Text:")
                st.write(urdu_text)

                # 4. Convert to Audio (Using Google TTS)
                with st.spinner("Converting to Audio..."):
                    tts = gTTS(text=urdu_text, lang='ur')
                    tts.save("chapter.mp3")
                    
                    # 5. Play the Audio
                    audio_file = open("chapter.mp3", 'rb')
                    audio_bytes = audio_file.read()
                    st.audio(audio_bytes, format='audio/mp3')
                    st.success("Done! Your friend can now listen.")
        else:
            st.error("Please upload some files first!")
