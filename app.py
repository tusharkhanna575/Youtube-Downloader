import streamlit as st
import os
import subprocess
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="YouTube Downloader",
    page_icon="🎬",
    layout="centered"
)

st.title("🎬 YouTube Downloader")
st.write("Download YouTube videos or playlists with ease")

# Create a downloads directory
downloads_dir = "downloads"
Path(downloads_dir).mkdir(exist_ok=True)

# Sidebar configuration
st.sidebar.title("⚙️ Settings")
download_type = st.sidebar.radio(
    "Select download type:",
    options=["Video", "Playlist"],
    help="Choose whether to download a single video or an entire playlist"
)

# Main content area
st.subheader(f"📥 Download {download_type}")

# URL input
url = st.text_input(
    "Paste YouTube URL:",
    placeholder="https://www.youtube.com/watch?v=...",
    help="Enter a YouTube video or playlist URL"
)

# Download button
col1, col2 = st.columns([1, 1])

with col1:
    if st.button("⬇️ Download", use_container_width=True):
        if not url:
            st.error("❌ Please enter a URL")
        else:
            try:
                with st.spinner("⏳ Downloading at maximum quality..."):
                    # Download best quality with proper sorting by resolution
                    format_option = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best[ext=mp4]/best"

                    # Build yt-dlp command with quality prioritization
                    if download_type == "Playlist":
                        command = [
                            "yt-dlp",
                            "-f", format_option,
                            "-S", "res,fps,codec:h264:m4a",
                            "-o", f"{downloads_dir}/%(playlist_title)s/%(title)s.%(ext)s",
                            "--no-part",
                            "--continue",
                            url
                        ]
                    else:
                        command = [
                            "yt-dlp",
                            "-f", format_option,
                            "-S", "res,fps,codec:h264:m4a",
                            "-o", f"{downloads_dir}/%(title)s.%(ext)s",
                            "--no-playlist",
                            "--no-part",
                            url
                        ]

                    # Execute download
                    result = subprocess.run(command, capture_output=True, text=True)
                    
                    if result.returncode == 0:
                        st.success(f"✅ {download_type} downloaded successfully at maximum quality!")
                        st.info(f"📁 Files saved to: `{downloads_dir}/`")
                    else:
                        error_msg = result.stderr
                        if "ffmpeg" in error_msg.lower() or "merger" in error_msg.lower():
                            st.error("❌ FFmpeg is required for merging audio and video. Install it:")
                            st.code("brew install ffmpeg  # macOS")
                        else:
                            st.error(f"❌ Download failed: {error_msg}")

            except FileNotFoundError:
                st.error("❌ yt-dlp is not installed. Please install it using: `pip install yt-dlp`")
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")

with col2:
    if st.button("📂 Open Downloads Folder", use_container_width=True):
        try:
            subprocess.Popen(["open", downloads_dir])
            st.success("📁 Opened downloads folder")
        except Exception as e:
            st.warning(f"Could not open folder: {str(e)}")

# Display downloaded files
st.divider()
st.subheader("📚 Downloaded Files")

if os.path.exists(downloads_dir):
    all_files = []
    for root, dirs, files in os.walk(downloads_dir):
        for file in files:
            file_path = os.path.join(root, file)
            rel_path = os.path.relpath(file_path, downloads_dir)
            all_files.append(rel_path)
    
    if all_files:
        st.success(f"Found {len(all_files)} file(s)")
        for file in sorted(all_files):
            st.write(f"✓ {file}")
    else:
        st.info("No files downloaded yet")
else:
    st.info("No files downloaded yet")

# Footer
st.divider()
st.markdown(
    """
    <div style='text-align: center; color: gray; margin-top: 20px;'>
    <small>Made with ❤️ by Tushar Khana | Respects YouTube Terms of Service</small>
    </div>
    """,
    unsafe_allow_html=True
)
