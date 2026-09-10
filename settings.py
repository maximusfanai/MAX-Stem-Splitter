import atexit
import base64
import json
import os
import shutil
import streamlit as st

CONFIG_FILE = "config.json"

# Default Configuration Values
DEFAULT_SETTINGS = {
    "app_theme": "Dark Mode (Default)",
    "export_format": "MP3",
    "export_bitrate": "320 kbps",
    "processing_engine": "CPU (Default)",
    "output_folder": "downloads",
    "auto_cleanup": True,
}


# Helper function to load configuration
def load_config():
  config = DEFAULT_SETTINGS.copy()
  if os.path.exists(CONFIG_FILE):
    try:
      with open(CONFIG_FILE, "r") as f:
        data = json.load(f)
        config.update(data)
    except Exception:
      pass
  return config


# Helper function to save configuration
def save_config(data):
  try:
    with open(CONFIG_FILE, "w") as f:
      json.dump(data, f, indent=4)
    return True
  except Exception as e:
    st.error(f"Config save error: {e}")
    return False


# Functional Temporary File Clean Up Mechanism
def clean_temporary_files():
  cfg = load_config()
  if cfg.get("auto_cleanup", True):
    out_dir = cfg.get("output_folder", "downloads")
    target_dirs = ["temp", os.path.join(out_dir, "temp"), "cache_temp"]

    cleaned_count = 0
    for target in target_dirs:
      if os.path.exists(target) and os.path.isdir(target):
        for item in os.listdir(target):
          item_path = os.path.join(target, item)
          try:
            if os.path.isfile(item_path) or os.path.islink(item_path):
              os.unlink(item_path)
              cleaned_count += 1
            elif os.path.isdir(item_path):
              shutil.rmtree(item_path)
              cleaned_count += 1
          except Exception:
            pass
    return cleaned_count
  return 0


# Register auto-cleanup on Python app process exit
atexit.register(clean_temporary_files)

