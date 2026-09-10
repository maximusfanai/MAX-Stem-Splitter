import base64
from datetime import datetime
import os
import time

import streamlit as st

st.set_page_config(
    page_title="MAX Cloud Drive",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Unified Theme & Styling
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0b0c14 !important;
        color: #ffffff !important;
        font-family: 'Segoe UI', system-ui, sans-serif;
    }
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
    }
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
        gap: 10px !important;
    }

    [data-testid='stSidebar'] div[data-testid='stPageLink'],
    [data-testid='stSidebar'] div[data-testid='stPageLink'] > a {
        background-color: #091326 !important;
        border: 1.5px solid #00bfff !important;
        border-radius: 6px !important;
        margin-bottom: 8px !important;
        width: 100% !important;
        padding: 6px 8px !important;
    }
    
    [data-testid='stSidebar'] div[data-testid='stPageLink'] span,
    [data-testid='stSidebar'] div[data-testid='stPageLink'] p {
        color: #ffffff !important;
        font-weight: bold !important;
        font-size: 12px !important;
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
        margin-bottom: 16px; 
        margin-top: -10px; 
    }
    .main-logo-brand { 
        font-size: 20px; 
        font-weight: 900; 
        color: #ffffff; 
        margin-right: 10px; 
    }
    .main-app-title { 
        font-size: 17px; 
        color: #06b6d4; 
        border-left: 2px solid #06b6d4; 
        padding-left: 10px; 
        font-weight: 700; 
    }

    .status-badge-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background-color: #101524;
        border: 1px solid #1e293b;
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 16px;
    }
    .status-active {
        color: #10b981;
        font-weight: bold;
        font-size: 13px;
    }

    .file-item-card {
        background-color: #101524;
        border: 1px solid #1e293b;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 10px;
    }
    
    div.stButton > button {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%) !important;
        border-radius: 6px !important;
        border: 1px solid #38bdf8 !important;
        font-size: 12px !important;
        color: #ffffff !important;
        font-weight: bold !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar setup
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
                <span style="font-size: 16px; font-weight: 900; color: #ffffff;">MAX Cloud Drive</span>
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

st.markdown(
    '<div class="top-header-container"><span'
    ' class="main-logo-brand">MAX</span><span class="main-app-title">Cloud'
    ' Storage & Backup</span></div>',
    unsafe_allow_html=True,
)

cloud_dir = "cloud_drive"
os.makedirs(cloud_dir, exist_ok=True)


def get_file_size(size_bytes):
  if size_bytes < 1024:
    return f"{size_bytes} B"
  elif size_bytes < 1024 * 1024:
    return f"{size_bytes / 1024:.1f} KB"
  else:
    return f"{size_bytes / (1024 * 1024):.2f} MB"


# Storage Bar
files_list = []
for root, dirs, filenames in os.walk(cloud_dir):
  for f in filenames:
    files_list.append(os.path.join(root, f))

total_used_bytes = sum(os.path.getsize(f) for f in files_list if os.path.exists(f))
used_mb = total_used_bytes / (1024 * 1024)
max_quota_mb = 1024.0
quota_pct = min(int((used_mb / max_quota_mb) * 100), 100)

