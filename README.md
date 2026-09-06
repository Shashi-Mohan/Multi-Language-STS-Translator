AI-Based Voice Translation System

An AI-powered speech-to-speech translation application that takes an English audio file, converts the speech into text, translates the text into multiple languages, and then generates natural-sounding voice output for each translated language.
The project combines three main AI stages:
Speech-to-Text (ASR) → Machine Translation (MT) → Text-to-Speech (TTS)
It is implemented in Python with a Streamlit web interface. The project uses AssemblyAI for speech recognition, a translation service for multilingual text conversion, and ElevenLabs for multilingual voice generation. The project report describes support for Russian, Hindi, Swedish, German, Spanish, and Japanese.

📌 What This Project Does
The main purpose of this project is to make multilingual communication easier by converting spoken English into translated text and spoken audio.
For example:
Input: English audio — "Good morning, everyone. My name is Shashi Mohan."
The system:
1. Receives the English audio file.
2. Transcribes the spoken English into text.
3. Translates the English text into multiple target languages.
4. Converts every translated sentence into natural-sounding speech.
5. Shows the translated text and provides audio playback through the Streamlit interface.

The overall pipeline is:
"""
English Audio
      ↓
Speech-to-Text
      ↓
English Transcript
      ↓
Machine Translation
      ↓
Multilingual Text
      ↓
Text-to-Speech
      ↓
Multilingual Audio Output
"""
🧩 What Is Needed
To run this project, the following technologies and services are required.
Component             Used For
Python                Main programming language
Streamlit             Web application / user interface
AssemblyAI            English Speech-to-Text / transcription                 
Translation           Translation from English into target languages
API / library 
ElevenLabs            Text-to-Speech and natural voice generation
tempfile              Temporary handling of uploaded audio
pathlib               File and path management
uuid                  Creating unique names for generated audio files
os                    File-system operations
VS Code               Development environment used in the project

🤖 AI Services Used

1. AssemblyAI — Speech-to-Text
AssemblyAI is used for Automatic Speech Recognition (ASR).
The uploaded English audio is sent to AssemblyAI, which returns an English transcript.
   English Audio
        ↓
   AssemblyAI
        ↓
   English Text
The project uses the AssemblyAI transcription result as the input for the translation stage.

2. Translation — Machine Translation
The English transcript is passed to the translation stage.
The project documentation describes the use of Google Translate for converting the English transcript into multiple languages.
   English Transcript
           ↓
   Translation Service
           ↓
        Russian
        Hindi
        Swedish
        German
        Spanish
        Japanese
The Python implementation uses the translate library:
from translate import Translator
The translator is configured using a source language of English and a target-language code.
Example: translator = Translator(from_lang="en", to_lang="de")

3. ElevenLabs — Text-to-Speech
After translation, every translated sentence is sent to ElevenLabs.
ElevenLabs converts the translated text into audio using its multilingual TTS model.
The project uses:
eleven_multilingual_v2
The generated audio is saved as an MP3 file with a unique filename.
Translated Text
      ↓
ElevenLabs
      ↓
Multilingual Speech
      ↓
MP3 Audio
The project also configures voice characteristics such as:
Stability
Similarity boost
Style
Speaker boost

🌍 Language Codes

The language codes used by the project follow standard two-letter language identifiers.

Code                   Language              Used For

en                     English               Source language

ru                     Russian               Russian translation

hi                     Hindi                 Hindi translation

sv                     Swedish               Swedish translation

de                     German                German translation

es                     Spanish               Spanish translation

ja                     Japanese              Japanese translation

Examples
en → ru    English → Russian
en → hi    English → Hindi
en → sv    English → Swedish
en → de    English → German
en → es    English → Spanish
en → ja    English → Japanese

⚠️ Important implementation note
The project report/presentation describes the target languages as:
Russian, Hindi, Swedish, German, Spanish, Japanese
However, the currently provided voice_translator.py contains:
languages = ["ru", "tr", "sv", "de", "es", "ja"]
Here, tr means Turkish, not Hindi.
Therefore, if the intended final project is the Hindi version documented in the report, the implementation should use:
languages = ["ru", "hi", "sv", "de", "es", "ja"]
This README follows the language list documented in the project report while explicitly noting the difference in the currently supplied Python file.
🔄 Complete System Workflow

The system works in the following stages:

