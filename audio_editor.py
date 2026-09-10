import os
import streamlit as st
from pydub import AudioSegment

st.markdown("""
<style>
    .editor-container {
        background: #10121d;
        border: 1px solid #1c1e2d;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
    }
    .editor-title {
        color: #a855f7;
        font-size: 18px;
        font-weight: 800;
        margin-bottom: 15px;
        letter-spacing: 0.5px;
    }
    .stButton > button {
        background: linear-gradient(135deg, #7c3aed 0%, #5b21b6 100%) !important;
        color: #ffffff !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 10px 20px !important;
        box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="editor-container">', unsafe_allow_html=True)
st.markdown('<div class="editor-title">✂️ KINEMASTER STYLE AUDIO SPLITTER</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("Audio file rawn upload rawh (MP3, WAV)", type=["mp3", "wav"])

if uploaded_file is not None:
    try:
        audio = AudioSegment.from_file(uploaded_file)
        duration_sec = len(audio) / 1000.0
        
        st.audio(uploaded_file)
        st.markdown(f"<div style='color:#10b981; font-size:13px; font-weight:600; margin-top:10px;'>🎵 Total Length: {duration_sec:.2f} seconds</div>", unsafe_allow_html=True)
        
        st.markdown("<hr style='border-color: #22263d;'>", unsafe_allow_html=True)
        st.markdown("<div style='color:#ffffff; font-weight:bold; margin-bottom:10px;'>Split Position (Playhead)</div>", unsafe_allow_html=True)
        
        # Kinemaster ang a a lai taka then hran na (Split position)
        split_sec = st.slider("Hmun la lai then hrang tur (Seconds)", 0.1, duration_sec - 0.1, duration_sec / 2, 0.1)
        
        st.markdown(f"<div style='color:#a855f7; font-size:12px;'>A thenna tur hun: <b>{split_sec:.2f}s</b> (Part 1: 0s - {split_sec:.2f}s | Part 2: {split_sec:.2f}s - {duration_sec:.2f}s)</div>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("✂️ SPLIT AUDIO (PAHNIHAH THEN HRAN)", use_container_width=True):
            with st.spinner("Splitting audio..."):
                split_ms = int(split_sec * 1000)
                
                # Kinemaster a split ang chiaha then hrang
                part1 = audio[:split_ms]
                part2 = audio[split_ms:]
                
                output_dir = "downloads"
                os.makedirs(output_dir, exist_ok=True)
                
                path1 = os.path.join(output_dir, "split_part1.mp3")
                path2 = os.path.join(output_dir, "split_part2.mp3")
                
                part1.export(path1, format="mp3")
                part2.export(path2, format="mp3")
                
                st.success("Audio a in-split hrang ta! File hnihin a hnuaiah a awm e:")
                
                col_a, col_b = st.columns(2)
                
                with col_a:
                    st.markdown("#### **Part 1 (A Tir lam)**")
                    st.audio(path1)
                    with open(path1, "rb") as f1:
                        st.download_button(
                            label="📥 Download Part 1",
                            data=f1,
                            file_name="split_part1.mp3",
                            mime="audio/mp3",
                            use_container_width=True,
                            key="btn_part1"
                        )
                        
                with col_b:
                    st.markdown("#### **Part 2 (A Tawp lam)**")
                    st.audio(path2)
                    with open(path2, "rb") as f2:
                        st.download_button(
                            label="📥 Download Part 2",
                            data=f2,
                            file_name="split_part2.mp3",
                            mime="audio/mp3",
                            use_container_width=True,
                            key="btn_part2"
                        )
    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("Audio file upload turin hmet rawh.")

st.markdown('</div>', unsafe_allow_html=True)