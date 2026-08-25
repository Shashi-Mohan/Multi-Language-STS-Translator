import os
import numpy as np
import streamlit as st
# import gradio as gr
import assemblyai as aai
from translate import Translator
import uuid
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from pathlib import Path


def voice_to_voice(audio_file):

    # transcript speech
    transcript = transcribe_audio(tmp_path)
    st.write(f"Transcript status: {transcript.status}")  # Debug: Show status
    st.write(f"Transcript text: {transcript.text}")  # Debug: Show transcribed text
    st.write(f"Transcript error (if any): {transcript.error}")  # Debug: Show errors
    if transcript.status == aai.TranscriptStatus.error:
            st.error(transcript.error)
            return None, None
    else:
            transcript_text = transcript.text

    # translate text
    list_translations = translate_text(transcript)
    generated_audio_paths = []

    # generate speech from text
    for translation in list_translations:
        translated_audio_file_name = text_to_speech(translation)
        path = Path(translated_audio_file_name)
        generated_audio_paths.append(path)


    return generated_audio_paths[0], generated_audio_paths[1], generated_audio_paths[2], generated_audio_paths[3], generated_audio_paths[4], generated_audio_paths[5], list_translations[0], list_translations[1], list_translations[2], list_translations[3], list_translations[4], list_translations[5]

# Function to transcribe audio using AssemblyAI
def transcribe_audio(audio_file):
    aai.settings.api_key = "0601dc77fb1a74e8ca239a8fe00a5952"

    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_file)

    return transcript

    
# Function to translate text
def translate_text(text: str) -> str:

    languages = ["ru", "tr", "sv", "de", "es", "ja"]
    list_translations = []

    for lan in languages:
        translator = Translator(from_lang="en", to_lang=lan)
        translation = translator.translate(text)
        list_translations.append(translation)

    return list_translations

# Function to generate speech
def text_to_speech(text: str) -> str:

    # ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
    client = ElevenLabs(
        api_key="sk_3bdc6c5233b287809eeecf6e7c8caad0576a4f132ff2b229",
    )

    # Calling the text_to_speech conversion API with detailed parameters
    response = client.text_to_speech.convert(
        voice_id="V6mpzZ1krBodIBG8UCB7",  # Clone your voice on ElevenLabs dashboard and copy the ID
        optimize_streaming_latency="0",
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_multilingual_v2", # use the turbo model for low latency, for other languages use the `eleven_multilingual_v2`
        voice_settings=VoiceSettings(
            stability=0.5,
            similarity_boost=0.8,
            style=0.5,
            use_speaker_boost=True,
        ),
    )

    save_file_path = f"{uuid.uuid4()}.mp3"

    # Writing the audio to a file
    with open(save_file_path, "wb") as f:
        for chunk in response:
            if chunk:
                f.write(chunk)

    print(f"{save_file_path}: A new audio file was saved successfully!")

    # Return the path of the saved audio file
    return save_file_path

# Streamlit app
st.title("Voice to Voice Translation")
st.markdown("Record yourself in English and upload the audio file to receive voice translations.")

audio_file = st.file_uploader("Upload an audio file (e.g., WAV, MP3)", type=["wav", "mp3", "m4a"])

if st.button("Submit") and audio_file is not None:
    with st.spinner("Processing..."):
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            temp_file.write(audio_file.read())
            temp_audio_path = temp_file.name
        
        # Process the audio
        result = voice_to_voice(temp_audio_path)
        
        if result:
            generated_audio_paths, list_translations = result
        
            # Languages and their labels
            languages = ["Russian", "Turkish", "Swedish", "German", "Spanish", "Japanese"]
            audio_paths = generated_audio_paths
            texts = list_translations
        
            # Display in two rows of three columns each
            col1, col2, col3 = st.columns(3)
            with col1:
                st.subheader(languages[0])
                st.audio(str(audio_paths[0]))
                st.markdown(f"**Text:** {texts[0]}")
            with col2:
                st.subheader(languages[1])
                st.audio(str(audio_paths[1]))
                st.markdown(f"**Text:** {texts[1]}")
            with col3:
                st.subheader(languages[2])
                st.audio(str(audio_paths[2]))
                st.markdown(f"**Text:** {texts[2]}")
            col4, col5, col6 = st.columns(3)
            with col4:
                st.subheader(languages[3])
                st.audio(str(audio_paths[3]))
                st.markdown(f"**Text:** {texts[3]}")
            with col5:
                st.subheader(languages[4])
                st.audio(str(audio_paths[4]))
                st.markdown(f"**Text:** {texts[4]}")
            with col6:
                st.subheader(languages[5])
                st.audio(str(audio_paths[5]))
                st.markdown(f"**Text:** {texts[5]}")
        