import streamlit as st
import os
import subprocess
import shutil
from pathlib import Path
import platform
import urllib.request
import tarfile
import stat

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
                    # Try to ensure ffmpeg exists. On Streamlit Cloud we can
                    # download a static ffmpeg binary for Linux x86_64 at runtime.
                    def ensure_ffmpeg():
                        if shutil.which("ffmpeg"):
                            return True
                        # Only attempt automatic download on Linux x86_64
                        sys = platform.system().lower()
                        machine = platform.machine().lower()
                        if sys != "linux" or ("64" not in machine and machine != "x86_64"):
                            return False

                        ff_dir = os.path.join(".ffmpeg")
                        ff_bin = os.path.join(ff_dir, "ffmpeg")
                        if os.path.exists(ff_bin) and os.access(ff_bin, os.X_OK):
                            os.environ["PATH"] = ff_dir + os.pathsep + os.environ.get("PATH", "")
                            return True

                        try:
                            os.makedirs(ff_dir, exist_ok=True)
                            url = "https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz"
                            archive_path = os.path.join(ff_dir, "ffmpeg-static.tar.xz")
                            urllib.request.urlretrieve(url, archive_path)
                            # Extract
                            with tarfile.open(archive_path, "r:xz") as tar:
                                members = tar.getmembers()
                                # find ffmpeg binary path inside archive
                                ff_member = None
                                for m in members:
                                    if os.path.basename(m.name) == "ffmpeg":
                                        ff_member = m
                                        break
                                if ff_member is None:
                                    return False
                                tar.extract(ff_member, path=ff_dir)
                                extracted_path = os.path.join(ff_dir, ff_member.name)
                                # Move binary to ff_dir root
                                final_bin = ff_bin
                                os.replace(extracted_path, final_bin)
                                os.chmod(final_bin, os.stat(final_bin).st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
                                os.environ["PATH"] = ff_dir + os.pathsep + os.environ.get("PATH", "")
                                return True
                        except Exception:
                            return False

                    ffmpeg_available = ensure_ffmpeg()

                    if ffmpeg_available:
                        format_option = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best[ext=mp4]/best"
                        sort_args = ["-S", "res,fps,codec:h264:m4a"]
                    else:
                        st.warning("FFmpeg not available and automatic install failed — falling back to single-file downloads (may be lower quality).")
                        format_option = "best[ext=mp4]/best"
                        sort_args = []

                    # Build yt-dlp command with appropriate flags
                    if download_type == "Playlist":
                        command = [
                            "yt-dlp",
                            "-f", format_option,
                        ] + sort_args + [
                            "-o", f"{downloads_dir}/%(playlist_title)s/%(title)s.%(ext)s",
                            "--no-part",
                            "--continue",
                            url
                        ]
                    else:
                        command = [
                            "yt-dlp",
                            "-f", format_option,
                        ] + sort_args + [
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
        # On Streamlit Cloud (or other remote hosts) opening a local folder
        # with `open` is not possible. Provide a ZIP download of the
        # `downloads/` folder instead so users can download files from the app.
        if not os.path.exists(downloads_dir):
            st.warning("No downloads available")
        else:
            try:
                import zipfile

                zip_path = os.path.join(downloads_dir, "all_downloads.zip")
                # Create or overwrite the zip file
                with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
                    for root, dirs, files in os.walk(downloads_dir):
                        for f in files:
                            # skip the zip itself if present
                            if f == "all_downloads.zip":
                                continue
                            file_path = os.path.join(root, f)
                            arcname = os.path.relpath(file_path, downloads_dir)
                            zf.write(file_path, arcname)

                # Serve the zip to the user
                with open(zip_path, "rb") as fh:
                    data = fh.read()
                    st.download_button("📥 Download all files (ZIP)", data, file_name="downloads.zip")
                st.success("📁 Prepared ZIP for download")
            except Exception as e:
                st.warning(f"Could not prepare ZIP: {str(e)}")

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
