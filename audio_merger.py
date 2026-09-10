import streamlit as st

st.set_page_config(page_title="Audio Merger", page_icon="🔀", layout="wide", initial_sidebar_state="expanded")
st.markdown("<style>.stApp { background-color: #0b0c14 !important; color: #f1f5f9 !important; font-family: 'Segoe UI', sans-serif; } div[data-testid='stSidebarNav'] { display: none !important; } [data-testid='stSidebar'] { background-color: #090a10 !important; border-right: 1px solid #1c1e2d !important; max-width: 240px !important; }</style>", unsafe_allow_html=True)

with st.sidebar:
    st.markdown('<div style="font-family: Arial Black; font-size: 22px; color: #fff; padding: 10px 0;">MAX</div>', unsafe_allow_html=True)
    st.markdown('<div style="color: #4b5563; font-size: 11px; font-weight: bold; margin-bottom: 5px;">CHOOSE CATEGORY</div>', unsafe_allow_html=True)
    st.page_link("app.py", label="🎛️ STEM SPLITTER")
    st.page_link("pages/audio_editor.py", label="✂️ AUDIO EDITOR")
    st.page_link("pages/noise_reduction.py", label="🔇 NOISE REDUCTION")
    st.page_link("pages/voice_recorder.py", label="🎙️ VOICE RECORDER")
    st.page_link("pages/audio_merger.py", label="🔀 AUDIO MERGER")
    st.page_link("pages/remastering.py", label="🎚️ REMASTERING")
    st.page_link("pages/recent_files.py", label="🕒 RECENT FILES")
    st.page_link("pages/projects.py", label="📁 PROJECTS")
    st.page_link("pages/cloud_drive.py", label="☁️ CLOUD DRIVE")
    st.page_link("pages/settings.py", label="⚙️ SETTINGS")

st.markdown('<div style="font-size:20px; font-weight:bold; color:#06b6d4; margin-bottom:10px;">🔀 AUDIO MERGER</div>', unsafe_allow_html=True)
st.markdown('<div style="background:#10121d; border:1px solid #1c1e2d; padding:15px; border-radius:6px;">', unsafe_allow_html=True)
st.file_uploader("Upload Multiple Audio Files to Merge", type=["mp3", "wav"], accept_multiple_files=True)
st.markdown('</div>', unsafe_allow_html=True)