┌──────────────────────────┐
│      User Input          │
│  English Audio File      │
│   WAV / MP3 / M4A        │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│    Streamlit Interface   │
│       File Upload        │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│     Temporary Storage    │
│       tempfile           │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│    Speech-to-Text (ASR) │
│        AssemblyAI        │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│    English Transcript    │
│        Text Output       │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│    Machine Translation   │
│   Translation Service    │
└────────────┬─────────────┘
             │
      ┌──────┼──────┬──────┬──────┬──────┐
      ▼      ▼      ▼      ▼      ▼      ▼
     RU     HI     SV     DE     ES     JA
      │      │      │      │      │      │
      └──────┴──────┴──────┴──────┴──────┘
             │
             ▼
┌──────────────────────────┐
│      ElevenLabs TTS      │
│  eleven_multilingual_v2  │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│   Generated MP3 Audio    │
│   for each language      │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│     Streamlit Output     │
│                          │
│  Translated Text + Audio │
│  Playback / Download     │
└──────────────────────────┘

🏗️ How the Code Works

1. Importing the Required Libraries
The application imports Python libraries and external packages:

import os
import numpy as np
import streamlit as st
import assemblyai as aai
from translate import Translator
import uuid
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from pathlib import Path

These libraries provide the application's UI, speech recognition, translation, voice generation, and file-management functionality.

2. Uploading the Audio
The Streamlit application accepts:
.wav

.mp3

.m4a

The interface provides an upload area where the user selects the English audio file.
audio_file = st.file_uploader(
    "Upload an audio file (e.g., WAV, MP3, M4A)",
    type=["wav", "mp3", "m4a"]
)

3. Temporary Audio File
The uploaded audio is temporarily stored using Python's tempfile functionality.
This allows the audio to be passed to the processing pipeline without permanently storing the original upload.

4. Speech-to-Text
The transcribe_audio() function sends the uploaded audio to AssemblyAI.
Conceptually:
Audio File
    ↓
AssemblyAI Transcriber
    ↓
Transcript
The resulting transcript is then passed to the translation stage.

5. Translation
The translate_text() function loops through the target languages.
Conceptually:
for language in languages:
    translator = Translator(
        from_lang="en",
        to_lang=language
    )
    
Each translated result is stored in a list.
The result is therefore a collection of translated texts:
Russian Text
Hindi Text
Swedish Text
German Text
Spanish Text
Japanese Text

6. Text-to-Speech
The text_to_speech() function sends each translated sentence to ElevenLabs.
The project uses the multilingual model:
eleven_multilingual_v2
The generated audio is returned as a response and written to an MP3 file.
A UUID is used to create a unique filename:
save_file_path = f"{uuid.uuid4()}.mp3"
This prevents generated audio files from accidentally using the same filename.

7. Output Generation
The application displays each language in the Streamlit interface.
For every language, the user can see:
Language name
Translated text
Audio player
The interface is arranged into two rows of three language outputs.

┌────────────┬────────────┬────────────┐
│  Russian   │   Hindi    │  Swedish   │
│   Text     │    Text    │   Text     │
│   Audio    │    Audio   │   Audio    │
└────────────┴────────────┴────────────┘

┌────────────┬────────────┬────────────┐
│   German   │   Spanish  │  Japanese  │
│   Text     │    Text    │    Text    │
│   Audio    │    Audio   │    Audio   │
└────────────┴────────────┴────────────┘

🧠 Main Functions

The application is organized around three major processing functions.
voice_to_voice()
Controls the complete pipeline:
Audio
  ↓
Transcription
  ↓
Translation
  ↓
Speech Generation
  ↓
Output
transcribe_audio()
Handles speech recognition through AssemblyAI.
Audio → AssemblyAI → English Transcript
translate_text()
Handles multilingual text translation.
English Text
   ↓
Translation
   ↓
RU / HI / SV / DE / ES / JA
text_to_speech()
Generates speech using ElevenLabs.
Translated Text
   ↓
ElevenLabs
   ↓
MP3 Audio

📁 Project Structure
A simple repository structure can be:
AI-Based-Voice-Translation-System/
│
├── voice_translator.py
├── requirements.txt
├── .gitignore
├── README.md
└── generated_audio/
If generated audio is stored temporarily during execution, it should normally not be committed to the repository.

⚙️ Installation
1. Clone the Repository
git clone <your-repository-url>
cd AI-Based-Voice-Translation-System

2. Create a Virtual Environment
python -m venv venv
Windows
venv\Scripts\activate
macOS / Linux
source venv/bin/activate

