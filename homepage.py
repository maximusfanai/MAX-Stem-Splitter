import streamlit as st

st.set_page_config(
    page_title="MizoAudioAI",
    page_icon="🎵",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Custom Mobile-App Style CSS & Gradients
st.markdown(
    """
    <style>
    .stApp {
        background-color: #07080e !important;
        color: #ffffff !important;
        font-family: 'Segoe UI', system-ui, sans-serif;
    }
    div[data-testid='stSidebarNav'] { display: none !important; }
    
    /* Header Styles */
    .header-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 16px;
        padding-top: 5px;
    }
    .brand-title {
        font-size: 20px;
        font-weight: 900;
        color: #ffffff;
        letter-spacing: 0.5px;
    }
    .brand-subtitle {
        font-size: 9px;
        color: #94a3b8;
        font-weight: bold;
        letter-spacing: 1px;
    }
    .pro-badge {
        background: linear-gradient(135deg, #eab308 0%, #ca8a04 100%);
        color: #ffffff;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 10px;
        font-weight: 900;
        border: 1px solid #facc15;
    }

    /* Hero Banner Card */
    .hero-card {
        background: linear-gradient(135deg, #1e1b4b 0%, #31103f 50%, #0f172a 100%);
        border: 1px solid #6d28d9;
        border-radius: 16px;
        padding: 18px;
        margin-bottom: 14px;
        box-shadow: 0 8px 25px rgba(109, 40, 217, 0.25);
    }

    /* Grid Cards Styling */
    .card-project {
        background: linear-gradient(145deg, #0f172a 0%, #090d16 100%);
        border: 1px solid #1e3a8a;
        border-radius: 14px;
        padding: 14px;
        margin-bottom: 10px;
        min-height: 110px;
    }
    .card-splitter {
        background: linear-gradient(145deg, #2e1065 0%, #0f071f 100%);
        border: 1px solid #7c3aed;
        border-radius: 14px;
        padding: 14px;
        margin-bottom: 10px;
        min-height: 110px;
    }
    .card-recorder {
        background: linear-gradient(145deg, #022c22 0%, #061210 100%);
        border: 1px solid #0d9488;
        border-radius: 14px;
        padding: 14px;
        margin-bottom: 10px;
        min-height: 110px;
    }
    .card-stemtube {
        background: linear-gradient(145deg, #450a0a 0%, #180505 100%);
        border: 1px solid #dc2626;
        border-radius: 14px;
        padding: 14px;
        margin-bottom: 10px;
        min-height: 110px;
    }
    .card-small {
        background: linear-gradient(145deg, #111827 0%, #0b0f19 100%);
        border: 1px solid #1f2937;
        border-radius: 12px;
        padding: 12px;
        margin-bottom: 10px;
        min-height: 80px;
    }

    /* Streamlit Button Customization for Card Triggers */
    div.stButton > button {
        background: transparent !important;
        border: none !important;
        color: #38bdf8 !important;
        font-size: 12px !important;
        font-weight: bold !important;
        text-align: left !important;
        padding: 0 !important;
        margin-top: 6px !important;
    }
    div.stButton > button:hover {
        color: #ffffff !important;
    }
    
    .hero-btn > button {
        background: linear-gradient(135deg, #0284c7 0%, #2563eb 100%) !important;
        border: 1px solid #60a5fa !important;
        border-radius: 8px !important;
        color: #ffffff !important;
        padding: 6px 16px !important;
        font-weight: bold !important;
        text-align: center !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Top Bar Header
st.markdown(
    """
    <div class="header-container">
        <div style="display: flex; align-items: center;">
            <span style="font-size: 22px; margin-right: 8px;">🎛️</span>
            <div>
                <div class="brand-title">MizoAudioAI</div>
                <div class="brand-subtitle">STEM SPLITTER & AUDIO STUDIO</div>
            </div>
        </div>
        <div style="display: flex; align-items: center; gap: 8px;">
            <div class="pro-badge">⭐ PRO</div>
            <div style="background: #1e293b; padding: 6px 10px; border-radius: 50%; font-size: 14px;">👤</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Hero Banner
st.markdown(
    """
    <div class="hero-card">
        <div style="font-size: 9px; color: #cbd5e1; letter-spacing: 1px; margin-bottom: 4px; font-weight: bold;">SEPARATE &bull; ENHANCE &bull; CREATE</div>
        <div style="font-size: 19px; font-weight: 900; color: #ffffff; margin-bottom: 6px;">AI-Powered Stem Separation</div>
        <div style="font-size: 11px; color: #94a3b8; margin-bottom: 12px; line-height: 1.4;">Extract vocals, drums, bass, guitar and more with crystal clear quality.</div>
    </div>
    """,
    unsafe_allow_html=True,
)

col_hero = st.columns(1)
with col_hero[0]:
  st.markdown('<div class="hero-btn">', unsafe_allow_html=True)
  if st.button("✨ Get Started ➔", use_container_width=True, key="get_started"):
    st.switch_page("pages/stem_splitter.py")
  st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='margin-top: 14px;'></div>", unsafe_allow_html=True)

# Row 1: Project & Stem Splitter
c1, c2 = st.columns(2)
with c1:
  st.markdown(
      """
        <div class="card-project">
            <div style="font-size: 18px; margin-bottom: 6px;">📁</div>
            <div style="font-size: 13px; font-weight: bold; color: #ffffff;">Project</div>
            <div style="font-size: 10px; color: #94a3b8; margin-top: 2px;">Manage your audio projects and files.</div>
        </div>
        """,
      unsafe_allow_html=True,
  )
  if st.button("Open Project ➔", key="b_proj"):
    st.switch_page("pages/projects.py")

with c2:
  st.markdown(
      """
        <div class="card-splitter">
            <div style="font-size: 18px; margin-bottom: 6px;">🎛️</div>
            <div style="font-size: 13px; font-weight: bold; color: #ffffff;">Stem Splitter</div>
            <div style="font-size: 10px; color: #94a3b8; margin-top: 2px;">Split vocals, drums, bass, guitar.</div>
        </div>
        """,
      unsafe_allow_html=True,
  )
  if st.button("Open Splitter ➔", key="b_split"):
    st.switch_page("pages/stem_splitter.py")

# Row 2: Voice Recorder & StemTube
c3, c4 = st.columns(2)
with c3:
  st.markdown(
      """
        <div class="card-recorder">
            <div style="font-size: 18px; margin-bottom: 6px;">🎙️</div>
            <div style="font-size: 13px; font-weight: bold; color: #ffffff;">Voice Recorder</div>
            <div style="font-size: 10px; color: #94a3b8; margin-top: 2px;">Record, edit and save your voice.</div>
        </div>
        """,
      unsafe_allow_html=True,
  )
  if st.button("Open Recorder ➔", key="b_rec"):
    st.switch_page("pages/voice_recorder.py")

with c4:
  st.markdown(
      """
        <div class="card-stemtube">
            <div style="font-size: 18px; margin-bottom: 6px;">📥</div>
            <div style="font-size: 13px; font-weight: bold; color: #ffffff;">StemTube</div>
            <div style="font-size: 10px; color: #94a3b8; margin-top: 2px;">Find and download stems from YouTube.</div>
        </div>
        """,
      unsafe_allow_html=True,
  )
  if st.button("Open StemTube ➔", key="b_tube"):
    st.switch_page("pages/stemtube.py")

# Row 3: Noise Reduction, Recent Files, Cloud Drive (3 columns)
rc1, rc2, rc3 = st.columns(3)
with rc1:
  st.markdown(
      """
        <div class="card-small">
            <div style="font-size: 14px; margin-bottom: 4px;">🔇</div>
            <div style="font-size: 11px; font-weight: bold; color: #ffffff;">Noise Reduction</div>
        </div>
        """,
      unsafe_allow_html=True,
  )
  if st.button("Open ➔", key="b_noise"):
    st.switch_page("pages/noise_reduction.py")

with rc2:
  st.markdown(
      """
        <div class="card-small">
            <div style="font-size: 14px; margin-bottom: 4px;">🕒</div>
            <div style="font-size: 11px; font-weight: bold; color: #ffffff;">Recent Files</div>
        </div>
        """,
      unsafe_allow_html=True,
  )
  if st.button("Open ➔", key="b_recent"):
    st.switch_page("pages/recent_files.py")

with rc3:
  st.markdown(
      """
        <div class="card-small">
            <div style="font-size: 14px; margin-bottom: 4px;">☁️</div>
            <div style="font-size: 11px; font-weight: bold; color: #ffffff;">Cloud Drive</div>
        </div>
        """,
      unsafe_allow_html=True,
  )
  if st.button("Open ➔", key="b_cloud"):
    st.switch_page("pages/cloud_drive.py")

# Row 4: Remastering & Setting
sc1, sc2 = st.columns(2)
with sc1:
  st.markdown(
      """
        <div class="card-small">
            <div style="font-size: 14px; margin-bottom: 4px;">✨</div>
            <div style="font-size: 11px; font-weight: bold; color: #ffffff;">Remastering</div>
        </div>
        """,
      unsafe_allow_html=True,
  )
  if st.button("Open ➔", key="b_remaster"):
    st.switch_page("pages/remastering.py")

with sc2:
  st.markdown(
      """
        <div class="card-small">
            <div style="font-size: 14px; margin-bottom: 4px;">⚙️</div>
            <div style="font-size: 11px; font-weight: bold; color: #ffffff;">Setting</div>
        </div>
        """,
      unsafe_allow_html=True,
  )
  if st.button("Open ➔", key="b_setting"):
    st.switch_page("pages/settings.py")

# Bottom Navigation Bar Simulation
st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
st.markdown(
    """
    <div style="display: flex; justify-content: space-around; background-color: #0c0f1d; border-top: 1px solid #1e293b; padding: 10px 0; border-radius: 12px;">
        <div style="text-align: center; color: #a855f7; font-size: 11px; font-weight: bold;">🏠<br>Home</div>
        <div style="text-align: center; color: #64748b; font-size: 11px;">📁<br>Projects</div>
        <div style="text-align: center; color: #64748b; font-size: 11px;">🎵<br>Library</div>
        <div style="text-align: center; color: #64748b; font-size: 11px;">⚙️<br>More</div>
    </div>
    """,
    unsafe_allow_html=True,
)