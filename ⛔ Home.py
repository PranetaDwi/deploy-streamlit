import streamlit as st

st.set_page_config(page_title="Voice Recorder", page_icon="👋")

import streamlit as st
import speech_recognition as sr
import time

st.title("Pengenalan Perintah Suara")

recognizer = sr.Recognizer()
microphone = sr.Microphone()

# Inisialisasi session state jika belum ada
if "recording" not in st.session_state:
    st.session_state["recording"] = True  # Default mulai merekam
if "command_text" not in st.session_state:
    st.session_state["command_text"] = None

# Fungsi untuk merekam suara
def record_audio():
    with microphone as source:
        st.write("Silakan berbicara...")
        recognizer.adjust_for_ambient_noise(source)  # Mengatasi noise
        audio_data = recognizer.listen(source)

    try:
        command_text = recognizer.recognize_google(audio_data, language="id-ID")
        st.session_state["command_text"] = command_text
        if command_text.lower() == "berhenti":
            st.session_state["recording"] = False  # Set recording ke False
        st.success(f"Perintah yang dikenali: {command_text}")

    except sr.UnknownValueError:
        st.warning("Maaf, tidak dapat mengenali suara.")
    except sr.RequestError:
        st.error("Gagal terhubung ke layanan Speech Recognition.")

    time.sleep(0.5)  # Jeda sejenak sebelum rekaman berikutnya
    st.rerun()  # Jalankan ulang aplikasi

# Proses rekaman jika recording aktif
if st.session_state["recording"]:
    record_audio()
else:
    st.write("Recording dihentikan. Tekan tombol di bawah untuk mulai lagi.")
    if st.button("Mulai Rekaman Lagi"):
        st.session_state["recording"] = True
        st.rerun()  # Jalankan ulang aplikasi agar rekaman dimulai
