import base64
import os
import time
import numpy as np
import soundfile as sf
import streamlit as st
import streamlit.components.v1 as components

# --- TORCH & HUGGINGFACE PATHS (Portable) ---
if os.name == 'nt':
    os.environ['TORCH_HOME'] = 'E:/StemSplitterProject/cache/torch'
    os.environ['HF_HOME'] = 'E:/StemSplitterProject/cache/huggingface'
    os.environ['HUGGINGFACE_HUB_CACHE'] = 'E:/StemSplitterProject/cache/huggingface/hub'
else:
    os.environ['TORCH_HOME'] = '/tmp/torch'
    os.environ['HF_HOME'] = '/tmp/huggingface'
    os.environ['HUGGINGFACE_HUB_CACHE'] = '/tmp/huggingface/hub'

st.set_page_config(
    page_title="MAX Stem Splitter & Auth",
    page_icon="🎛️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- SESSION STATES INITIALIZATION ---
if "page_mode" not in st.session_state:
    st.session_state.page_mode = "signin"

if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None

if "split_done" not in st.session_state:
    st.session_state.split_done = False
if "stems_paths" not in st.session_state:
    st.session_state.stems_paths = {}

# --- CHECK IF USER IS LOGGED IN ---
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
        </style>
        """,
        unsafe_allow_html=True,
    )

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
    st.page_link("noise_reduction.py", label="🔇 NOISE REDUCTION")
    st.page_link("voice_recorder.py", label="🎙️ VOICE RECORDER")
    st.page_link("remastering.py", label="🎚️ REMASTERING")
    st.page_link("stemtube.py", label="📥 STEMTUBE")
    st.page_link("recent_files.py", label="🕒 RECENT FILES")
    st.page_link("projects.py", label="📁 PROJECTS")
    st.page_link("cloud_drive.py", label="☁️ CLOUD DRIVE")
    st.page_link("settings.py", label="⚙️ SETTINGS")
        
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
    # --- LOGIN PAGE ---
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
