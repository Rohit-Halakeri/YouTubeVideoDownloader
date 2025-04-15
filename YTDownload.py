import yt_dlp
import streamlit as st
import os

# Secure password input
correct_password = 'Rohit123'

st.sidebar.title("🔒 Rohit's YouTube Video Downloader 🎥")
email = st.sidebar.text_input("Enter your email address")
password = st.sidebar.text_input("Enter password", type='password')

# State to track login status
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Check login
if st.sidebar.button("Login"):
    if password == correct_password and email:
        st.session_state.logged_in = True
        st.sidebar.success(f"{email} - Welcome 🎉")
        st.sidebar.balloons()
    else:
        st.sidebar.error("Invalid email or password ❌")

# Main content
if st.session_state.logged_in:
    st.title("🎥 YouTube Video Downloader")

    video_url = st.text_input("Paste YouTube URL (works with Shorts too)")

    if st.button("Download"):
        if not video_url.strip():
            st.warning("⚠️ Please enter a valid YouTube URL.")
        else:
            with st.spinner("Downloading..."):
                try:
                    download_dir = "downloads"
                    os.makedirs(download_dir, exist_ok=True)

                    ydl_opts = {
                        'format': 'best',
                        'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
                    }

                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(video_url, download=True)
                        filename = ydl.prepare_filename(info)

                    st.success("✅ Download completed!")
                    st.info(f"📁 Saved to: `{os.path.abspath(filename)}`")

                    with open(filename, "rb") as f:
                        st.download_button(
                            label="⬇️ Download Video to Your Device",
                            data=f,
                            file_name=os.path.basename(filename),
                            mime="video/mp4"
                        )

                except Exception as e:
                    st.error(f"❌ Error occurred: {e}")
else:
    st.warning("🔐 Please log in to access the video downloader.")
