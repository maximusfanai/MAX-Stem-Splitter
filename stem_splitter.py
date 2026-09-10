import os
import streamlit as st

# Local PC / Device-a folder thlan tura Tkinter hmanga popup siamna
def choose_folder():
    try:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        folder_selected = filedialog.askdirectory(master=root)
        root.destroy()
        return folder_selected
    except Exception:
        return None

st.set_page_config(
    page_title="MAX Stem Splitter",
    page_icon="🎛️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Phone-a Portrait-a hmeh din tura JavaScript siam a ni
st.markdown(
    """
    <script>
    function triggerPortrait() {
        let elem = document.documentElement;
        if (elem.requestFullscreen) {
            elem.requestFullscreen().then(() => {
                if (screen.orientation && screen.orientation.lock) {
                    screen.orientation.lock('portrait').catch(function(error) {
                        console.log("Orientation lock failed: ", error);
                    });
                }
            }).catch(function(err) {
                console.log("Fullscreen request failed: ", err);
            });
        }
    }
    </script>
    
    <style>
    /* Dark Theme Base & Text Set Up */
    html, body, .stApp, p, span, div, label, h1, h2, h3, h4, h5, h6 { 
        background-color: #0b0c14 !important; 
        color: #ffffff !important; 
        font-family: system-ui, -apple-system, sans-serif !important;
        overflow-x: hidden !important;
    }
    
    [data-testid='stSidebar'] { 
        background-color: #090a10 !important; 
        border-right: 1px solid #1e2541 !important;
        max-width: 220px !important;
    }

    .block-container { 
        max-width: 100% !important; 
        padding: 0.4rem 0.6rem !important;
    }

    .stMarkdown, .stText, div[data-testid="stWidgetLabel"] p, label, span, div {
        color: #ffffff !important;
    }

    /* Audio Player Custom CSS */
    audio {
        width: 100% !important;
        min-width: 150px !important;
        display: block !important;
        height: 32px !important;
    }
    
    audio::-webkit-media-controls-volume-slider,
    audio::-webkit-media-controls-mute-button,
    audio::-webkit-media-controls-overflow-button,
    audio::-webkit-media-controls-download-button {
        display: none !important;
    }
    
    div[data-testid="stAudio"] {
        width: 100% !important;
    }

    details summary div[data-testid="stExpanderToggleIcon"],
    summary svg[data-testid="stExpanderToggleIcon"] {
        display: none !important;
    }

    /* Action Buttons (Purple Gradient) */
    div[data-testid="stButton"] button, div[data-testid="stDownloadButton"] button { 
        background: linear-gradient(135deg, #7c3aed 0%, #4f46e5 100%) !important; 
        border-radius: 4px !important; 
        border: 1px solid #8b5cf6 !important; 
        color: #ffffff !important; 
        font-weight: bold !important;
        width: 100% !important;
    }
    
    div[data-testid="stButton"] button p, 
    div[data-testid="stButton"] button span,
    div[data-testid="stDownloadButton"] button p,
    div[data-testid="stDownloadButton"] button span {
        color: #ffffff !important;
    }

    /* Right Panel Settings Buttons */
    .right-settings-btn div[data-testid="stButton"] button,
    .right-settings-btn div[data-testid="stButton"] button p,
    .right-settings-btn div[data-testid="stButton"] button span {
        background: linear-gradient(135deg, #7c3aed 0%, #4f46e5 100%) !important;
        border: 1px solid #a855f7 !important;
        box-shadow: 0 0 10px rgba(168, 85, 247, 0.4) !important;
        color: #ffffff !important;
        height: 32px !important;
        min-height: 32px !important;
        font-size: 11px !important;
        padding: 2px 6px !important;
        margin-bottom: 4px !important;
    }

    .track-row-box {
        background: #121526; 
        border: 1px solid #1e2541; 
        border-radius: 6px;
        padding: 6px 8px; 
        margin-bottom: 6px;
    }

    .sec-title {
        font-size: 10px !important;
        font-weight: bold !important;
        color: #ffffff !important;
        margin: 4px 0 2px 0 !important;
        letter-spacing: 0.5px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

if "output_folder" not in st.session_state:
    st.session_state.output_folder = "downloads"
if "split_done" not in st.session_state:
    st.session_state.split_done = False
if "stems_paths" not in st.session_state:
    st.session_state.stems_paths = {}

# Sidebar Menu
with st.sidebar:
    st.markdown(
        '<div style="font-weight:900; font-size:16px; color:#ffffff;'
        ' margin-bottom:3px;">MAX</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div style="font-size:11px; color:#ffffff;'
        ' font-weight:900; margin-bottom:10px; letter-spacing: 0.5px;">CHOOSE'
        " CATEGORY</div>",
        unsafe_allow_html=True,
    )

    st.page_link("app.py", label="🎛️ STEM SPLITTER")
    st.page_link("pages/noise_reduction.py", label="🔇 NOISE REDUCTION")
    st.page_link("pages/voice_recorder.py", label="🎙️ VOICE RECORDER")
    st.page_link("pages/remastering.py", label="🎚️ REMASTERING")
    st.page_link("pages/stemtube.py", label="🎵 STEMTUBE")
    st.page_link("pages/recent_files.py", label="📁 RECENT FILES")
    st.page_link("pages/projects.py", label="📂 PROJECTS")
    st.page_link("pages/cloud_drive.py", label="☁️ CLOUD DRIVE")
    st.page_link("pages/settings.py", label="⚙️ SETTINGS")

# Main Header
st.markdown(
    '<div style="font-weight:900; font-size:13px; color:#ffffff;'
    ' margin-bottom:6px;">MAX <span style="color:#ffffff;">| Stem'
    " Splitter</span></div>",
    unsafe_allow_html=True,
)
st.markdown('<div class="sec-title">STEM SPLITTER</div>', unsafe_allow_html=True)

col_left, col_right = st.columns([0.72, 0.28], gap="small")

with col_left:
    st.markdown(
        '<div class="sec-title">SELECT AUDIO</div>', unsafe_allow_html=True
    )
    uploaded_file = st.file_uploader(
        "Upload Audio", type=["mp3", "wav"], label_visibility="collapsed"
    )

    if uploaded_file is not None:
        st.markdown(
            f'<div style="background:#121526; border:1px solid #ffffff;'
            " border-radius:4px; padding:4px 6px; font-size:10px;"
            f' margin-top:3px; color:#ffffff;">🎵 {uploaded_file.name}</div>',
            unsafe_allow_html=True,
        )
        st.audio(uploaded_file, format="audio/wav")

    b1, b2 = st.columns(2)
    with b1:
        if st.button("✂️ SPLITTER", use_container_width=True):
            # Screen lock hi portrait-ah a lek tur JS trigger-na
            st.markdown(
                '<script>triggerPortrait();</script>', unsafe_allow_html=True
            )
            if uploaded_file is not None:
                st.session_state.split_done = True
                st.success("Done!")
            else:
                st.warning("Upload audio first.")
    with b2:
        if st.button("Cancel", use_container_width=True):
            st.session_state.split_done = False
            st.rerun()

    st.markdown(
        '<div class="sec-title" style="margin-top:8px;">EXTRACTED STEMS</div>', unsafe_allow_html=True
    )

    stems_list = [
        {"name": "Vocals", "icon": "🎤", "color": "#ffffff", "key": "vocals"},
        {"name": "Drum", "icon": "🥁", "color": "#ffffff", "key": "drums"},
        {"name": "Bass", "icon": "🎸", "color": "#ffffff", "key": "bass"},
        {
            "name": "Other Instrument",
            "icon": "🎹",
            "color": "#ffffff",
            "key": "other",
        },
    ]

    for item in stems_list:
        st.markdown('<div class="track-row-box">', unsafe_allow_html=True)
        st.markdown(
            f'<div style="display: flex; align-items: center; gap: 4px;'
            ' margin-bottom:4px;">'
            f'<span style="color: {item["color"]}; font-size:12px;">{item["icon"]}</span>'
            '<span style="color: #ffffff; font-size: 11px;'
            f' font-weight: 600;">{item["name"]}</span>'
            "</div>",
            unsafe_allow_html=True,
        )

        if st.session_state.split_done and uploaded_file is not None:
            st.audio(uploaded_file, format="audio/wav")
            
            c_dl1, c_dl2 = st.columns(2)
            
            # Download Button
            with c_dl1:
                st.download_button(
                    label=f"⬇️ Download {item['name']}",
                    data=uploaded_file.getvalue(),
                    file_name=f"{item['key']}_{uploaded_file.name}",
                    mime="audio/wav",
                    key=f"dl_{item['key']}",
                    use_container_width=True,
                )
            
            # Choose Folder & Save Button
            with c_dl2:
                if st.button(f"📁 Choose Folder", key=f"fld_{item['key']}", use_container_width=True):
                    selected_dir = choose_folder()
                    if selected_dir:
                        out_path = os.path.join(selected_dir, f"{item['key']}_{uploaded_file.name}")
                        with open(out_path, "wb") as f:
                            f.write(uploaded_file.getvalue())
                        st.success(f"Saved: {out_path}")
                    else:
                        st.info("Folder thlan loh a ni.")
        else:
            st.markdown(
                f'<div style="font-size:9px; color:{item["color"]}; text-align:center;'
                ' padding:2px;">✨ Ready after splitting</div>',
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

with col_right:
    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    st.markdown('<div class="right-settings-btn">', unsafe_allow_html=True)

    with st.expander("⚡ Quality"):
        st.radio(
            "Quality",
            ["Fast", "Normal", "High", "Ultra"],
            label_visibility="collapsed",
        )

    with st.expander("🎛️ Effect"):
        st.slider("Reverb (Enhanced Hall)", 0, 100, 0)
        st.slider("Auto-Tune Correction", 0, 100, 0)
        st.slider("Echo Delay/Feedback", 0, 100, 0)
        st.slider("Vocals Vol", 0, 100, 100)
        st.slider("Vocal Pan & Pitch", -1.0, 1.0, 0.0)

    with st.expander("📁 Format"):
        st.radio(
            "Format",
            ["WAV (Lossless)", "MP3 (Standard)"],
            label_visibility="collapsed",
        )

    with st.expander("🎤 Voice Changer"):
        st.radio(
            "Voice",
            [
                "Normal",
                "Female / Woman Voice",
                "Male / Man Voice",
                "Baby / Kid",
                "Megaphone / Telephone",
                "Monster",
                "Old Woman",
                "Old Man",
                "Robot",
            ],
            label_visibility="collapsed",
        )

    if st.button("▶️ Play Preview", use_container_width=True):
        st.info("Preview playing...")

    st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)
    if st.button("💾 SAVE & EXPORT", use_container_width=True):
        if st.session_state.split_done:
            st.success("Exported!")
        else:
            st.warning("Split first.")

    st.markdown("</div>", unsafe_allow_html=True)