# Page Configuration
st.set_page_config(
    page_title="MAX Settings",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load saved values into session state ONCE on initial load
saved_cfg = load_config()
for key, default_val in DEFAULT_SETTINGS.items():
  if key not in st.session_state:
    st.session_state[key] = saved_cfg.get(key, default_val)

# Load Logo Image in Base64
logo_b64 = ""
logo_paths = [
    r"E:/maxstemsplitter project/logo.png",
    r"E:/StemSplitterProject/logo.png",
    "logo.png",
]
for path in logo_paths:
  if os.path.exists(path):
    try:
      with open(path, "rb") as lf:
        logo_b64 = base64.b64encode(lf.read()).decode()
      break
    except Exception:
      pass


# Dynamic Theme CSS Generator
def get_theme_css(theme):
  if theme == "Glassmorphic Dark":
    bg_color = (
        "radial-gradient(circle at 50% 30%, #1e2640 0%, #0c0e18 100%)"
        " !important"
    )
    card_bg = "rgba(255, 255, 255, 0.05)"
    card_border = "1px solid rgba(255, 255, 255, 0.15)"
    card_shadow = "0 8px 32px 0 rgba(0, 0, 0, 0.4)"
    accent_color = "#38bdf8"
    input_bg = "rgba(255, 255, 255, 0.08)"
    input_border = "1px solid rgba(56, 189, 248, 0.5)"
    btn_bg = (
        "linear-gradient(135deg, rgba(56,189,248,0.5) 0%,"
        " rgba(3,105,161,0.8) 100%)"
    )
  elif theme == "Cyberpunk Blue Neon":
    bg_color = "#030712 !important"
    card_bg = "linear-gradient(145deg, #050b18 0%, #0a1738 100%)"
    card_border = "1px solid #00f0ff"
    card_shadow = "0 0 25px rgba(0, 240, 255, 0.25)"
    accent_color = "#00f0ff"
    input_bg = "#081026"
    input_border = "1.5px solid #00f0ff"
    btn_bg = "linear-gradient(135deg, #00f0ff 0%, #0077ff 100%)"
  else:  # Dark Mode (Default)
    bg_color = "#0b0c14 !important"
    card_bg = "linear-gradient(145deg, #0e121e 0%, #161b2e 100%)"
    card_border = "1px solid #232a42"
    card_shadow = "0 0 20px rgba(6, 182, 212, 0.15)"
    accent_color = "#06b6d4"
    input_bg = "#161929"
    input_border = "1.5px solid #0ea5e9"
    btn_bg = "linear-gradient(135deg, #0284c7 0%, #0369a1 100%)"

  return f"""
    <style>
    header[data-testid="stHeader"] {{ display: none !important; }}
    
    .stApp {{
        background: {bg_color};
        color: #ffffff !important;
        font-family: 'Segoe UI', system-ui, sans-serif;
        max-width: 100% !important;
        overflow-x: hidden !important;
    }}
    
    .block-container {{
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        max-width: 680px !important;
        background: {card_bg} !important;
        border: {card_border} !important;
        border-radius: 12px !important;
        box-shadow: {card_shadow} !important;
        backdrop-filter: blur(12px);
        margin-top: -35px !important;
    }}
    
    div[data-testid='stSidebarNav'] {{ display: none !important; }}

    [data-testid='stSidebar'] {{
        background-color: #090a10 !important;
        border-right: 1px solid #1c1e2d !important;
        max-width: 240px !important;
        min-width: 240px !important;
        padding-top: 0px !important;
    }}
    
    [data-testid='stSidebar'] > div:first-child {{
        padding-top: 0px !important;
        margin-top: 0px !important;
    }}

    [data-testid='stSidebar'] [data-testid='stVerticalBlock'] {{ 
        gap: 10px !important; 
        margin-top: -30px !important; 
    }}

    [data-testid='stSidebar'] div[data-testid='stPageLink'],
    [data-testid='stSidebar'] div[data-testid='stPageLink'] > a {{
        background-color: #091326 !important;
        border: 1.5px solid {accent_color} !important;
        border-radius: 6px !important;
        box-shadow: 0 0 14px rgba(0, 191, 255, 0.4) !important;
        margin-bottom: 8px !important;
        width: 100% !important;
        padding: 6px 8px !important;
    }}
    
    [data-testid='stSidebar'] div[data-testid='stPageLink'] span {{
        color: #ffffff !important;
        font-weight: bold !important;
        font-size: 12px !important;
    }}

    .choose-category-title {{
        font-size: 16px !important;
        color: #ffffff !important;
        text-shadow: 0 0 10px rgba(255, 255, 255, 0.2) !important;
        font-weight: 900 !important;
        text-transform: uppercase !important;
        margin-bottom: 10px !important;
        margin-top: 12px !important;
    }}

    /* Header Logo & Colored Title Text */
    .header-logo-img {{ width: 38px; height: 38px; margin-right: 10px; object-fit: contain; }}

    /* Header Back Button Styling */
    .header-back-btn {{
        background: {btn_bg} !important;
        border-radius: 6px !important;
        border: 1px solid {accent_color} !important;
        color: #ffffff !important;
        font-weight: bold !important;
        font-size: 12px !important;
        padding: 5px 12px !important;
        text-decoration: none !important;
        box-shadow: 0 0 10px {accent_color}44 !important;
        white-space: nowrap !important;
        display: inline-block !important;
        transition: background 0.1s ease;
    }}

    .header-back-btn:active {{
        background: #000000 !important;
        border-color: {accent_color} !important;
        color: #ffffff !important;
        box-shadow: 0 0 5px #000000 !important;
        transform: scale(0.96);
    }}

    /* Section Headers Font Size */
    .setting-section-title {{
        color: {accent_color} !important;
        font-size: 16px !important;
        font-weight: 800 !important;
        margin-bottom: 8px !important;
        margin-top: 14px !important;
    }}

    div[data-testid='stTextInput'] input {{ 
        background-color: {input_bg} !important; 
        border: {input_border} !important; 
        color: #ffffff !important; 
        font-size: 12px !important; 
        height: 38px !important; 
        border-radius: 6px !important;
    }}
    div[data-testid='stSelectbox'] div[data-baseweb='select'] {{ 
        background-color: {input_bg} !important; 
        border: {input_border} !important; 
        color: #ffffff !important; 
        font-size: 12px !important; 
        min-height: 38px !important; 
        border-radius: 6px !important;
    }}

    /* General Button Styling */
    div.stButton > button {{
        background: {btn_bg} !important;
        border-radius: 6px !important;
        border: 1px solid {accent_color} !important;
        font-size: 13px !important;
        min-height: 36px !important;
        color: #ffffff !important;
        font-weight: bold !important;
        box-shadow: 0 0 12px {accent_color}55 !important;
        white-space: nowrap !important;
        padding: 0 12px !important;
        transition: background 0.1s ease;
    }}

    /* Touch / Click Active Effect */
    div.stButton > button:active, div.stButton > button:focus:active {{
        background: #000000 !important;
        border-color: {accent_color} !important;
        color: #ffffff !important;
        box-shadow: 0 0 15px #000000 !important;
        transform: scale(0.96);
    }}

    div[data-testid='InputInstructions'] {{ display: none !important; }}
    </style>
    """


# Inject CSS dynamically based on active session state theme
st.markdown(get_theme_css(st.session_state.app_theme), unsafe_allow_html=True)


# Helper function to get accent color directly for inline HTML elements
def get_accent_color(theme):
  if theme == "Glassmorphic Dark":
    return "#38bdf8"
  elif theme == "Cyberpunk Blue Neon":
    return "#00f0ff"
  else:
    return "#06b6d4"


current_accent = get_accent_color(st.session_state.app_theme)

# Sidebar Menu Setup
with st.sidebar:
  logo_img_tag = (
      f'<img src="data:image/png;base64,{logo_b64}" style="width: 32px;'
      ' height: 32px; margin-right: 8px; object-fit: contain;" />'
      if logo_b64
      else ""
  )
  st.markdown(
      f"""
        <div style="margin-top: 0px;">
            <div style="display: flex; align-items: center; margin-bottom: 4px;">
                {logo_img_tag}
                <span style="font-family: 'Segoe UI', system-ui, sans-serif; font-size: 16px; font-weight: 900;">
                    <span style="color: #ffffff;">MAX</span> <span style="color: {current_accent};">Stem Splitter</span>
                </span>
            </div>
            <div class="choose-category-title">CHOOSE CATEGORY</div>
        </div>
        """,
      unsafe_allow_html=True,
  )

  # Spacer to move the category boxes down by 2 steps while keeping CHOOSE CATEGORY untouched
  st.markdown("<div style='margin-top: 16px;'></div>", unsafe_allow_html=True)

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
header_logo_html = (
    f'<img src="data:image/png;base64,{logo_b64}" class="header-logo-img" />'
    if logo_b64
    else ""
)
st.markdown(
    f"""
    <div style="display: flex; justify-content: space-between; align-items: center; width: 100%; margin-top: -5px; margin-bottom: 12px;">
        <div style="display: flex; align-items: center;">
            {header_logo_html}
            <span style="font-family: 'Segoe UI', system-ui, sans-serif; font-size: 20px; color: #ffffff; font-weight: 800;">Stem Settings</span>
        </div>
        <a href="/" target="_self" class="header-back-btn">🔙 Back</a>
    </div>
    """,
    unsafe_allow_html=True,
)

# 🎨 Themes Appearance
st.markdown(
    '<div class="setting-section-title">🎨 Themes Appearance</div>',
    unsafe_allow_html=True,
)
theme_options = ["Dark Mode (Default)", "Glassmorphic Dark", "Cyberpunk Blue Neon"]
st.selectbox("Select Interface Theme:", theme_options, key="app_theme")

st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)

