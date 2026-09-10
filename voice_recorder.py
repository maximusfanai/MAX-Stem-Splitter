import base64
import os
import tempfile
import time
from pathlib import Path

from pydub import AudioSegment
import streamlit as st
import streamlit.components.v1 as components

try:
    import yt_dlp
except ImportError:
    yt_dlp = None

st.set_page_config(
    page_title="MAX Voice Recorder",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom Unified Theme & Responsive Styling for Phone Portrait
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
        padding-left: 8px !important;
        padding-right: 8px !important;
    }
    div[data-testid='stSidebarNav'] { display: none !important; }
    
    /* Desktop & Mobile Responsive Flex Layout */
    div[data-testid='stHorizontalBlock'] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: wrap !important;
        width: 100% !important;
        max-width: 100% !important;
        gap: 16px !important;
    }
    div[data-testid='stHorizontalBlock'] > div { 
        min-width: 0 !important; 
        overflow: visible !important; 
    }

    /* Mobile Portrait Adjustments */
    @media (max-width: 768px) {
        div[data-testid='stHorizontalBlock'] {
            flex-direction: column !important;
        }
        div[data-testid="stColumn"] {
            width: 100% !important;
            max-width: 100% !important;
        }
    }

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
        margin-bottom: 8px; 
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
        color: #00d2fc; 
        border-left: 2px solid #00d2fc; 
        padding-left: 10px; 
        font-weight: 700; 
    }
    .studio-step-label { 
        color: #00d2fc !important; 
        font-weight: 700 !important; 
        font-size: 12px !important; 
        text-transform: uppercase !important; 
        margin-bottom: 6px !important; 
        letter-spacing: 0.5px; 
    }

    div[data-testid='InputInstructions'] { display: none !important; }

    div[data-testid='stFileUploader'] {
        background-color: #0e1c38 !important;
        border: 1px dashed #00d2fc !important;
        border-radius: 6px !important;
        padding: 4px !important;
    }
    div[data-testid='stFileUploader'] section { padding: 4px !important; }
    div[data-testid='stFileUploader'] small { font-size: 10px !important; }

    div.stButton > button {
        background: linear-gradient(135deg, #00d2fc 0%, #0077b6 100%) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        border-radius: 6px !important;
        border: 1px solid #00d2fc !important;
        font-size: 12px !important;
        min-height: 36px !important;
        width: 100% !important;
        padding: 0px 8px !important;
        box-shadow: 0 0 10px rgba(0, 210, 252, 0.3) !important;
        transition: all 0.2s ease-in-out !important;
    }
    
    div.stButton > button:hover {
        box-shadow: 0 0 14px rgba(0, 210, 252, 0.7) !important;
        transform: scale(0.99) !important;
    }

    div[data-testid='stDownloadButton'] > button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        border: 1px solid #10b981 !important;
        box-shadow: 0 0 10px rgba(16, 185, 129, 0.4) !important;
        color: #ffffff !important;
        font-weight: bold !important;
    }

    div[data-testid='stTextInput'] input { 
        background-color: #0e1c38 !important; 
        border: 1px solid #00d2fc !important; 
        color: #ffffff !important; 
        font-size: 12px !important; 
        min-height: 36px !important; 
        border-radius: 6px !important;
    }

    div[data-baseweb="select"] > div {
        background-color: #0e1c38 !important;
        border: 1px solid #00d2fc !important;
        color: #ffffff !important;
        border-radius: 6px !important;
    }

    div[data-baseweb="slider"] {
        padding-top: 4px !important;
        padding-bottom: 4px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

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
                <span style="font-family: 'Segoe UI', system-ui, sans-serif; font-size: 16px; font-weight: 900; color: #ffffff; letter-spacing: 0.5px;">MAX Voice Recorder</span>
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

if "imported_track" not in st.session_state:
    st.session_state.imported_track = None
if "last_imported_name" not in st.session_state:
    st.session_state.last_imported_name = None
if "show_download_btn" not in st.session_state:
    st.session_state.show_download_btn = False
if "dl_button_mode" not in st.session_state:
    st.session_state.dl_button_mode = "Download"
if "temp_dl_bytes" not in st.session_state:
    st.session_state.temp_dl_bytes = None
if "temp_dl_name" not in st.session_state:
    st.session_state.temp_dl_name = None
if "youtube_url_val" not in st.session_state:
    st.session_state.youtube_url_val = ""

st.markdown(
    '<div class="top-header-container"><span class="main-logo-brand">MAX</span><span class="main-app-title">Voice Recorder Studio</span></div>',
    unsafe_allow_html=True,
)

# Responsive Layout Split (Left main workspace, Right tool panel)
left_col, right_col = st.columns([2.3, 1.0])

with left_col:
    st.markdown('<div class="studio-step-label">1. Import Backing Audio Track</div>', unsafe_allow_html=True)

    imported_file = st.file_uploader(
        "Import Backing File", type=["mp3", "wav", "m4a", "mp4"], label_visibility="collapsed"
    )
    status_placeholder = st.empty()

    if imported_file is not None:
        if st.session_state.last_imported_name != imported_file.name:
            file_bytes = imported_file.read()
            progress_bar = status_placeholder.progress(0, text="Loading track... 0%")
            for i in range(100):
                time.sleep(0.003)
                progress_bar.progress(i + 1, text=f"Loading track... {i + 1}%")

            progress_bar.empty()
            status_placeholder.markdown(
                '<div style="font-size:11px; color:#10b981; font-weight:bold; background:#0e1c38; padding:4px 8px; border-radius:4px; text-align:center; border:1px solid #10b981; margin-top:2px;">✅ Track Loaded Successfully</div>',
                unsafe_allow_html=True,
            )
            time.sleep(1.0)
            status_placeholder.empty()

            st.session_state.imported_track = file_bytes
            st.session_state.last_imported_name = imported_file.name
            st.session_state.show_download_btn = False
        else:
            status_placeholder.markdown(
                f'<div style="font-size:11px; color:#10b981; margin-top:2px;">✅ Active Track: {st.session_state.last_imported_name}</div>',
                unsafe_allow_html=True,
            )
    elif st.session_state.last_imported_name is not None:
        status_placeholder.markdown(
            f'<div style="font-size:11px; color:#10b981; margin-top:2px;">✅ Active Track: {st.session_state.last_imported_name}</div>',
            unsafe_allow_html=True,
        )

    st.markdown('<div class="studio-step-label" style="margin-top:12px;">2. Audacity Style Multi-Track Studio</div>', unsafe_allow_html=True)

    track_audio_html = ""
    if st.session_state.imported_track is not None:
        mime_type = "audio/mpeg"
        if st.session_state.last_imported_name:
            if st.session_state.last_imported_name.endswith(".wav"):
                mime_type = "audio/wav"
            elif st.session_state.last_imported_name.endswith(".m4a"):
                mime_type = "audio/mp4"
        b64_audio = base64.b64encode(st.session_state.imported_track).decode()
        track_audio_html = f'<audio id="realBackingAudio" preload="auto" src="data:{mime_type};base64,{b64_audio}"></audio>'

    studio_html = """
    <div style="background:#12131c; border:1px solid #232538; border-radius:10px; padding:10px; color:#fff; font-family:sans-serif; width:100%; position:relative; box-sizing:border-box; box-shadow: 0 0 12px rgba(0,210,252,0.15);">
        TRACK_AUDIO_PLACEHOLDER
        <audio id="recordedAudioPlayback" preload="auto" style="display:none;"></audio>
        <audio id="mixedAudioPlayback" preload="auto" style="display:none;"></audio>

        <!-- SAVE PROMPT MODAL OVERLAY -->
        <div id="saveModal" style="display:none; position:absolute; top:0; left:0; width:100%; height:100%; background:rgba(12,14,22,0.95); z-index:99; border-radius:10px; flex-direction:column; align-items:center; justify-content:center; padding:15px; text-align:center;">
            <div style="font-size:14px; font-weight:bold; color:#fff; margin-bottom:12px;">Do you want to save & mix recording?</div>
            <div style="display:flex; gap:12px; width:100%; justify-content:center;">
                <button id="saveYesBtn" style="background:#10b981; color:#fff; border:none; border-radius:6px; padding:8px 20px; font-weight:bold; font-size:12px; cursor:pointer; box-shadow: 0 0 8px rgba(16,185,129,0.5);">YES</button>
                <button id="saveNoBtn" style="background:#ef4444; color:#fff; border:none; border-radius:6px; padding:8px 20px; font-weight:bold; font-size:12px; cursor:pointer; box-shadow: 0 0 8px rgba(239,68,68,0.5);">NO</button>
            </div>
        </div>

        <!-- MIXED RESULT CONTAINER -->
        <div id="mixedResultContainer" style="display:none; background:#161824; border:1px solid #10b981; border-radius:6px; padding:8px; margin-bottom:8px; text-align:center;">
            <div style="font-size:12px; font-weight:bold; color:#10b981; margin-bottom:6px;">✨ Mixed Track Ready!</div>
            
            <div style="display:flex; align-items:center; justify-content:center; gap:8px; margin-bottom:8px; background:#101118; padding:6px; border-radius:4px;">
                <button id="mixedPlayBtn" style="background:#10b981; color:#fff; border:none; border-radius:4px; font-size:11px; padding:4px 10px; font-weight:bold; cursor:pointer;">▶ Play Mixed</button>
                <button id="mixedStopBtn" style="background:#232538; color:#64748b; border:1px solid #475569; border-radius:4px; font-size:11px; padding:4px 10px; font-weight:bold; cursor:pointer;" disabled>⏹ Stop</button>
            </div>

            <div style="margin-bottom:6px; text-align:left;">
                <label style="font-size:10px; color:#94a3b8;">Export File Name:</label>
                <input type="text" id="mixedFileNameInput" value="voice_record.wav" style="width:100%; background:#101118; border:1px solid #10b981; color:#fff; font-size:11px; padding:4px 8px; border-radius:4px; margin-top:2px;">
            </div>
            <a id="downloadMixedBtn" style="display:block; background:linear-gradient(135deg, #10b981 0%, #059669 100%); color:#fff; text-decoration:none; font-size:12px; font-weight:bold; padding:8px; border-radius:6px; box-shadow: 0 0 8px rgba(16,185,129,0.4);" download="voice_record.wav">💾 Download Mixed Audio Track</a>
        </div>

        <!-- LAYER 1: MUSIC TRACK -->
        <div style="background:#161824; border:1px solid #232538; border-radius:6px; padding:8px; margin-bottom:8px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px; font-size:11px; font-weight:bold; color:#a855f7; flex-wrap:wrap; gap:6px;">
                <div style="display:flex; align-items:center; gap:6px; flex-wrap:wrap;">
                    <input type="checkbox" id="enableLayer1" checked style="accent-color:#a855f7; cursor:pointer;">
                    <span>🎵 LAYER 1 (BACKING TRACK)</span>
                    <button id="layer1PlayBtn" style="background:#232538; color:#a855f7; border:1px solid #a855f7; border-radius:4px; font-size:10px; padding:2px 8px; cursor:pointer;">▶ Play</button>
                    <button id="layer1StopBtn" style="background:#232538; color:#64748b; border:1px solid #475569; border-radius:4px; font-size:10px; padding:2px 8px; cursor:pointer;" disabled>⏹ Stop</button>
                </div>
                <div style="display:flex; align-items:center; gap:6px; color:#94a3b8;">
                    <span>🔊</span>
                    <input type="range" id="trackVol" min="0" max="100" value="80" style="accent-color:#a855f7; width:60px; cursor:pointer;">
                    <span id="trackVolVal">80%</span>
                </div>
            </div>
            <div style="position:relative; height:32px; background:#101118; border-radius:4px; overflow:hidden; display:flex; align-items:center; justify-content:center;">
                <canvas id="trackCanvas" width="600" height="32" style="width:100%; height:100%; cursor:pointer;"></canvas>
            </div>
        </div>

        <!-- LAYER 2: VOICE REC -->
        <div style="background:#161824; border:1px solid #232538; border-radius:6px; padding:8px; margin-bottom:8px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px; font-size:11px; font-weight:bold; color:#ef4444; flex-wrap:wrap; gap:6px;">
                <div style="display:flex; align-items:center; gap:6px; flex-wrap:wrap;">
                    <input type="checkbox" id="enableLayer2" checked style="accent-color:#ef4444; cursor:pointer;">
                    <span>🎙️ LAYER 2 (VOICE MIC)</span>
                    <button id="layer2PlayBtn" style="background:#232538; color:#64748b; border:1px solid #475569; border-radius:4px; font-size:10px; padding:2px 8px; cursor:pointer;" disabled>▶ Play</button>
                    <button id="layer2StopBtn" style="background:#232538; color:#64748b; border:1px solid #475569; border-radius:4px; font-size:10px; padding:2px 8px; cursor:pointer;" disabled>⏹ Stop</button>
                </div>
                <div style="display:flex; align-items:center; gap:6px; color:#94a3b8;">
                    <span>🎤</span>
                    <input type="range" id="micVol" min="0" max="200" value="150" style="accent-color:#ef4444; width:60px; cursor:pointer;" title="Mic Boost Gain Level">
                    <span id="micVolVal">150%</span>
                </div>
            </div>
            <div style="position:relative; height:32px; background:#101118; border-radius:4px; overflow:hidden; display:flex; align-items:center; justify-content:center;">
                <canvas id="voiceCanvas" width="600" height="32" style="width:100%; height:100%; cursor:pointer;"></canvas>
            </div>
        </div>

        <!-- REC & PLAY CONTROLS -->
        <div style="display:flex; justify-content:space-between; align-items:center; background:#161824; border:1px solid #232538; border-radius:6px; padding:8px; margin-bottom:4px;">
            <div style="text-align:center;">
                <button id="startRecBtn" style="width:44px; height:44px; border-radius:50%; background:radial-gradient(circle, #ef4444 40%, #991b1b 100%); border:2px solid #f87171; box-shadow:0 0 12px rgba(239,68,68,0.6); cursor:pointer; display:flex; align-items:center; justify-content:center; margin:0 auto;">
                    <div style="width:14px; height:14px; background:#fff; border-radius:50%;"></div>
                </button>
                <div style="font-size:9px; font-weight:bold; color:#ef4444; margin-top:3px;">REC</div>
            </div>
            <div style="text-align:center;">
                <div id="studioTimer" style="font-size:18px; font-weight:900; font-family:monospace; color:#fff; letter-spacing:1px;">00:00.00</div>
                <div id="studioStatus" style="font-size:9px; color:#94a3b8;">Ready (Active)</div>
            </div>
            <div style="text-align:center;">
                <button id="stopRecBtn" style="width:44px; height:44px; border-radius:50%; background:#1e293b; border:2px solid #475569; cursor:pointer; display:flex; align-items:center; justify-content:center; margin:0 auto;" disabled>
                    <div style="width:14px; height:14px; background:#cbd5e1; border-radius:2px;"></div>
                </button>
                <div style="font-size:9px; font-weight:bold; color:#64748b; margin-top:3px;">STOP</div>
            </div>
        </div>
    </div>

    <script>
    let mediaRecorder = null;
    let audioChunks = [];
    let startTime = 0;
    let timerInterval = null;
    let audioCtx = null;
    let analyser = null;
    let microphoneStream = null;
    let finalRecordedBlob = null;

    const startBtn = document.getElementById("startRecBtn");
    const stopBtn = document.getElementById("stopRecBtn");
    const timerDisplay = document.getElementById("studioTimer");
    const statusDisplay = document.getElementById("studioStatus");
    const backingAudio = document.getElementById("realBackingAudio");
    const recordedPlayback = document.getElementById("recordedAudioPlayback");
    const mixedPlayback = document.getElementById("mixedAudioPlayback");

    const layer1PlayBtn = document.getElementById("layer1PlayBtn");
    const layer1StopBtn = document.getElementById("layer1StopBtn");
    const layer2PlayBtn = document.getElementById("layer2PlayBtn");
    const layer2StopBtn = document.getElementById("layer2StopBtn");

    const mixedPlayBtn = document.getElementById("mixedPlayBtn");
    const mixedStopBtn = document.getElementById("mixedStopBtn");

    const enableLayer1Chk = document.getElementById("enableLayer1");
    const enableLayer2Chk = document.getElementById("enableLayer2");

    const saveModal = document.getElementById("saveModal");
    const saveYesBtn = document.getElementById("saveYesBtn");
    const saveNoBtn = document.getElementById("saveNoBtn");
    const mixedResultContainer = document.getElementById("mixedResultContainer");
    const downloadMixedBtn = document.getElementById("downloadMixedBtn");
    const mixedFileNameInput = document.getElementById("mixedFileNameInput");

    saveModal.style.display = "none";

    const trackHeights = Array.from({length: 80}, (_, i) => Math.sin(i * 0.2) * 8 + 10);
    let voiceHeights = Array.from({length: 80}, () => 8);

    if (mixedFileNameInput) {
      mixedFileNameInput.oninput = (e) => {
        let val = e.target.value.trim();
        if (val) {
          downloadMixedBtn.download = val;
        }
      };
    }

    function drawTrackWaveform(progress) {
      const canvas = document.getElementById("trackCanvas");
      if (!canvas) return;
      const ctx = canvas.getContext("2d");
      ctx.fillStyle = "#101118";
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      let barWidth = 3; let gap = 2;
      let numBars = Math.floor(canvas.width / (barWidth + gap));
      let currentBarIndex = Math.floor(numBars * progress);

      for(let i = 0; i < numBars; i++) {
        let h = trackHeights[i % trackHeights.length];
        ctx.fillStyle = (i <= currentBarIndex && progress > 0) ? "#38bdf8" : "#a855f7";
        ctx.fillRect(i * (barWidth + gap), (canvas.height - h) / 2, barWidth, h);
      }

      let lineX = progress * canvas.width;
      ctx.fillStyle = "#ffffff";
      ctx.fillRect(lineX, 0, 2, canvas.height);
    }

    function drawVoiceWaveform(progress) {
      const canvas = document.getElementById("voiceCanvas");
      if (!canvas) return;
      const ctx = canvas.getContext("2d");
      ctx.fillStyle = "#101118";
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      let barWidth = 3; let gap = 2;
      let numBars = voiceHeights.length;
      let currentBarIndex = Math.floor(numBars * progress);

      for(let i = 0; i < numBars; i++) {
        let h = voiceHeights[i];
        if (i <= currentBarIndex && progress > 0) {
          ctx.fillStyle = "#ef4444";
        } else {
          ctx.fillStyle = "#ffffff";
        }
        ctx.fillRect(i * (barWidth + gap), (canvas.height - h) / 2, barWidth, h);
      }

      let lineX = progress * canvas.width;
      ctx.fillStyle = "#00d2fc";
      ctx.fillRect(lineX, 0, 2, canvas.height);
    }

    drawTrackWaveform(0);
    drawVoiceWaveform(0);

    function updateTimer() {
      const elapsed = Date.now() - startTime;
      const mins = String(Math.floor(elapsed / 60000)).padStart(2, "0");
      const secs = String(Math.floor((elapsed % 60000) / 1000)).padStart(2, "0");
      const ms = String(Math.floor((elapsed % 1000) / 10)).padStart(2, "0");
      timerDisplay.innerText = mins + ":" + secs + "." + ms;

      let prog = 0;
      if (backingAudio && backingAudio.duration) {
        prog = backingAudio.currentTime / backingAudio.duration;
      } else {
        prog = (elapsed / 30000) % 1;
      }

      if ((mediaRecorder && mediaRecorder.state === "recording") || (enableLayer1Chk.checked && !enableLayer2Chk.checked && backingAudio && !backingAudio.paused)) {
        let voiceHeight = 8; 
        if (analyser && enableLayer2Chk.checked) {
          let dataArray = new Uint8Array(analyser.frequencyBinCount);
          analyser.getByteFrequencyData(dataArray);
          let sum = 0;
          for(let i = 0; i < dataArray.length; i++) {
            sum += dataArray[i];
          }
          let avg = sum / dataArray.length;
          if (avg > 2) {
            voiceHeight = Math.min(28, Math.max(6, (avg / 255) * 28));
          }
        }

        if (enableLayer2Chk.checked) {
          voiceHeights.push(voiceHeight);
          if (voiceHeights.length > 80) voiceHeights.shift();
        }

        if (enableLayer2Chk.checked) {
          drawVoiceWaveform(prog);
        }
      }
    }

    if (layer1PlayBtn) {
      layer1PlayBtn.onclick = () => {
        if (backingAudio) {
          backingAudio.play().then(() => {
            layer1PlayBtn.innerText = "⏸ Pause";
            layer1StopBtn.disabled = false;
            layer1StopBtn.style.color = "#a855f7";
            layer1StopBtn.style.borderColor = "#a855f7";
          }).catch(e => alert("Track a la awm lo emaw play theih a ni lo."));
        } else {
          alert("Music track import a la ni lo.");
        }
      };
    }

    if (layer1StopBtn) {
      layer1StopBtn.onclick = () => {
        if (backingAudio) {
          backingAudio.pause();
          backingAudio.currentTime = 0;
          layer1PlayBtn.innerText = "▶ Play";
          layer1StopBtn.disabled = true;
          layer1StopBtn.style.color = "#64748b";
          layer1StopBtn.style.borderColor = "#475569";
          drawTrackWaveform(0);
        }
      };
    }

    if (backingAudio) {
      backingAudio.ontimeupdate = () => {
        if (backingAudio.duration) {
          let prog = backingAudio.currentTime / backingAudio.duration;
          drawTrackWaveform(prog);
        }
      };
      backingAudio.onended = () => { 
        layer1PlayBtn.innerText = "▶ Play"; 
        layer1StopBtn.disabled = true;
        layer1StopBtn.style.color = "#64748b";
        layer1StopBtn.style.borderColor = "#475569";
        drawTrackWaveform(0);
      };
    }

    if (layer2PlayBtn) {
      layer2PlayBtn.onclick = () => {
        if (recordedPlayback && recordedPlayback.src) {
          recordedPlayback.play();
          layer2PlayBtn.innerText = "⏸ Pause";
          layer2StopBtn.disabled = false;
          layer2StopBtn.style.color = "#ef4444";
          layer2StopBtn.style.borderColor = "#ef4444";
        }
      };
    }

    if (layer2StopBtn) {
      layer2StopBtn.onclick = () => {
        if (recordedPlayback) {
          recordedPlayback.pause();
          recordedPlayback.currentTime = 0;
          layer2PlayBtn.innerText = "▶ Play";
          layer2StopBtn.disabled = true;
          layer2StopBtn.style.color = "#64748b";
          layer2StopBtn.style.borderColor = "#475569";
          drawVoiceWaveform(0);
        }
      };
    }

    if (recordedPlayback) {
      recordedPlayback.ontimeupdate = () => {
        if (recordedPlayback.duration) {
          let prog = recordedPlayback.currentTime / recordedPlayback.duration;
          drawVoiceWaveform(prog);
        }
      };
      recordedPlayback.onended = () => { 
        layer2PlayBtn.innerText = "▶ Play"; 
        layer2StopBtn.disabled = true;
        layer2StopBtn.style.color = "#64748b";
        layer2StopBtn.style.borderColor = "#475569";
        drawVoiceWaveform(0);
      };
    }

    if (mixedPlayBtn) {
      mixedPlayBtn.onclick = () => {
        if (mixedPlayback && mixedPlayback.src) {
          mixedPlayback.play().then(() => {
            mixedPlayBtn.innerText = "⏸ Pause Mixed";
            mixedStopBtn.disabled = false;
            mixedStopBtn.style.color = "#fff";
            mixedStopBtn.style.borderColor = "#10b981";
          }).catch(e => console.log("Mixed play error:", e));
        }
      };
    }

    if (mixedStopBtn) {
      mixedStopBtn.onclick = () => {
        if (mixedPlayback) {
          mixedPlayback.pause();
          mixedPlayback.currentTime = 0;
          mixedPlayBtn.innerText = "▶ Play Mixed";
          mixedStopBtn.disabled = true;
          mixedStopBtn.style.color = "#64748b";
          mixedStopBtn.style.borderColor = "#475569";
        }
      };
    }

    if (mixedPlayback) {
      mixedPlayback.onended = () => {
        mixedPlayBtn.innerText = "▶ Play Mixed";
        mixedStopBtn.disabled = true;
        mixedStopBtn.style.color = "#64748b";
        mixedStopBtn.style.borderColor = "#475569";
      };
    }

    const trackCanvas = document.getElementById("trackCanvas");
    if (trackCanvas) {
      trackCanvas.onclick = (e) => {
        if (backingAudio && backingAudio.duration) {
          const rect = trackCanvas.getBoundingClientRect();
          const clickX = e.clientX - rect.left;
          const prog = clickX / rect.width;
          backingAudio.currentTime = prog * backingAudio.duration;
          drawTrackWaveform(prog);
        }
      };
    }

    const voiceCanvas = document.getElementById("voiceCanvas");
    if (voiceCanvas) {
      voiceCanvas.onclick = (e) => {
        if (recordedPlayback && recordedPlayback.duration) {
          const rect = voiceCanvas.getBoundingClientRect();
          const clickX = e.clientX - rect.left;
          const prog = clickX / rect.width;
          recordedPlayback.currentTime = prog * recordedPlayback.duration;
          drawVoiceWaveform(prog);
        }
      };
    }

    if (startBtn) {
      startBtn.onclick = async () => {
        audioChunks = [];
        voiceHeights = Array.from({length: 80}, () => 8);
        mixedResultContainer.style.display = "none";
        
        const isL1Checked = enableLayer1Chk.checked;
        const isL2Checked = enableLayer2Chk.checked;

        if (!isL1Checked && !isL2Checked) {
          alert("Layer 1 emaw Layer 2 a tlem berah pakhat tal tick rawh.");
          return;
        }

        try {
          if (isL2Checked) {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: { echoCancellation: true, noiseSuppression: true, autoGainControl: true } });
            microphoneStream = stream;
            
            audioCtx = new (window.AudioContext || window.webkitAudioContext)();
            const source = audioCtx.createMediaStreamSource(stream);
            analyser = audioCtx.createAnalyser();
            analyser.fftSize = 256;
            source.connect(analyser);

            mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/webm;codecs=opus' });
            mediaRecorder.ondataavailable = event => { if(event.data.size > 0) audioChunks.push(event.data); };
            mediaRecorder.onstop = () => {
              finalRecordedBlob = new Blob(audioChunks, { type: "audio/webm" });
              recordedPlayback.src = URL.createObjectURL(finalRecordedBlob);
              layer2PlayBtn.disabled = false;
              layer2PlayBtn.style.color = "#ef4444";
              layer2PlayBtn.style.borderColor = "#ef4444";
              layer2PlayBtn.style.background = "#232538";
              if (microphoneStream) {
                microphoneStream.getTracks().forEach(track => track.stop());
              }
            };
            mediaRecorder.start(100);
          }

          if (isL1Checked && backingAudio) {
            backingAudio.currentTime = 0;
            backingAudio.play().catch(e => console.log("Backing play error:", e));
            if (layer1PlayBtn) layer1PlayBtn.innerText = "⏸ Pause";
            layer1StopBtn.disabled = false;
            layer1StopBtn.style.color = "#a855f7";
            layer1StopBtn.style.borderColor = "#a855f7";
          }

          startTime = Date.now();
          if (timerInterval) clearInterval(timerInterval);
          timerInterval = setInterval(updateTimer, 50);
          startBtn.style.boxShadow = "0 0 20px #ef4444";
          stopBtn.style.borderColor = "#ef4444";
          stopBtn.style.background = "#7f1d1d";
          stopBtn.disabled = false;
          statusDisplay.innerText = isL2Checked ? "Recording..." : "Playing Track...";
          statusDisplay.style.color = "#ef4444";
        } catch(err) {
          alert("Microphone permission blocked or not allowed. Check browser settings.");
        }
      };
    }

    if (stopBtn) {
      stopBtn.onclick = () => {
        if (mediaRecorder && mediaRecorder.state !== "inactive") {
          mediaRecorder.requestData();
          mediaRecorder.stop();
        }
        if (backingAudio) {
          backingAudio.pause();
          backingAudio.currentTime = 0;
          if (layer1PlayBtn) layer1PlayBtn.innerText = "▶ Play";
          if (layer1StopBtn) {
            layer1StopBtn.disabled = true;
            layer1StopBtn.style.color = "#64748b";
            layer1StopBtn.style.borderColor = "#475569";
          }
        }
        if (timerInterval) {
          clearInterval(timerInterval);
          timerInterval = null;
        }
        
        saveModal.style.display = "flex";
      };
    }

    saveNoBtn.onclick = () => {
      saveModal.style.display = "none";
      timerDisplay.innerText = "00:00.00";
      startBtn.style.boxShadow = "0 0 12px rgba(239,68,68,0.6)";
      stopBtn.style.background = "#1e293b";
      stopBtn.style.borderColor = "#475569";
      stopBtn.disabled = true;
      statusDisplay.innerText = "Discarded";
      statusDisplay.style.color = "#94a3b8";
      drawVoiceWaveform(0);
    };

    saveYesBtn.onclick = async () => {
      saveModal.style.display = "none";
      timerDisplay.innerText = "00:00.00";
      startBtn.style.boxShadow = "0 0 12px rgba(239,68,68,0.6)";
      stopBtn.style.background = "#1e293b";
      stopBtn.style.borderColor = "#475569";
      stopBtn.disabled = true;
      statusDisplay.innerText = "Mixing & Saved!";
      statusDisplay.style.color = "#10b981";
      drawVoiceWaveform(1);

      try {
        const trackVolVal = (document.getElementById("trackVol").value / 100);
        const micVolVal = (document.getElementById("micVol").value / 100);

        const mixCtx = new (window.AudioContext || window.webkitAudioContext)();
        let trackBuffer = null;
        let voiceBuffer = null;

        if (backingAudio && backingAudio.src && enableLayer1Chk.checked) {
          const resp = await fetch(backingAudio.src);
          const buf = await resp.arrayBuffer();
          trackBuffer = await mixCtx.decodeAudioData(buf);
        }

        if (finalRecordedBlob && enableLayer2Chk.checked) {
          const resp = await fetch(URL.createObjectURL(finalRecordedBlob));
          const buf = await resp.arrayBuffer();
          voiceBuffer = await mixCtx.decodeAudioData(buf);
        }

        let maxDuration = 0;
        if (trackBuffer) maxDuration = Math.max(maxDuration, trackBuffer.duration);
        if (voiceBuffer) maxDuration = Math.max(maxDuration, voiceBuffer.duration);

        if (maxDuration > 0) {
          const offlineCtx = new OfflineAudioContext(2, mixCtx.sampleRate * maxDuration, mixCtx.sampleRate);

          if (trackBuffer) {
            const s1 = offlineCtx.createBufferSource();
            s1.buffer = trackBuffer;
            const gain1 = offlineCtx.createGain();
            gain1.gain.value = trackVolVal;
            s1.connect(gain1);
            gain1.connect(offlineCtx.destination);
            s1.start(0);
          }

          if (voiceBuffer) {
            let maxPeak = 0;
            for (let c = 0; c < voiceBuffer.numberOfChannels; c++) {
              const data = voiceBuffer.getChannelData(c);
              for (let i = 0; i < data.length; i++) {
                const abs = Math.abs(data[i]);
                if (abs > maxPeak) maxPeak = abs;
              }
            }
            let autoBoostRatio = 1.0;
            if (maxPeak > 0 && maxPeak < 0.8) {
              autoBoostRatio = 0.92 / maxPeak;
            }

            const s2 = offlineCtx.createBufferSource();
            s2.buffer = voiceBuffer;
            const gain2 = offlineCtx.createGain();
            gain2.gain.value = micVolVal * autoBoostRatio;
            s2.connect(gain2);
            gain2.connect(offlineCtx.destination);
            s2.start(0);
          }

          const renderedBuffer = await offlineCtx.startRendering();
          const wavBlob = bufferToWaveBlob(renderedBuffer, mixCtx.sampleRate);
          const mixedUrl = URL.createObjectURL(wavBlob);

          mixedPlayback.src = mixedUrl;

          let customName = mixedFileNameInput.value.trim() || "voice_record.wav";
          downloadMixedBtn.download = customName;
          downloadMixedBtn.href = mixedUrl;
          mixedResultContainer.style.display = "block";
        }
      } catch (err) {
        console.log("Mixing error:", err);
      }
    };

    function bufferToWaveBlob(abBuffer, sampleRate) {
      const numOfChan = abBuffer.numberOfChannels;
      const length = abBuffer.length * numOfChan * 2 + 44;
      const out = new DataView(new ArrayBuffer(length));
      let channels = [];
      let sample;
      let offset = 0;
      let pos = 0;

      function writeString(str) {
        for (let i = 0; i < str.length; i++) {
          out.setUint8(pos++, str.charCodeAt(i));
        }
      }

      writeString('RIFF');
      out.setUint32(pos, length - 8, true); pos += 4;
      writeString('WAVE');
      writeString('fmt ');
      out.setUint32(pos, 16, true); pos += 4;
      out.setUint16(pos, 1, true); pos += 2;
      out.setUint16(pos, numOfChan, true); pos += 2;
      out.setUint32(pos, sampleRate, true); pos += 4;
      out.setUint32(pos, sampleRate * 2 * numOfChan, true); pos += 4;
      out.setUint16(pos, numOfChan * 2, true); pos += 2;
      out.setUint16(pos, 16, true); pos += 2;
      writeString('data');
      out.setUint32(pos, length - pos - 4, true); pos += 4;

      for (let i = 0; i < abBuffer.numberOfChannels; i++) {
        channels.push(abBuffer.getChannelData(i));
      }

      while (pos < length) {
        for (let i = 0; i < numOfChan; i++) {
          sample = Math.max(-1, Math.min(1, channels[i][offset]));
          sample = (0.5 + sample < 0 ? sample * 32768 : sample * 32767)|0;
          out.setInt16(pos, sample, true);
          pos += 2;
        }
        offset++;
      }

      return new Blob([out.buffer], { type: 'audio/wav' });
    }

    const trackVol = document.getElementById("trackVol");
    if(trackVol) {
      trackVol.oninput = (e) => {
        document.getElementById("trackVolVal").innerText = e.target.value + "%";
        if(backingAudio) backingAudio.volume = e.target.value / 100;
      };
    }
    const micVol = document.getElementById("micVol");
    if(micVol) {
      micVol.oninput = (e) => {
        document.getElementById("micVolVal").innerText = e.target.value + "%";
      };
    }
    </script>
    """

    studio_html = studio_html.replace("TRACK_AUDIO_PLACEHOLDER", track_audio_html)
    components.html(studio_html, height=470)

with right_col:
    st.markdown('<div class="studio-step-label">3. StemTube & YouTube Downloader</div>', unsafe_allow_html=True)
    
    st.link_button(
        "▶️ Open StemTube Web App", "https://www.youtube.com", use_container_width=True
    )

    url_col, paste_btn_col = st.columns([3.2, 1], vertical_alignment="bottom")
    with url_col:
        youtube_url = st.text_input(
            "YouTube URL:",
            value=st.session_state.youtube_url_val,
            placeholder="Paste YouTube Link...",
            label_visibility="collapsed",
            key="yt_input_field",
        )
    with paste_btn_col:
        if st.button("Paste", use_container_width=True):
            paste_code = """
            <script>
            try {
                navigator.clipboard.readText().then(text => {
                    const input = parent.document.querySelectorAll('input[type="text"]');
                    for (let el of input) {
                        if (el.value !== undefined) {
                            el.value = text;
                            el.dispatchEvent(new Event('input', { bubbles: true }));
                        }
                    }
                }).catch(err => {
                    console.log('Clipboard access denied.');
                });
            } catch(e) {
                console.log('Parent frame access blocked.');
            }
            </script>
            """
            components.html(paste_code, height=0)
            st.rerun()

    st.markdown('<div style="margin-top:4px;"></div>', unsafe_allow_html=True)

    # --- FORMAT & QUALITY OPTIONS ---
    format_type = st.radio(
        "Output Format:", ["MP3 Audio", "WAV Audio", "MP4 Video", "FLAC Lossless"], horizontal=True
    )

    if "Audio" in format_type or format_type == "FLAC Lossless":
        quality_options = [
            "320 kbps (Ultra Studio Quality)",
            "256 kbps (High Quality Audio)",
            "192 kbps (Standard Quality)",
            "128 kbps (Compact Web Audio)",
        ]
    else:
        quality_options = ["1080p (Full HD)", "720p (HD)", "480p (SD)", "360p (Low Res)"]

    selected_quality = st.selectbox("Audio/Video Quality:", quality_options)

    # --- AUDIO EFFECTS, VOICE CHANGER, TRANSPOSE & TEMPO (MOVED UP ABOVE DOWNLOAD) ---
    eff_col1, eff_col2 = st.columns(2)
    with eff_col1:
        effect_type = st.selectbox(
            "Audio Effect Preset:",
            ["None (Clean)", "Studio Vocal Warmth", "Echo & Reverb", "Radio Broadcast", "Deep Bass Boost"],
            key="rec_effect_type"
        )
    with eff_col2:
        voice_changer_mode = st.selectbox(
            "Voice Changer / Pitch Profile:",
            ["Original Voice", "Chipmunk / High Pitch", "Deep / Monster", "Robot FX", "Radio Transceiver"],
            key="rec_voice_changer"
        )

    transpose_val = st.slider(
        "Transpose Semitones", -12, 12, 0, key="transpose_slider"
    )
    tempo_val = st.slider("Tempo / Speed", 0.5, 2.0, 1.0, 0.1, key="tempo_slider")

    st.markdown('<div style="margin-top:4px;"></div>', unsafe_allow_html=True)

    dl_progress_container = st.empty()

    btn_label = st.session_state.dl_button_mode
    if st.button(
        btn_label, use_container_width=True, key="main_download_trigger_btn"
    ):
        if st.session_state.dl_button_mode == "Download":
            if not youtube_url:
                st.warning("YouTube link rawn dah hmasa rawh.")
            elif yt_dlp is None:
                st.error("Terminal-ah `pip install yt-dlp` ti rawh.")
            else:
                st.session_state.dl_button_mode = "Cancel"
                st.rerun()

        elif st.session_state.dl_button_mode == "Cancel":
            st.session_state.dl_button_mode = "Download"
            st.info("Download cancelled.")
            st.rerun()

        elif st.session_state.dl_button_mode == "Complete":
            st.session_state.dl_button_mode = "Download"
            st.rerun()

    st.markdown('<div style="margin-top:6px;"></div>', unsafe_allow_html=True)

    if (
        st.session_state.dl_button_mode == "Complete"
        and st.session_state.temp_dl_bytes
    ):
        st.download_button(
            label="💾 Save File to Device",
            data=st.session_state.temp_dl_bytes,
            file_name=st.session_state.temp_dl_name,
            mime=(
                "audio/mpeg" if st.session_state.temp_dl_name.endswith(".mp3")
                else "audio/wav" if st.session_state.temp_dl_name.endswith(".wav")
                else "audio/flac" if st.session_state.temp_dl_name.endswith(".flac")
                else "video/mp4"
            ),
            use_container_width=True,
        )

    if st.session_state.dl_button_mode == "Cancel" and youtube_url:
        progress_bar = dl_progress_container.progress(
            0, text="⚡ Downloading..."
        )

        def progress_hook(d):
            if d["status"] == "downloading":
                total = d.get("total_bytes") or d.get("total_bytes_estimate", 0)
                downloaded = d.get("downloaded_bytes", 0)
                if total > 0:
                    pct = int((downloaded / total) * 100)
                    pct = max(1, min(99, pct))
                    progress_bar.progress(pct, text=f"⚡ Downloading {pct}%")
                else:
                    progress_bar.progress(50, text="⚡ Downloading...")
            elif d["status"] == "finished":
                progress_bar.progress(100, text="✅ Complete")

        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                out_path = os.path.join(tmpdir, "youtube_media.%(ext)s")

                is_video = "Video" in format_type
                if not is_video:
                    if "320" in selected_quality:
                        bitrate = "320"
                    elif "256" in selected_quality:
                        bitrate = "256"
                    elif "192" in selected_quality:
                        bitrate = "192"
                    else:
                        bitrate = "128"

                    codec_ext = "mp3"
                    if "WAV" in format_type:
                        codec_ext = "wav"
                    elif "FLAC" in format_type:
                        codec_ext = "flac"

                    ydl_opts = {
                        "format": "bestaudio/best",
                        "outtmpl": out_path,
                        "quiet": True,
                        "no_warnings": True,
                        "progress_hooks": [progress_hook],
                        "postprocessors": [{
                            "key": "FFmpegExtractAudio",
                            "preferredcodec": codec_ext,
                            "preferredquality": bitrate,
                        }],
                        "socket_timeout": 15,
                        "nocheckcertificate": True,
                    }
                else:
                    res = "720"
                    if "1080p" in selected_quality:
                        res = "1080"
                    elif "480p" in selected_quality:
                        res = "480"
                    elif "360p" in selected_quality:
                        res = "360"

                    ydl_opts = {
                        "format": f"bestvideo[height<={res}]+bestaudio/best[height<={res}]/best",
                        "outtmpl": out_path,
                        "quiet": True,
                        "no_warnings": True,
                        "progress_hooks": [progress_hook],
                        "socket_timeout": 15,
                        "nocheckcertificate": True,
                    }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(youtube_url, download=True)
                    filename = ydl.prepare_filename(info)
                    if not is_video:
                        codec_ext = "mp3"
                        if "WAV" in format_type:
                            codec_ext = "wav"
                        elif "FLAC" in format_type:
                            codec_ext = "flac"
                        filename = os.path.splitext(filename)[0] + f".{codec_ext}"

                if os.path.exists(filename):
                    if not is_video and (transpose_val != 0 or tempo_val != 1.0 or effect_type != "None (Clean)" or voice_changer_mode != "Original Voice"):
                        progress_bar.progress(
                            95, text="🎵 Applying Effects & Voice Transformation..."
                        )
                        audio = AudioSegment.from_file(filename)

                        effective_transpose = transpose_val
                        if voice_changer_mode == "Chipmunk / High Pitch":
                            effective_transpose += 6
                        elif voice_changer_mode == "Deep / Monster":
                            effective_transpose -= 5

                        if tempo_val != 1.0:
                            new_fr = int(audio.frame_rate * tempo_val)
                            audio = audio._spawn(audio.raw_data, overrides={"frame_rate": new_fr})
                            audio = audio.set_frame_rate(44100)

                        if effective_transpose != 0:
                            factor = 2 ** (effective_transpose / 12.0)
                            new_fr = int(audio.frame_rate * factor)
                            audio = audio._spawn(audio.raw_data, overrides={"frame_rate": new_fr})
                            audio = audio.set_frame_rate(44100)

                        if effect_type == "Studio Vocal Warmth":
                            audio = audio.low_pass_filter(5000).high_pass_filter(80)
                        elif effect_type == "Echo & Reverb":
                            audio = audio.overlay(audio - 6, position=120).overlay(audio - 12, position=240)
                        elif effect_type == "Radio Broadcast":
                            audio = audio.high_pass_filter(300).low_pass_filter(3400)
                        elif effect_type == "Deep Bass Boost":
                            audio = audio.low_pass_filter(250)

                        export_codec = "mp3"
                        if "WAV" in format_type:
                            export_codec = "wav"
                        elif "FLAC" in format_type:
                            export_codec = "flac"

                        filename = os.path.splitext(filename)[0] + f".{export_codec}"
                        audio.export(filename, format=export_codec)

                    with open(filename, "rb") as f:
                        downloaded_bytes = f.read()

                    ext = os.path.splitext(filename)[1].lower()
                    safe_title = "".join([
                        c
                        for c in info.get("title", "YouTube_Media")
                        if c.isalpha() or c.isdigit() or c == " "
                    ]).rstrip()
                    final_name = f"{safe_title}{ext}"

                    st.session_state.temp_dl_bytes = downloaded_bytes
                    st.session_state.temp_dl_name = final_name

                    st.session_state.imported_track = downloaded_bytes
                    st.session_state.last_imported_name = final_name

                    st.session_state.dl_button_mode = "Complete"

                    time.sleep(1.0)
                    progress_bar.empty()
                    dl_progress_container.success(
                        f"✅ {final_name} download a ni a, Layer 1-ah a lut nghal e!"
                    )
                    st.rerun()
                else:
                    dl_progress_container.empty()
                    st.error("Media file a bo.")
                    st.session_state.dl_button_mode = "Download"
                    st.rerun()
        except Exception as e:
            dl_progress_container.empty()
            error_msg = str(e)
            if (
                "not available" in error_msg.lower()
                or "private" in error_msg.lower()
            ):
                st.error("❌ He video hi Private a ni.")
            else:
                st.error(f"❌ Harsatna: {error_msg}")
            st.session_state.dl_button_mode = "Download"
            st.rerun()

    if st.session_state.show_download_btn and st.session_state.imported_track:
        st.markdown('<div style="margin-top:4px;"></div>', unsafe_allow_html=True)

        mime_type = (
            "audio/mpeg"
            if st.session_state.last_imported_name.endswith(".mp3")
            else "video/mp4"
        )

        st.download_button(
            label="⬇️ Save / Drag & Drop File",
            data=st.session_state.imported_track,
            file_name=st.session_state.last_imported_name,
            mime=mime_type,
            use_container_width=True,
        )