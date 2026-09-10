import base64
from datetime import datetime
import os
import shutil
import time
import streamlit as st

st.set_page_config(
    page_title="MAX Projects",
    page_icon="📁",
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
        color: #ffffff !important;
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

    /* Header Container */
    .top-header-container { 
        display: flex; 
        align-items: center; 
        margin-bottom: 16px; 
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
    .projects-card {
        background: linear-gradient(145deg, #0e121e 0%, #161b2e 100%);
        border: 1px solid #232a42;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 0 20px rgba(6, 182, 212, 0.15);
        margin-bottom: 16px;
    }

    .project-item-card {
        background-color: #101524;
        border: 1px solid #1e293b;
        border-radius: 8px;
        padding: 14px 18px;
        margin-bottom: 12px;
        transition: all 0.2s ease-in-out;
    }
    .project-item-card:hover {
        border-color: #06b6d4;
        box-shadow: 0 0 14px rgba(6, 182, 212, 0.25);
    }

    .project-title {
        color: #f8fafc;
        font-size: 15px;
        font-weight: 700;
        margin-bottom: 4px;
    }
    .project-meta {
        color: #64748b;
        font-size: 11px;
        font-weight: 600;
    }

    .empty-state {
        background-color: #0e1526;
        border: 1px dashed #1e293b;
        border-radius: 8px;
        padding: 30px;
        text-align: center;
        color: #64748b;
        font-size: 13px;
        font-weight: 600;
    }

    /* Input & Button Styling */
    div[data-testid='stTextInput'] input { 
        background-color: #161929 !important; 
        border: 1.5px solid #0ea5e9 !important; 
        color: #ffffff !important; 
        font-size: 12px !important; 
        height: 38px !important; 
        border-radius: 6px !important;
    }

    div.stButton > button {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important;
        border-radius: 6px !important;
        border: 1px solid #38bdf8 !important;
        font-size: 12px !important;
        min-height: 36px !important;
        color: #ffffff !important;
        font-weight: bold !important;
    }

    div[data-testid='InputInstructions'] { display: none !important; }
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
                <span style="font-family: 'Segoe UI', system-ui, sans-serif; font-size: 16px; font-weight: 900; color: #ffffff; letter-spacing: 0.5px;">MAX Projects</span>
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
    '<div class="top-header-container"><span'
    ' class="main-logo-brand">MAX</span><span class="main-app-title">Project'
    ' Workspace</span></div>',
    unsafe_allow_html=True,
)

# Root directory for storing project folders
projects_base = "projects"
os.makedirs(projects_base, exist_ok=True)


def get_dir_size(path):
  total = 0
  for root, _, files in os.walk(path):
    for f in files:
      total += os.path.getsize(os.path.join(root, f))
  if total < 1024:
    return f"{total} B"
  elif total < 1024 * 1024:
    return f"{total / 1024:.1f} KB"
  else:
    return f"{total / (1024 * 1024):.2f} MB"


st.markdown('<div class="projects-card">', unsafe_allow_html=True)

# Create New Project Input
c_in, c_btn = st.columns([3, 1])
with c_in:
  new_proj_name = st.text_input(
      "Create Project Workspace Folder:",
      placeholder="e.g. Acoustic_Album_Vocal_Stems",
  )
with c_btn:
  st.markdown("<div style='margin-top:28px;'></div>", unsafe_allow_html=True)
  if st.button("➕ Create Project", use_container_width=True):
    if new_proj_name.strip():
      clean_folder = "".join(
          c for c in new_proj_name if c.isalnum() or c in (" ", "_", "-")
      ).strip()
      p_path = os.path.join(projects_base, clean_folder)
      if not os.path.exists(p_path):
        os.makedirs(p_path)
        st.toast(f"Project '{clean_folder}' created!")
        time.sleep(0.3)
        st.rerun()
      else:
        st.warning("Project with this name already exists.")

st.markdown("<div style='margin-top:16px;'></div>", unsafe_allow_html=True)

# List Existing Projects
projects_list = [
    d
    for d in os.listdir(projects_base)
    if os.path.isdir(os.path.join(projects_base, d))
]

if not projects_list:
  st.markdown(
      """
        <div class="empty-state">
            <div style="font-size:32px; margin-bottom:8px;">📁</div>
            <div>No active projects found.</div>
            <div style="font-size:11px; margin-top:6px; color:#475569;">Create a project folder above to organize your stems, audio tracks, and mixes.</div>
        </div>
        """,
      unsafe_allow_html=True,
  )
else:
  st.markdown(
      f'<div style="font-size:12px; color:#06b6d4; font-weight:bold;'
      f' margin-bottom:12px;">Active Projects ({len(projects_list)})</div>',
      unsafe_allow_html=True,
  )

  for idx, p_name in enumerate(projects_list):
    p_path = os.path.join(projects_base, p_name)
    stat = os.stat(p_path)
    mod_time = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M")
    p_size = get_dir_size(p_path)
    file_count = len(os.listdir(p_path))

    st.markdown(
        f"""
            <div class="project-item-card">
                <div class="project-title">📁 {p_name}</div>
                <div class="project-meta">Last Updated: {mod_time} &nbsp;|&nbsp; Files: {file_count} &nbsp;|&nbsp; Total Size: {p_size}</div>
            </div>
            """,
        unsafe_allow_html=True,
    )

    with st.expander(f"🔍 Manage Content - {p_name}", expanded=False):
      p_files = os.listdir(p_path)
      if not p_files:
        st.caption("No files in this project workspace.")
      else:
        for pf in p_files:
          f_full = os.path.join(p_path, pf)
          c_f1, c_f2 = st.columns([3, 1])
          with c_f1:
            st.markdown(
                f"<span style='font-size:12px;' >🎵 {pf}</span>",
                unsafe_allow_html=True,
            )
            if pf.lower().endswith((".mp3", ".wav", ".flac", ".m4a", ".ogg")):
              st.audio(f_full)
          with c_f2:
            if st.button("🗑️ Delete File", key=f"del_f_{idx}_{pf}"):
              os.remove(f_full)
              st.rerun()

      if st.button(
          f"🗑️ Delete Whole Project Folder ({p_name})", key=f"del_proj_{idx}"
      ):
        shutil.rmtree(p_path)
        st.toast(f"Deleted project {p_name}")
        time.sleep(0.3)
        st.rerun()

    st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)