st.markdown(
    f"""
    <div class="status-badge-container">
        <div>
            <div class="status-active">🟢 MAX Local Cloud Sync Active</div>
            <div style="font-size:11px; color:#64748b;">Storage Folder: <code>./cloud_drive/</code></div>
        </div>
        <div style="text-align:right;">
            <div style="font-size:12px; font-weight:bold; color:#06b6d4;">{used_mb:.1f} MB / {max_quota_mb:.0f} MB Used</div>
            <div style="font-size:10px; color:#64748b;">Quota Used: {quota_pct}%</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.progress(quota_pct / 100, text=f"Storage Capacity: {quota_pct}%")

st.markdown("<div style='margin-top:16px;'></div>", unsafe_allow_html=True)

# Google Photos Style Batch Selector / Backup Section
with st.expander(
    "📸 Gallery Backup: Select Files & Create Custom Folder", expanded=True
):
  st.markdown(
      "<div style='font-size:12px; color:#38bdf8; margin-bottom:8px;'>Hmun"
      " hrang hranga i file siam tawhte (Outputs, Voice Records, Projects) lo"
      " lang chu tick-in, folder bik siamin a rualin backup rawh.</div>",
      unsafe_allow_html=True,
  )

  # Scan source folders where files are usually saved (e.g., outputs, voice_records, projects, etc.)
  source_dirs = ["output", "voice_records", "projects", "stemtube_downloads"]
  all_source_files = []

  for sdir in source_dirs:
    if os.path.exists(sdir):
      for root, dirs, files in os.walk(sdir):
        for file in files:
          f_path = os.path.join(root, file)
          all_source_files.append(
              {
                  "name": file,
                  "path": f_path,
                  "size": os.path.getsize(f_path),
                  "mtime": os.path.getmtime(f_path),
                  "category": sdir,
              }
          )

  if not all_source_files:
    st.info(
        "Backup tur file hmuh tur a la awm lo. Stem Splitter emaw Voice"
        " Recorder-ah file siam hmasa phawt rawh."
    )
  else:
    # Custom Folder Name Input
    backup_folder_name = st.text_input(
        "📁 Cloud Backup Folder Hming (Optional):",
        value="My_Backup",
        placeholder="Entirnan: Album_1, Jam_Tracks",
    )

    selected_files_to_backup = []

    st.markdown(
        "<div style='font-size:12px; font-weight:bold; color:#f8fafc;"
        " margin-top:10px;'>Select Files to Backup:</div>",
        unsafe_allow_html=True,
    )

    # Display in a compact grid/list with checkboxes
    for idx, sf in enumerate(all_source_files):
      col_chk, col_info = st.columns([0.1, 0.9])
      with col_chk:
        is_checked = st.checkbox("", key=f"sel_file_{idx}")
      with col_info:
        st.markdown(
            f"**{sf['name']}** <span style='font-size:10px;"
            f" color:#64748b;'>({sf['category']} |"
            f" {get_file_size(sf['size'])})</span>",
            unsafe_allow_html=True,
        )
        if is_checked:
          selected_files_to_backup.append(sf)

    st.markdown("<div style='margin-top:10px;'></div>", unsafe_allow_html=True)
    if st.button("🚀 Backup Selected Files to Cloud", use_container_width=True):
      if not selected_files_to_backup:
        st.warning("Backup tur file pakhat mah i la tick lo!")
      else:
        # Create target custom folder inside cloud_dir
        target_sub_dir = os.path.join(
            cloud_dir, backup_folder_name.strip() or "General"
        )
        os.makedirs(target_sub_dir, exist_ok=True)

        copied_count = 0
        for item in selected_files_to_backup:
          dest_path = os.path.join(target_sub_dir, item["name"])
          with open(item["path"], "rb") as f_src, open(
              dest_path, "wb"
          ) as f_dst:
            f_dst.write(f_src.read())
          copied_count += 1

        st.success(
            f"Successfully backed up {copied_count} file(s) to folder:"
            f" '{backup_folder_name}'!"
        )
        time.sleep(1)
        st.rerun()

st.markdown("<div style='margin-top:16px;'></div>", unsafe_allow_html=True)

# List Cloud Files & Folders
st.markdown(
    '<div style="font-size:13px; color:#06b6d4; font-weight:bold;'
    ' margin-bottom:12px;">Cloud Drive Contents & Folders</div>',
    unsafe_allow_html=True,
)

root_files = [
    f for f in os.listdir(cloud_dir) if os.path.isfile(os.path.join(cloud_dir, f))
]
root_dirs = [
    d for d in os.listdir(cloud_dir) if os.path.isdir(os.path.join(cloud_dir, d))
]

if not root_files and not root_dirs:
  st.markdown(
      """
        <div style="background-color:#0e1526; border:1px dashed #1e293b; border-radius:8px; padding:30px; text-align:center; color:#64748b; font-size:13px;">
            <div style="font-size:32px; margin-bottom:8px;">☁️</div>
            <div>Cloud Storage is empty.</div>
        </div>
        """,
      unsafe_allow_html=True,
  )
else:
  # Show Folders first
  if root_dirs:
    st.markdown(
        "<div style='font-size:11px; color:#94a3b8; font-weight:bold;"
        " margin-bottom:6px;'>FOLDERS</div>",
        unsafe_allow_html=True,
    )
    for folder_name in root_dirs:
      folder_path = os.path.join(cloud_dir, folder_name)
      sub_files = os.listdir(folder_path)
      st.markdown(
          f"""
            <div class="file-item-card" style="border-left: 3px solid #06b6d4;">
                <div class="file-title">📁 {folder_name}</div>
                <div class="file-meta">Contains {len(sub_files)} file(s)</div>
            </div>
            """,
          unsafe_allow_html=True,
      )

  # Show direct files in root cloud_dir
  if root_files:
    st.markdown(
        "<div style='font-size:11px; color:#94a3b8; font-weight:bold;"
        " margin-top:12px; margin-bottom:6px;'>FILES</div>",
        unsafe_allow_html=True,
    )
    for idx, fname in enumerate(root_files):
      fpath = os.path.join(cloud_dir, fname)
      stat = os.stat(fpath)
      mod_time = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M")
      size_str = get_file_size(stat.st_size)

      st.markdown(
          f"""
            <div class="file-item-card">
                <div class="file-title">☁️ {fname}</div>
                <div class="file-meta">Uploaded: {mod_time} &nbsp;|&nbsp; Size: {size_str}</div>
            </div>
            """,
          unsafe_allow_html=True,
      )

      c_play, c_dl, c_del = st.columns([3, 1, 1])
      with c_play:
        if fname.lower().endswith((".mp3", ".wav", ".m4a", ".flac", ".ogg")):
          st.audio(fpath)
        else:
          st.caption("📄 Non-media file")
      with c_dl:
        with open(fpath, "rb") as fd:
          st.download_button(
              "💾 Download", fd, file_name=fname, key=f"dl_root_{idx}"
          )
      with c_del:
        if st.button("🗑️ Delete", key=f"del_root_{idx}"):
          os.remove(fpath)
          st.toast(f"Removed {fname}")
          time.sleep(0.3)
          st.rerun()