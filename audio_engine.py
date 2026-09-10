import json
import os
import torch
from pydub import AudioSegment
import streamlit as st

CONFIG_FILE = "config.json"


def get_config():
  """config.json a tangin setting zawng zawng a la khawm ang."""
  default_cfg = {
      "app_theme": "Dark Mode (Default)",
      "export_format": "MP3",
      "export_bitrate": "320 kbps",
      "processing_engine": "CPU (Default)",
      "output_folder": "downloads",
      "auto_cleanup": True,
  }
  if os.path.exists(CONFIG_FILE):
    try:
      with open(CONFIG_FILE, "r") as f:
        default_cfg.update(json.load(f))
    except Exception:
      pass
  return default_cfg


def get_processing_device():
  """Settings-a CPU/GPU thlan a zir in PyTorch/Torch Device ('cuda' or 'cpu') a return ang."""
  cfg = get_config()
  selected_engine = cfg.get("processing_engine", "CPU (Default)")

  if "GPU" in selected_engine:
    if torch.cuda.is_available():
      device = "cuda"
      gpu_name = torch.cuda.get_device_name(0)
      st.toast(f"⚡ Running on GPU Acceleration: {gpu_name}", icon="🚀")
      return device
    else:
      st.warning(
          "⚠️ GPU (CUDA) Support a awm loh avangin CPU hmang a run rih a ni!"
      )
      return "cpu"
  return "cpu"


def process_and_export_stem(
    input_audio_path, stem_name="vocals", custom_output_dir=None
):
  """Format, Bitrate, leh Output Folder Settings-a thlan te a taka hmangin audio file a save ang."""
  cfg = get_config()

  # 1. Format leh Bitrate lakchhuah
  export_fmt = cfg.get("export_format", "MP3").lower()
  raw_bitrate = cfg.get("export_bitrate", "320 kbps")
  bitrate_val = raw_bitrate.split()[0] + "k"  # e.g., '1080k', '720k', '320k'

  # 2. Output Folder Path lakchhuah
  target_dir = custom_output_dir or cfg.get("output_folder", "downloads")
  os.makedirs(target_dir, exist_ok=True)

  output_file_name = f"{stem_name}.{export_fmt}"
  final_output_path = os.path.join(target_dir, output_file_name)

  # 3. Audio Export Convert execution
  audio = AudioSegment.from_file(input_audio_path)

  if export_fmt == "mp3":
    audio.export(final_output_path, format="mp3", bitrate=bitrate_val)
  elif export_fmt == "m4a":
    audio.export(final_output_path, format="ipod", bitrate=bitrate_val)
  elif export_fmt in ["wav", "flac"]:
    audio.export(final_output_path, format=export_fmt)

  return final_output_path