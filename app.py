import streamlit as st
from yt_dlp import YoutubeDL

import utils
from uuid import uuid4
from streamlit_local_storage import LocalStorage

localStorage = LocalStorage()
if 'uuid' not in st.session_state:
    st.session_state.uuid = localStorage.getItem('uuid') or str(uuid4())
    localStorage.setItem('uuid', st.session_state.uuid)

st.title('DownloadHub')
url = st.text_input('Video URL', placeholder='Enter video URL: YouTube or TikTok')

def progress_hook(d):
    """Function to update the progress bar"""
    if d['status'] == 'downloading':
        if 'total_bytes' in d:
            progress = d['downloaded_bytes'] / d['total_bytes']
            progress_bar.progress(progress)
            status_text.text(f"Downloaded: {d['downloaded_bytes']:,} / {d['total_bytes']:,} bytes ({progress:.1%})")
        elif 'total_bytes_estimate' in d:
            progress = d['downloaded_bytes'] / d['total_bytes_estimate']
            progress_bar.progress(min(progress, 1.0))
            status_text.text(f"Downloaded: {d['downloaded_bytes']:,} bytes (approx. {progress:.1%})")
        else:
            status_text.text(f"Downloaded: {d['downloaded_bytes']:,} bytes")
    elif d['status'] == 'finished':
        progress_bar.progress(1.0)
        status_text.success(f"✅ Download complete: {d['filename']}")

if st.button('Download'):
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': f'{st.session_state.uuid}.%(ext)s',
        'quiet': True,
        'overwrites': True,
        'merge_output_format': 'mp4',
        'progress_hooks': [progress_hook]
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            status_text.info("🔍 Retrieving video information...")
            info = ydl.extract_info(url.strip(), download=False)
            file_ext = info.get('ext', 'mp4')
            thumbnail_url = info.get('thumbnail')
            video_title = info.get('title', 'Unknown video')
            video_duration = info.get('duration', 'N/A')
            status_text.info(f"📹 Starting download: {video_title}")
            
            # Download the video
            ydl.download([url.strip()])
            utils.dialog(thumbnail_url, file_ext, f'{st.session_state.uuid}.{file_ext}')
            
    except Exception as e:
        progress_bar.empty()
        status_text.error(f"❌ Error during download: {str(e)}")

st.divider()
preview = st.empty()
button_dwlp = st.empty()