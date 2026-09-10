import base64
import os
import streamlit as st
from pydub import AudioSegment

st.set_page_config(
    page_title="Noise Reduction",
    page_icon="🔇",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Logo path leh Base64 encoding (HTML chhunga fiah taka a lan theih nan)
logo_path = r"E:\stemsplitterproject\logo.png"
logo_img_tag = ""
if os.path.exists(logo_path):
  with open(logo_path, "rb") as f:
    encoded_logo = base64.b64encode(f.read()).decode()
    logo_img_tag = f'<img src="data:image/png;base64,{encoded_logo}" style="height: 22px; width: auto; margin-right: 8px; vertical-align: middle;">'

st.markdown(
    """
<style>
    .stApp { background-color: #0b0c14 !important; color: #f1f5f9 !important; font-family: 'Segoe UI', sans-serif; }
    div[data-testid='stSidebarNav'] { display: none !important; }
    
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
        gap: 12px !important;
    }

    /* Sidebar Page Links - Completely Static across all active/hover/focus states */
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
        margin-bottom: 12px !important;
        width: 100% !important;
        padding: 6px 8px !important;
        transform: none !important;
        opacity: 1 !important;
    }
    
    [data-testid='stSidebar'] div[data-testid='stPageLink'] span,
    [data-testid='stSidebar'] div[data-testid='stPageLink'] p,
    [data-testid='stSidebar'] div[data-testid='stPageLink'] div,
    [data-testid='stSidebar'] div[data-testid='stPageLink'][aria-current="page"] span,
    [data-testid='stSidebar'] div[data-testid='stPageLink'][aria-current="page"] p,
    [data-testid='stSidebar'] div[data-testid='stPageLink'][aria-current="page"] div {
        color: #ffffff !important;
        font-weight: bold !important;
        font-size: 12px !important;
        background-color: transparent !important;
    }

    .main-card {
        background: linear-gradient(145deg, #10121d 0%, #171a2b 100%);
        border: 1px solid #25283d;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
        margin-bottom: 20px;
    }
    .header-title {
        font-size: 20px;
        font-weight: 800;
        color: #06b6d4;
        letter-spacing: 0.5px;
    }
    .stButton > button {
        background: linear-gradient(135deg, #06b6d4 0%, #0284c7 100%) !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 12px 20px !important;
        box-shadow: 0 4px 14px rgba(6, 182, 212, 0.4);
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        opacity: 0.9;
        box-shadow: 0 6px 20px rgba(6, 182, 212, 0.6);
    }
    .preview-label {
        color: #94a3b8;
        font-size: 13px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 6px;
    }
</style>
""",
    unsafe_allow_html=True,
)

with st.sidebar:
  st.markdown(
      f"""
        <div style="margin-top: -85px;">
            <div style="display: flex; align-items: center; margin-bottom: 4px;">
                {logo_img_tag}
                <span style="font-family: 'Segoe UI', system-ui, sans-serif; font-size: 16px; font-weight: 900; color: #ffffff; letter-spacing: 0.5px;">MAX Stem Splitter</span>
            </div>
            <div style="color: #0055ff; font-size: 13px; font-weight: 900; margin-bottom: 8px; margin-top: 4px; letter-spacing: 1px;">CHOOSE CATEGORY</div>
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

# Title leh Back button chu "NOISE REDUCTION" ziahna chung chiah ah dah a ni a
col_title, col_back = st.columns([75, 25])
with col_title:
  st.markdown(
      '<div class="header-title">🔇 NOISE REDUCTION STUDIO</div>',
      unsafe_allow_html=True,
  )
with col_back:
  st.page_link("app.py", label="🔙 Back", use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

st.markdown('<div class="main-card">', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Upload Audio to Clean Noise", type=["mp3", "wav"]
)

if uploaded_file is not None:
  st.markdown("<br>", unsafe_allow_html=True)
  st.markdown(
      '<div class="preview-label">▶️ Original Audio Preview</div>',
      unsafe_allow_html=True,
  )
  st.audio(uploaded_file)
  st.markdown("<br>", unsafe_allow_html=True)

  noise_level = st.slider("Noise Reduction Level", 0, 100, 50)

  st.markdown("<br>", unsafe_allow_html=True)

  if "is_processing" not in st.session_state:
    st.session_state.is_processing = False

  btn_label = "Processing..." if st.session_state.is_processing else "Process"

  if st.button(btn_label, use_container_width=True):
    st.session_state.is_processing = True
    st.rerun()

  if st.session_state.is_processing:
    progress_bar = st.progress(0, text="Initializing noise reduction...")

    progress_bar.progress(30, text="Analyzing audio stream...")
    audio = AudioSegment.from_file(uploaded_file)

    progress_bar.progress(60, text="Applying high-pass noise filter...")
    filtered_audio = audio
    if noise_level > 0:
      cutoff = int(80 + (noise_level * 18))
      filtered_audio = filtered_audio.high_pass_filter(cutoff)

    progress_bar.progress(85, text="Exporting cleaned audio file...")
    output_dir = "downloads"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "denoised_output.mp3")
    filtered_audio.export(output_path, format="mp3")

    progress_bar.progress(100, text="Processing complete!")
    st.session_state.is_processing = False
    st.rerun()

  output_path = "downloads/denoised_output.mp3"
  if os.path.exists(output_path) and not st.session_state.is_processing:
    st.markdown("<br>", unsafe_allow_html=True)
    st.success("Noise reduction a zo ta!")
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        '<div class="preview-label">▶️ Cleaned Audio Preview</div>',
        unsafe_allow_html=True,
    )
    st.audio(output_path)

    with open(output_path, "rb") as f:
      st.download_button(
          label="📥 Download Cleaned Audio",
          data=f,
          file_name="denoised_output.mp3",
          mime="audio/mp3",
          use_container_width=True,
      )
else:
  st.info("Audio file upload turin hmet rawh.")

st.markdown("</div>", unsafe_allow_html=True)