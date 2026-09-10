import base64
import os
import time
from pathlib import Path

from pydub import AudioSegment, effects
import streamlit as st

st.set_page_config(
    page_title="Remastering Studio",
    page_icon="🎚️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Unified Theme & Styling
st.markdown(
    """
    <style>
    /* Global App Theme */
    .stApp {
        background-color: #0b0c14 !important;
        color: #f1f5f9 !important;
        font-family: 'Segoe UI', system-ui, sans-serif;
        max-width: 100% !important;
        overflow-x: hidden !important;
    }
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
    }
    div[data-testid='stSidebarNav'] { display: none !important; }

    /* Sidebar Theme */
    [data-testid='stSidebar'] {
        background-color: #090a10 !important;
        border-right: 1px solid #1c1e2d !important;
        max-width: 240px !important;
        min-width: 240px !important;
        padding-top: 0px !important;
    }
    
    [data-testid='stSidebar'] > div:first-child {
        padding-top: 0px !important;
        margin-top: 0px !important;
    }

    [data-testid='stSidebar'] [data-testid='stVerticalBlock'] {
        gap: 10px !important;
    }

    /* Sidebar Links Box */
    [data-testid='stSidebar'] div[data-testid='stPageLink'],
    [data-testid='stSidebar'] div[data-testid='stPageLink'] > a,
    [data-testid='stSidebar'] div[data-testid='stPageLink'][aria-current="page"],
    [data-testid='stSidebar'] div[data-testid='stPageLink'][aria-current="page"] > a,
    [data-testid='stSidebar'] div[data-testid='stPageLink']:hover,
    [data-testid='stSidebar'] div[data-testid='stPageLink']:active,
    [data-testid='stSidebar'] div[data-testid='stPageLink']:focus {
        background-color: #091326 !important;
        background-image: none !important;
        border: 1.5px solid #00bfff !important;
        border-radius: 6px !important;
        box-shadow: 0 0 14px rgba(0, 191, 255, 0.5), inset 0 0 6px rgba(0, 191, 255, 0.2) !important;
        margin-bottom: 8px !important;
        width: 100% !important;
        padding: 6px 8px !important;
        transform: none !important;
        opacity: 1 !important;
    }
    
    [data-testid='stSidebar'] div[data-testid='stPageLink'] span,
    [data-testid='stSidebar'] div[data-testid='stPageLink'] p,
    [data-testid='stSidebar'] div[data-testid='stPageLink'] div {
        color: #ffffff !important;
        font-weight: bold !important;
        font-size: 12px !important;
        background-color: transparent !important;
    }

    .choose-category-title {
        font-size: 13px !important;
        color: #0055ff !important;
        text-shadow: 0 0 10px #0055ff, 0 0 20px #1e90ff !important;
        font-weight: 900 !important;
        margin-bottom: 8px !important;
        margin-top: 4px !important;
        letter-spacing: 1px !important;
    }

    .top-header-container { 
        display: flex; 
        align-items: center; 
        margin-bottom: 12px; 
        margin-top: -10px; 
    }
    .main-logo-brand { 
        font-family: 'Arial Black', sans-serif; 
        font-size: 20px; 
        font-weight: 900; 
        color: #ffffff; 
        margin-right: 10px; 
    }
    .main-app-title { 
        font-family: 'Segoe UI', sans-serif; 
        font-size: 17px; 
        color: #06b6d4; 
        border-left: 2px solid #06b6d4; 
        padding-left: 10px; 
        font-weight: 700; 
    }

    /* Main Container Card */
    .remaster-card {
        background: linear-gradient(145deg, #0e121e 0%, #161b2e 100%);
        border: 1px solid #232a42;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 0 20px rgba(6, 182, 212, 0.15);
        margin-bottom: 16px;
    }

    .preview-label {
        color: #06b6d4;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 6px;
    }

    /* Custom File Uploader */
    div[data-testid='stFileUploader'] {
        background-color: #0e1c38 !important;
        border: 1px dashed #06b6d4 !important;
        border-radius: 6px !important;
        padding: 4px !important;
    }
    div[data-testid='stFileUploader'] section { padding: 4px !important; }

    /* Universal Buttons Theme */
    div.stButton > button {
        background: linear-gradient(135deg, #06b6d4 0%, #0284c7 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        border-radius: 6px !important;
        border: 1px solid #06b6d4 !important;
        font-size: 13px !important;
        min-height: 40px !important;
        width: 100% !important;
        box-shadow: 0 0 12px rgba(6, 182, 212, 0.3) !important;
        transition: all 0.2s ease-in-out !important;
    }
    
    div.stButton > button:hover {
        box-shadow: 0 0 18px rgba(6, 182, 212, 0.7) !important;
        transform: scale(0.99) !important;
    }

    div[data-testid='stDownloadButton'] > button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        border: 1px solid #10b981 !important;
        box-shadow: 0 0 12px rgba(16, 185, 129, 0.4) !important;
        color: #ffffff !important;
        font-weight: bold !important;
        min-height: 40px !important;
        border-radius: 6px !important;
    }

    /* Sliders Styling */
    div[data-baseweb="slider"] {
        padding-top: 4px !important;
        padding-bottom: 4px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar setup with Logo check
logo_b64 = ""
logo_path = "E:/StemSplitterProject/logo.png"
if os.path.exists(logo_path):
    with open(logo_path, "rb") as lf:
        logo_b64 = base64.b64encode(lf.read()).decode()

with st.sidebar:
    st.markdown(
        f"""
        <div style="margin-top: -85px;">
            <div style="display: flex; align-items: center; margin-bottom: 4px;">
                <img src="data:image/png;base64,{logo_b64}" style="width: 32px; height: 32px; margin-right: 8px; object-fit: contain;" />
                <span style="font-family: 'Segoe UI', system-ui, sans-serif; font-size: 16px; font-weight: 900; color: #ffffff; letter-spacing: 0.5px;">MAX Remastering</span>
            </div>
            <div class="choose-category-title">CHOOSE CATEGORY</div>
        </div>
        """,
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

# Main Header
st.markdown(
    '<div class="top-header-container"><span class="main-logo-brand">MAX</span><span class="main-app-title">Audio Remastering Studio</span></div>',
    unsafe_allow_html=True,
)

# Card Container
st.markdown('<div class="remaster-card">', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Upload Audio for Remastering",
    type=["mp3", "wav", "m4a", "flac"],
    label_visibility="visible",
)

if uploaded_file is not None:
    st.markdown('<div style="margin-top:12px;"></div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="preview-label">▶️ Original Audio Preview</div>',
        unsafe_allow_html=True,
    )
    st.audio(uploaded_file)
    st.markdown('<div style="margin-top:12px;"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        boost_gain = st.slider("Volume Gain Boost (dB)", 0, 25, 8)
    with col2:
        clarity_level = st.slider("Clarity Enhancement Level", 0, 100, 50)

    st.markdown('<div style="margin-top:8px;"></div>', unsafe_allow_html=True)

    if "is_remastering" not in st.session_state:
        st.session_state.is_remastering = False

    btn_label = (
        "⏳ Processing Audio..."
        if st.session_state.is_remastering
        else "🎚️ Process & Remaster"
    )

    if st.button(
        btn_label, use_container_width=True, disabled=st.session_state.is_remastering
    ):
        st.session_state.is_remastering = True
        st.rerun()

    if st.session_state.is_remastering:
        progress_bar = st.progress(0, text="Initializing audio remastering...")

        time.sleep(0.3)
        progress_bar.progress(25, text="Analyzing frequency spectrum...")
        audio = AudioSegment.from_file(uploaded_file)

        time.sleep(0.3)
        progress_bar.progress(
            55, text="Applying gain boost & clarity enhancement..."
        )

        # Peak normalization & dynamic loudness tuning
        processed_audio = audio.normalize()

        if boost_gain > 0:
            processed_audio = processed_audio + boost_gain

        if clarity_level > 0:
            cutoff = int(70 + (clarity_level * 2.2))
            processed_audio = processed_audio.high_pass_filter(cutoff)

        time.sleep(0.3)
        progress_bar.progress(85, text="Exporting remastered audio file...")

        output_dir = "downloads"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, "remastered_output.mp3")
        processed_audio.export(output_path, format="mp3", bitrate="320k")

        progress_bar.progress(100, text="✨ Remastering complete!")
        time.sleep(0.5)
        st.session_state.is_remastering = False
        st.rerun()

    output_path = "downloads/remastered_output.mp3"
    if os.path.exists(output_path) and not st.session_state.is_remastering:
        st.markdown(
            '<div style="font-size:12px; color:#10b981; font-weight:bold; background:#0e1c38; padding:8px; border-radius:6px; text-align:center; border:1px solid #10b981; margin-top:12px;">✅ Remastering Completed Successfully!</div>',
            unsafe_allow_html=True,
        )
        st.markdown('<div style="margin-top:12px;"></div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="preview-label">▶️ Remastered Audio Preview</div>',
            unsafe_allow_html=True,
        )
        st.audio(output_path)

        st.markdown('<div style="margin-top:8px;"></div>', unsafe_allow_html=True)
        with open(output_path, "rb") as f:
            st.download_button(
                label="💾 Download Remastered Audio Track",
                data=f,
                file_name="remastered_output.mp3",
                mime="audio/mp3",
                use_container_width=True,
            )
else:
    st.info("Remaster turin audio file upload rawh.")

st.markdown("</div>", unsafe_allow_html=True)