# 🎵 Audio Export Format & Quality
st.markdown(
    '<div class="setting-section-title">🎵 Audio Export Format & Quality</div>',
    unsafe_allow_html=True,
)
col_fmt, col_bit = st.columns(2)

with col_fmt:
  st.selectbox(
      "Audio Format:", ["MP3", "WAV", "FLAC", "M4A"], key="export_format"
  )

with col_bit:
  st.selectbox(
      "Quality Bitrate:",
      [
          "1080 kbps",
          "720 kbps",
          "320 kbps",
          "256 kbps",
          "192 kbps",
          "128 kbps",
      ],
      key="export_bitrate",
  )

st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)

# 🚀 Processing Engine
st.markdown(
    '<div class="setting-section-title">🚀 Processing Engine (Stem Splitter /'
    ' Remaster)</div>',
    unsafe_allow_html=True,
)
st.selectbox(
    "Hardware Acceleration:",
    ["CPU (Default)", "GPU (CUDA Acceleration)"],
    key="processing_engine",
)

st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)

# 📁 Output Directory Path
st.markdown(
    '<div class="setting-section-title">📁 Output Directory Path</div>',
    unsafe_allow_html=True,
)

col_dir, col_browse = st.columns([4.2, 0.8], vertical_alignment="bottom")

with col_dir:
  st.text_input("Downloads Folder Path:", key="output_folder")

with col_browse:
  if st.button("📁 Browse Folder", use_container_width=False):
    try:
      import tkinter as tk
      from tkinter import filedialog

      root = tk.Tk()
      root.withdraw()
      root.attributes("-topmost", True)
      chosen_dir = filedialog.askdirectory(master=root)
      root.destroy()
      if chosen_dir:
        st.session_state.output_folder = chosen_dir
        st.rerun()
    except Exception as e:
      st.error(f"Folder selection error: {e}")

st.markdown("<div style='margin-top: 10px;'></div>", unsafe_allow_html=True)

# 🧹 Maintenance & Storage
st.markdown(
    '<div class="setting-section-title">🧹 Maintenance & Storage</div>',
    unsafe_allow_html=True,
)

col_clean_toggle, col_clean_now = st.columns([3.5, 1.2], vertical_alignment="center")

with col_clean_toggle:
  st.toggle("Automatically clean temporary files on exit", key="auto_cleanup")

with col_clean_now:
  if st.button("🧹 Clean Temp Now", use_container_width=False):
    cleaned = clean_temporary_files()
    st.toast(f"Cleaned {cleaned} temporary items!")

st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

# 💾 Save & 🔄 Reset Buttons
c_save, c_reset, _ = st.columns([0.3, 0.35, 0.35])

with c_save:
  if st.button("💾 Save Settings", use_container_width=False):
    current_config = {
        "app_theme": st.session_state.app_theme,
        "export_format": st.session_state.export_format,
        "export_bitrate": st.session_state.export_bitrate,
        "processing_engine": st.session_state.processing_engine,
        "output_folder": st.session_state.output_folder,
        "auto_cleanup": st.session_state.auto_cleanup,
    }
    if save_config(current_config):
      if st.session_state.auto_cleanup:
        clean_temporary_files()
      st.toast("Settings saved successfully!")
      st.rerun()

with c_reset:
  if st.button("🔄 Reset Defaults", use_container_width=False):
    for k, v in DEFAULT_SETTINGS.items():
      st.session_state[k] = v

    save_config(DEFAULT_SETTINGS)
    st.toast("Reset to default settings!")
    st.rerun()