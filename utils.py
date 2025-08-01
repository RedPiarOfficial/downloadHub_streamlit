import streamlit as st
import mimetypes
from uuid import uuid4
import os

@st.dialog('Video Confirm')
def dialog(preview, file_ext, video_name):
    st.image(preview, caption="preview", width=200)
    with open(video_name, 'rb') as file:
        mime_type, encoding = mimetypes.guess_type(video_name)
        with st.spinner('loading...'):
            st.download_button('Download video', file.read(), str(uuid4()) + f'.{file_ext}', mime=mime_type)