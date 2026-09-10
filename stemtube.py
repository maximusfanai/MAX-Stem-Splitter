import base64
import os
import time

import streamlit as st
import yt_dlp

# Folder chooser atan Tkinter support
try:
  import tkinter as tk
  from tkinter import filedialog

  HAS_TK = True
except Exception:
  HAS_TK = False

st.set_page_config(
    page_title="MAX StemTube Downloader",
    page_icon="📥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Mobile Responsive Styling
st.markdown(
    """
    <style>
    /* Strict Mobile Viewport Boundaries */
    html, body, .stApp, div[data-testid="stAppViewContainer"] {
        background-color: #0b0c14 !important;
        color: #ffffff !important;
        font-family: 'Segoe UI', system-ui, sans-serif;
        max-width: 100vw !important;
        overflow-x: hidden !important;
    }
    
    .block-container {
        padding: 0.5rem 0.5rem 1rem 0.5rem !important;
        max-width: 100% !important;
        width: 100% !important;
        box-sizing: border-box !important;
    }

    div[data-testid='stSidebarNav'] { display: none !important; }

    /* Horizontal Block Alignment Fix */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        align-items: flex-end !important;
        gap: 4px !important;
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
    }

    /* Column 1 (Link Input): Flex Width (~78%) */
    div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-child(1),
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(1) {
        flex: 78 1 0% !important;
        min-width: 0 !important;
        width: auto !important;
        max-width: none !important;
    }

    /* Column 2 (Paste Button): Flex Width (~22%) */
    div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-child(2),
    div[data-testid="stHorizontalBlock"] > div[data-testid="column"]:nth-child(2) {
        flex: 22 1 0% !important;
        min-width: 0 !important;
        width: auto !important;
        max-width: none !important;
    }

    div[data-testid="stHorizontalBlock"] div[data-testid="stTextInput"],
    div[data-testid="stHorizontalBlock"] div[data-testid="stTextInput"] input {
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
    }

    /* Sidebar Theme */
    [data-testid='stSidebar'] {
        background-color: #090a10 !important;
        border-right: 1px solid #1c1e2d !important;
        max-width: 240px !important;
        min-width: 240px !important;
    }
    
    [data-testid='stSidebar'] div[data-testid='stPageLink'],
    [data-testid='stSidebar'] div[data-testid='stPageLink'] > a {
        background-color: #091326 !important;
        border: 1.5px solid #00bfff !important;
        border-radius: 6px !important;
        margin-bottom: 6px !important;
        padding: 4px 6px !important;
    }
    
    [data-testid='stSidebar'] div[data-testid='stPageLink'] span {
        color: #ffffff !important;
        font-weight: bold !important;
        font-size: 11px !important;
    }

    .choose-category-title {
        font-size: 12px !important;
        color: #0055ff !important;
        font-weight: 900 !important;
        margin-bottom: 6px !important;
    }

    /* Header Container */
    .top-header-container { 
        display: flex; 
        align-items: center; 
        margin-bottom: 8px; 
        margin-top: 0px; 
    }
    .main-app-title { 
        display: flex;
        align-items: center;
        gap: 6px;
        font-family: 'Segoe UI', system-ui, sans-serif; 
        font-size: 16px; 
        font-weight: 900; 
        color: #ffffff; 
    }
    .main-app-title span {
        color: #38bdf8; 
    }

    /* StemTube Button Box */
    .stemtube-btn-box {
        display: flex !important; 
        align-items: center !important; 
        justify-content: center !important; 
        gap: 6px !important;
        background: linear-gradient(135deg, #0c192c 0%, #0369a1 100%) !important;
        border: 1.5px solid #38bdf8 !important; 
        color: #ffffff !important;
        padding: 6px 12px !important; 
        border-radius: 5px !important; 
        font-size: 12px !important; 
        font-weight: bold !important;
        text-decoration: none !important; 
        margin: 0 auto 10px auto !important; 
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    }

    /* Input & Select Box Styling */
    div[data-testid='stTextInput'], div[data-testid='stSelectbox'] {
        width: 100% !important;
        margin-bottom: 0px !important;
    }

    div[data-testid='stTextInput'] label, div[data-testid='stSelectbox'] label {
        font-size: 11px !important;
        font-weight: bold !important;
        color: #38bdf8 !important;
        margin-bottom: 2px !important;
    }
    
    div[data-testid='stTextInput'] input { 
        background-color: #161929 !important; 
        border: 1.5px solid #0ea5e9 !important; 
        color: #ffffff !important; 
        font-size: 11px !important; 
        height: 32px !important; 
        border-radius: 5px !important;
        padding: 0 6px !important;
        width: 100% !important;
        box-sizing: border-box !important;
    }
    
    div[data-testid='stSelectbox'] div[data-baseweb='select'] { 
        background-color: #161929 !important; 
        border: 1.5px solid #0ea5e9 !important; 
        color: #ffffff !important; 
        font-size: 11px !important; 
        min-height: 32px !important; 
        border-radius: 5px !important;
        width: 100% !important;
    }

    /* Paste Button Aligned Exact with Text Input Box */
    .custom-paste-btn {
        display: flex !important; 
        align-items: center !important; 
        justify-content: center !important; 
        height: 32px !important; 
        width: 100% !important;
        background: linear-gradient(135deg, #161929 0%, #0f172a 100%); 
        border: 1.5px solid #0ea5e9;
        color: #ffffff !important; 
        border-radius: 5px; 
        font-size: 10px; 
        font-weight: bold; 
        cursor: pointer;
        box-sizing: border-box !important;
        white-space: nowrap;
        padding: 0 2px;
        margin-top: -28px !important;
    }

    /* Buttons */
    div.stButton > button, div.stDownloadButton > button { 
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important; 
        border-radius: 5px !important; 
        border: 1.5px solid #38bdf8 !important; 
        font-size: 12px !important; 
        width: 100% !important; 
        max-width: 100% !important;
        min-height: 34px !important; 
        color: #ffffff !important; 
        font-weight: bold !important;
        padding: 0 4px !important;
        margin: 6px auto 0 auto !important;
        display: block !important;
    }

    /* Specific adjustment for Choose Folder button to make it narrower */
    div[data-testid="stButton"] button[kind="secondary"] {
        width: 45% !important;
        max-width: 140px !important;
    }
    
    div[data-testid='InputInstructions'] { display: none !important; }

    header[data-testid="stHeader"] {
        display: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Session States
if "output_folder" not in st.session_state:
  st.session_state.output_folder = "downloads"
if "download_state" not in st.session_state:
  st.session_state.download_state = "IDLE"
if "last_downloaded_file" not in st.session_state:
  st.session_state.last_downloaded_file = None
if "last_downloaded_type" not in st.session_state:
  st.session_state.last_downloaded_type = "Audio"

yt_svg = """<svg width="18" height="13" viewBox="0 0 28 20" fill="none" xmlns="http://www.w3.org/2000/svg" style="vertical-align: middle; margin-right: 4px;"><rect width="28" height="20" rx="5" fill="#0055ff"/><path d="M11 5.5L19 10L11 14.5V5.5Z" fill="white"/></svg>"""

with st.sidebar:
  st.markdown(
      f"""
        <div style="margin-top: -15px;">
            <div style="display: flex; align-items: center; margin-bottom: 4px;">
                {yt_svg}
                <span style="font-size: 15px; font-weight: 900; color: #ffffff;">MAX StemTube</span>
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

# Logo file check leh loadna
logo_path = r"E:\stemsplitter project\logo.png"
logo_html = ""
if os.path.exists(logo_path):
  try:
    with open(logo_path, "rb") as f:
      encoded_logo = base64.b64encode(f.read()).decode("utf-8")
      logo_html = f'<img src="data:image/png;base64,{encoded_logo}" width="22" style="vertical-align: middle; border-radius: 4px; margin-right: 4px;" />'
  except Exception as e:
    print(f"Error loading logo: {e}")

# Main Title & Back Button Row (Top)
col_title, col_back = st.columns([72, 28])

with col_title:
  st.markdown(
      f'<div class="top-header-container"><div'
      f' class="main-app-title">{logo_html}MAX <span>StemTube'
      ' Downloader</span></div></div>',
      unsafe_allow_html=True,
  )

with col_back:
  st.page_link("app.py", label="🔙 Back", use_container_width=True)

# Preview Box (Conditional - only renders if a file has been downloaded)
if st.session_state.last_downloaded_file and os.path.exists(
    st.session_state.last_downloaded_file
):
  st.markdown('<div class="stemtube-card">', unsafe_allow_html=True)
  file_path = st.session_state.last_downloaded_file
  file_name = os.path.basename(file_path)
  file_size_mb = f"{os.path.getsize(file_path) / (1024 * 1024):.2f} MB"

  st.markdown(
      f"""
        <div style="background: rgba(14, 165, 233, 0.1); border: 1.5px solid #0ea5e9; border-radius: 6px; padding: 8px; margin-bottom: 10px; text-align: center;">
            <div style="color: #38bdf8; font-weight: 800; font-size: 11px;">🎉 DOWNLOAD COMPLETED</div>
            <div style="color: #ffffff; font-weight: bold; font-size: 11px; word-break: break-all;">📄 {file_name}</div>
            <div style="color: #94a3b8; font-size: 10px; margin-bottom: 6px;">💾 File Size: {file_size_mb}</div>
        </div>
        """,
      unsafe_allow_html=True,
  )

  if "Audio" in st.session_state.last_downloaded_type:
    st.audio(file_path)
  else:
    st.video(file_path)

  with open(file_path, "rb") as f:
    st.download_button(
        label=f"📥 Save {file_name} to Device",
        data=f,
        file_name=file_name,
        mime=(
            "audio/mpeg"
            if "Audio" in st.session_state.last_downloaded_type
            else "video/mp4"
        ),
        use_container_width=True,
    )
  st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    f'<a href="https://www.youtube.com" target="_blank"'
    f' class="stemtube-btn-box">{yt_svg}<span>StemTube</span></a>',
    unsafe_allow_html=True,
)

# 1. YouTube Link Input Box & Paste Button Row
col_link, col_paste = st.columns([78, 22])

with col_link:
  youtube_url = st.text_input("YouTube link:")

with col_paste:
  st.markdown(
      r"""
        <button onclick="
            navigator.clipboard.readText().then(text => {
                const inputs = document.querySelectorAll('input');
                for (let input of inputs) {
                    if (input.getAttribute('aria-label') && input.getAttribute('aria-label').includes('YouTube link')) {
                        input.value = text;
                        input.dispatchEvent(new Event('input', { bubbles: true }));
                        break;
                    }
                }
            }).catch(err => console.log(err));
        " class="custom-paste-btn" type="button">
            📋 Paste
        </button>
    """,
      unsafe_allow_html=True,
  )

st.markdown('<div style="margin-top: 8px;"></div>', unsafe_allow_html=True)

# 2. Format & Quality Dropdowns
download_type = st.selectbox("Format:", ["Audio (MP3)", "Video (MP4)"])

quality = st.selectbox(
    "Quality:",
    (
        ["144p", "240p", "360p", "720p", "1080p"]
        if "Video" in download_type
        else ["128kbps", "192kbps", "320kbps", "720kbps", "1080kbps"]
    ),
)

# 3. Save Folder Path & Folder Chooser
output_folder = st.text_input(
    "Save Folder Path:", value=st.session_state.output_folder
)
st.session_state.output_folder = output_folder

if HAS_TK:
  if st.button("📁 Choose Folder", use_container_width=True):
    try:
      root = tk.Tk()
      root.withdraw()
      root.attributes("-topmost", True)
      chosen_dir = filedialog.askdirectory(master=root)
      root.destroy()
      if chosen_dir:
        st.session_state.output_folder = chosen_dir
        st.rerun()
    except Exception as e:
      st.error(f"Folder thlan theih a ni lo: {e}")

# Download Action Button
if st.session_state.download_state == "DOWNLOADING":
  btn_label = "❌ Cancel Download"
elif st.session_state.download_state == "COMPLETE":
  btn_label = "✅ Complete! Download Again"
else:
  btn_label = "🚀 Download from YouTube"

download_clicked = st.button(btn_label, use_container_width=True)


def progress_hook(d):
  if st.session_state.download_state == "IDLE":
    raise Exception("Download cancelled by user.")
  if d["status"] == "downloading":
    try:
      dl, tot = d.get("downloaded_bytes", 0), d.get(
          "total_bytes"
      ) or d.get("total_bytes_estimate", 0)
      if tot > 0:
        pct = min(int(dl * 100 / tot), 100)
        progress_bar.progress(pct, text=f"Downloading... {pct}%")
    except Exception:
      pass


if download_clicked:
  if st.session_state.download_state in ["DOWNLOADING", "COMPLETE"]:
    st.session_state.download_state = "IDLE"
    st.rerun()
  elif st.session_state.download_state == "IDLE":
    if not youtube_url.strip():
      st.warning("Khawngaihin YouTube link dah hmasa rawh.")
    else:
      st.session_state.download_state = "DOWNLOADING"
      st.rerun()

if st.session_state.download_state == "DOWNLOADING":
  progress_bar = st.progress(0, text="Downloading... 0%")
  try:
    if not os.path.exists(output_folder):
      os.makedirs(output_folder)

    if "Audio" in download_type:
      ydl_opts = {
          "format": "bestaudio/best",
          "noplaylist": True,
          "postprocessors": [{
              "key": "FFmpegExtractAudio",
              "preferredcodec": "mp3",
              "preferredquality": {
                  "128kbps": "128",
                  "192kbps": "192",
              }.get(quality, "320"),
          }],
          "outtmpl": f"{output_folder}/%(title)s.%(ext)s",
          "progress_hooks": [progress_hook],
      }
    else:
      h = {"144p": "144", "240p": "240", "360p": "360", "720p": "720"}.get(
          quality, "1080"
      )
      ydl_opts = {
          "format": (
              f"bestvideo[height<={h}][ext=mp4]+bestaudio[ext=m4a]/best[height<={h}][ext=mp4]/best"
          ),
          "noplaylist": True,
          "outtmpl": f"{output_folder}/%(title)s.%(ext)s",
          "merge_output_format": "mp4",
          "progress_hooks": [progress_hook],
      }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
      info = ydl.extract_info(youtube_url, download=True)
      filename = ydl.prepare_filename(info)

      base, _ = os.path.splitext(filename)
      target_file = base + (".mp3" if "Audio" in download_type else ".mp4")

      if os.path.exists(target_file):
        st.session_state.last_downloaded_file = target_file
      elif os.path.exists(filename):
        st.session_state.last_downloaded_file = filename

      st.session_state.last_downloaded_type = download_type

    progress_bar.progress(100, text="✨ Complete!")
    time.sleep(0.5)
    progress_bar.empty()

    st.session_state.download_state = "COMPLETE"
    st.rerun()

  except Exception as e:
    progress_bar.empty()
    if st.session_state.download_state != "IDLE":
      st.error(f"Error: {e}")
    st.session_state.download_state = "IDLE"
    st.rerun()