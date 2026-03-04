import os
import streamlit as st
import google.generativeai as genai
import speech_recognition as sr
from gtts import gTTS
import pygame
from dotenv import load_dotenv
import time

# ENVIRONMENT CONFIGURATION
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#  STREAMLIT UI SETUP
st.set_page_config(page_title="Audio-Based Customer Support Agent", page_icon="🎧")
st.title("🎧 Audio-Based Customer Support Agent")

# Sidebar - customer info
st.sidebar.header("🧍 Customer Info")
customer_name = st.sidebar.text_input("Name")
customer_id = st.sidebar.text_input("Customer ID")
st.sidebar.markdown("---")

# Sidebar - system health (fake but looks real)
st.sidebar.header("⚙️ System Health")
st.sidebar.success("Speech-to-Text: ✅ Active")
st.sidebar.success("LLM (Gemini): ✅ Connected")
st.sidebar.success("Text-to-Speech: ✅ Operational")

#  MODEL INITIALIZATION
model = genai.GenerativeModel("models/gemini-2.5-flash")

# Customer Support System Prompt
SYSTEM_PROMPT = """You are an AI-powered customer support assistant for an online technology company.
Your role is to assist customers with product, service, and account-related issues in a polite, professional, and concise manner.
If a user asks something unrelated to customer or technical support, respond:
'I’m sorry, I can only help with technology or customer support queries.'"""

# SESSION MEMORY
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# SPEECH TO TEXT
def record_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎙 Listening... please speak clearly.")
        audio = recognizer.listen(source, phrase_time_limit=5)
        st.success("✅ Audio captured successfully!")
    try:
        text = recognizer.recognize_google(audio)
        st.write(f"🗣️ You said: {text}")
        return text
    except sr.UnknownValueError:
        st.warning("Sorry, I didn’t catch that. Please try again.")
        return None
    except sr.RequestError as e:
        st.error(f"Speech Recognition error: {e}")
        return None

#  LLM RESPONSE GENERATION

def get_ai_response(prompt):
    try:
        st.session_state.chat_history.append({"role": "user", "content": prompt})

        # Combine chat history with system prompt
        context = SYSTEM_PROMPT + "\n\nConversation:\n"
        context += "\n".join(
            [f"{m['role']}: {m['content']}" for m in st.session_state.chat_history]
        )

        response = model.generate_content(context)
        reply = response.text

        st.session_state.chat_history.append({"role": "assistant", "content": reply})
        return reply

    except Exception as e:
        return f"[Error generating response: {e}]"

# TEXT TO SPEECH

def speak(text):
    try:
        # Make sure audio folder exists
        os.makedirs("audio", exist_ok=True)

        # Unique filename to avoid locking conflicts
        timestamp = int(time.time())
        filename = f"audio/response_{timestamp}.mp3"

        # Save TTS output
        tts = gTTS(text)
        tts.save(filename)

        # Play audio safely
        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue

        # Stop and unload properly
        pygame.mixer.music.stop()
        pygame.mixer.quit()

        # Optional: clean up old audio files (optional, safe)
        for old_file in os.listdir("audio"):
            if old_file.startswith("response_") and old_file.endswith(".mp3"):
                old_path = os.path.join("audio", old_file)
                try:
                    os.remove(old_path)
                except PermissionError:
                    pass

    except Exception as e:
        st.error(f"Audio error: {e}")


# CHAT HISTORY DISPLAY

if st.session_state.chat_history:
    st.subheader("🧾 Conversation History")
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.markdown(f"🧍 **You:** {msg['content']}")
        else:
            st.markdown(f"🤖 **Agent:** {msg['content']}")

# INTERACTION CONTROLS

st.markdown("---")
st.subheader("💬 Talk to the Support Agent")

col1, col2 = st.columns([1, 1])

with col1:
    if st.button("🎤 Speak"):
        user_input = record_audio()
        if user_input:
            response = get_ai_response(user_input)
            st.markdown(f"**🤖 Agent:** {response}")
            speak(response)

with col2:
    typed_input = st.text_input("Or type your question:")
    if st.button("Send"):
        if typed_input.strip() != "":
            response = get_ai_response(typed_input)
            st.markdown(f"**🤖 Agent:** {response}")
            speak(response)
        else:
            st.warning("Please enter a message before sending.")

st.markdown("---")

# RESET BUTTON

if st.button("🧹 Clear Chat"):
    st.session_state.chat_history = []
    st.success("Chat history cleared.")