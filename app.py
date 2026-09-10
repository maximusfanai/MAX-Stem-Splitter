import base64
import os
import random
import time
from pathlib import Path
import librosa
import numpy as np
import soundfile as sf

import streamlit as st
import streamlit.components.v1 as components

# --- TORCH & HUGGINGFACE PATHS ---
os.environ['TORCH_HOME'] = 'E:/StemSplitterProject/cache/torch'
os.environ['HF_HOME'] = 'E:/StemSplitterProject/cache/huggingface'
os.environ['HUGGINGFACE_HUB_CACHE'] = 'E:/StemSplitterProject/cache/huggingface/hub'

st.set_page_config(
    page_title="MAX Stem Splitter & Auth",
    page_icon="🎛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- SESSION STATES INITIALIZATION ---
if "splash_done" not in st.session_state:
    st.session_state.splash_done = False

if "page_mode" not in st.session_state:
    st.session_state.page_mode = "signin"

if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None

if "split_done" not in st.session_state:
    st.session_state.split_done = False
if "stems_paths" not in st.session_state:
    st.session_state.stems_paths = {}
if "selected_quality" not in st.session_state:
    st.session_state.selected_quality = "Normal"
if "saved_output_format" not in st.session_state:
    st.session_state.saved_output_format = "WAV (Lossless)"


# --- 1. SPLASH SCREEN LOGIC ---
if not st.session_state.splash_done:
    st.markdown(
        """
    <style>
        .stApp { background-color: #000000 !important; }
        [data-testid="collapsedControl"] { display: none !important; }
        section[data-testid="stSidebar"] { display: none !important; }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        .splash-container {
            display: flex;
            justify-content: center;
            align-items: flex-start;
            height: 85vh;
            width: 100%;
            overflow: hidden;
        }
        .splash-image {
            animation: fadeIn 6s ease-in;
            width: 102%;
            height: 102%;
            object-fit: cover;
            margin-top: -60px;
        }
    </style>
    """,
        unsafe_allow_html=True,
    )

    splash_path = r"E:\StemSplitterProject\assets\splash.png"

    if os.path.exists(splash_path):
        with open(splash_path, "rb") as f:
            encoded_img = base64.b64encode(f.read()).decode()

        st.markdown(
            f"""
            <div class="splash-container">
                <img src="data:image/png;base64,{encoded_img}" class="splash-image">
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.error("⚠️ 'assets/splash.png' hi hmuh a ni lo!")

    time.sleep(6)
    st.session_state.splash_done = True
    st.rerun()

else:
    # --- 2. CHECK IF USER IS LOGGED IN ---
    if st.session_state.page_mode == "app_main" or st.session_state.logged_in_user is not None:
        
        st.markdown(
            """
            <style>
            .stApp {
                background-color: #0b0c14 !important;
                color: #f1f5f9 !important;
                font-family: 'Segoe UI', system-ui, sans-serif;
            }
            div[data-testid='stSidebarNav'] { display: none !important; }
            [data-testid='stSidebar'] {
                background-color: #090a10 !important;
                border-right: 1px solid #1c1e2d !important;
                max-width: 240px !important;
                min-width: 240px !important;
            }
            .choose-category-title {
                font-size: 13px !important;
                color: #0055ff !important;
                font-weight: 900 !important;
                margin-bottom: 8px !important;
            }
            .studio-panel-box { 
                background-color: #10121d !important; 
                border: 1px solid #1c1e2d !important; 
                border-radius: 6px !important; 
                padding: 12px 10px !important; 
            }
            .neon-sky-box {
                background-color: #0a1d37 !important;
                border: 1px solid #00f0ff !important;
                border-radius: 6px !important; 
                padding: 10px !important; 
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        def format_time(seconds):
            mins = int(seconds // 60)
            secs = int(seconds % 60)
            return f"{mins:02d}:{secs:02d}"

        def play_mobile_audio(file_path, accent_color="#00f0ff"):
            if file_path and os.path.exists(file_path):
                with open(file_path, "rb") as f:
                    audio_bytes = f.read()
                b64 = base64.b64encode(audio_bytes).decode()
                audio_html = f'''
                    <div style="background-color: #10121d; border: 1px solid {accent_color}; border-radius: 6px; padding: 10px; margin-bottom: 8px; width: 100%;">
                        <audio controls controlsList="nodownload" style="width: 100%; height: 42px;">
                            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                        </audio>
                    </div>
                '''
                components.html(audio_html, height=70)

        with st.sidebar:
            st.markdown(
                f'''
                <div style="margin-top: -15px;">
                    <span style="font-size: 16px; font-weight: 900; color: #ffffff;">MAX Stem Splitter</span><br>
                    <small style="color: #10b981;">👤 {st.session_state.logged_in_user}</small>
                    <div class="choose-category-title" style="margin-top: 15px;">CHOOSE CATEGORY</div>
                </div>
                ''',
                unsafe_allow_html=True,
            )

            st.page_link("app.py", label="🎛️ STEM SPLITTER")
            st.page_link("pages/noise_reduction.py", label="🔇 NOISE REDUCTION")
            st.page_link("pages/voice_recorder.py", label="🎙️ VOICE RECORDER")
            st.page_link("pages/remastering.py", label="🎚️ REMASTERING")
            st.page_link("pages/stemtube.py", label="📥 STEMTUBE")
            st.page_link("pages/recent_files.py", label="🕒 RECENT FILES")
            st.page_link("pages/projects.py", label="📁 PROJECTS")
            st.page_link("pages/cloud_drive.py", label="☁️ CLOUD DRIVE")
            st.page_link("pages/settings.py", label="⚙️ SETTINGS")
            
            st.divider()
            if st.button("Log out", use_container_width=True):
                st.session_state.logged_in_user = None
                st.session_state.page_mode = "signin"
                st.rerun()

        st.markdown('<div style="color:#06b6d4; font-size:17px; font-weight:bold; margin-bottom:10px;">🎛️ STEM SPLITTER</div>', unsafe_allow_html=True)
        user_media_uploader = st.file_uploader("Audio File Dropzone", type=["mp3", "wav"])
        if user_media_uploader:
            st.success("File uploaded successfully!")

    else:
        # --- 3. LOGIN PAGE (DIRECT EMAIL / PASSWORD INPUT) ---
        st.markdown(
            """
            <style>
            .stApp { background-color: #000000 !important; color: white; }
            [data-testid="collapsedControl"] { display: none !important; }
            section[data-testid="stSidebar"] { display: none !important; }
            
            div[data-testid="column"]:nth-of-type(2) {
                background-color: #111111;
                padding: 2.5rem;
                border-radius: 12px;
                margin-top: 5vh;
                border: 1px solid #222222;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        col1, col2, col3 = st.columns([1, 1.5, 1])
        
        with col2:
            st.markdown(
                """
                <div style='text-align: center; margin-bottom: 10px;'>
                    <span style='font-size: 32px; font-weight: bold;'>
                        <span style='color: #4285F4;'>G</span><span style='color: #EA4335;'>o</span><span style='color: #FBBC05;'>o</span><span style='color: #4285F4;'>g</span><span style='color: #34A853;'>l</span><span style='color: #EA4335;'>e</span>
                    </span>
                </div>
                <h2 style='text-align: center; color: #ffffff; font-weight: 400; margin-bottom: 5px;'>Sign in</h2>
                <p style='text-align: center; color: #aaaaaa; font-size: 14px; margin-bottom: 25px;'>Use your Google Account</p>
                """, 
                unsafe_allow_html=True
            )

            # Direct inputs for any Google Account Email & Password
            email_input = st.text_input("Email or phone", placeholder="Enter your email or phone")
            password_input = st.text_input("Password", type="password", placeholder="Enter your password")
            
            if st.button("Sign in", use_container_width=True, type="primary"):
                if email_input and password_input:
                    st.session_state.logged_in_user = email_input
                    st.session_state.page_mode = "app_main"
                    st.success("Successfully signed in!")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.warning("I email leh password chhut luh rawh.")