4. Install Dependencies
Create a requirements.txt file containing the packages required by the application.
Example:
streamlit
numpy
assemblyai
translate
elevenlabs
Then install them: pip install -r requirements.txt

🔐 API Keys
The project requires API access for the AI services.
You should never put API keys directly inside the Python source code or commit them to GitHub.
Use environment variables or Streamlit secrets instead.
For example:
import os
ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
Then configure the keys in your local environment.
Security: If API keys have previously been placed directly in source code, revoke/rotate those keys before publishing the repository.

▶️ Running the Application
Start the Streamlit application with:
streamlit run voice_translator.py
Streamlit will provide a local web address.
Open that address in a browser and upload an English audio file.

🎙️ Supported Input
The application accepts:
.wav
.mp3
.m4a
The intended input is spoken English audio.

📤 Output
The application produces:
English
Original transcription
Translated Languages
Russian (ru)
Hindi (hi)
Swedish (sv)
German (de)
Spanish (es)
Japanese (ja)
For each target language, the application provides:

Translated Text
       +
Generated Audio

The generated audio is stored in MP3 format.

📊 Example

Input
Good morning, everyone. My name is Shashi Mohan.
Transcription
Good morning, everyone. My name is Shashi Mohan.
Translation
Russian   → Доброе утро всем, меня зовут Шаши Мохан.
Hindi     → सुप्रभात, मेरा नाम शशि मोहन है।
Swedish   → God morgon allihopa, jag heter Shashi Mohan.
German    → Guten Morgen zusammen, mein Name ist Shashi Mohan.
Spanish   → Buenos días a todos, mi nombre es Shashi Mohan.
Japanese  → おはようございます、皆さん。私の名前はシャシ・モハンです。
The translated text is then converted into corresponding voice outputs using ElevenLabs.

📈 Results
According to the project evaluation, the system demonstrated:
Accurate transcription for clear English speech
Reliable translation for short/general-purpose sentences
Natural and smooth TTS output
An intuitive Streamlit interface
Multilingual text and audio output
Processing time dependent on audio length and network speed
The project report records approximately 95% transcription accuracy for clear English speech in its evaluation, while noting that translation quality can vary for longer or complex phrases.

🔬 Limitations
The project has some practical limitations:
Translation quality can vary for context-specific and idiomatic expressions.
Processing depends on external APIs and network connectivity.
The current system is based on uploaded audio rather than continuous live speech.
The number of supported languages is currently limited.
Offline/on-device processing is not implemented.

🚀 Future Scope
The project can be extended by:

🌍 Adding more regional and low-resource languages

🎙️ Adding real-time recording

⚡ Supporting live voice translation

📴 Implementing offline/on-device AI models

🧠 Improving context-aware translation

📱 Developing a mobile application

🎯 Improving translation quality for complex and idiomatic speech

🛠️ Technology Stack

Programming Language
        │
        ▼
      Python
        │
        ▼
   Streamlit UI
        │
        ▼
 ┌───────────────┐
 │ Audio Upload  │
 └───────┬───────┘
         │
         ▼
    AssemblyAI
   Speech-to-Text
         │
         ▼
 English Transcript
         │
         ▼
 Translation Service
         │
         ▼
 RU / HI / SV / DE / ES / JA
         │
         ▼
     ElevenLabs
      TTS Model
         │
         ▼
   Multilingual MP3
         │
         ▼
   Streamlit Output

📚 References

The project report references documentation and learning resources from:

AssemblyAI — Speech-to-Text API

ElevenLabs — Text-to-Speech API

Google Translate / Google Cloud Translation

Streamlit

Speech and Language Processing — Daniel Jurafsky and James H. Martin

Attention Is All You Need — Vaswani et al.

Deep Learning — Goodfellow, Bengio, and Courville

👨‍💻 Project

AI-Based Voice Translation System

Developed as a B.Tech Computer Science & Engineering project at University of Engineering & Management, Jaipur.

Developer: Shashi Mohan

Supervisor: Prof. Soumen Sarkar

⭐ Project Summary

This project demonstrates how Automatic Speech Recognition, Machine Translation, and Text-to-Speech can be integrated into a single application.

Instead of translating only text, the system creates a complete audio-to-audio pipeline:

🎙️ English Speech
      ↓
📝 Speech Recognition
      ↓
🌍 Translation
      ↓
🔊 Voice Generation
      ↓
🎧 Multilingual Speech

The goal is to provide a simple and accessible way to bridge language barriers using modern AI technologies.
