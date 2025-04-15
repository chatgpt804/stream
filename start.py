import subprocess
import os
import time

# Function to run the bash command (your ffmpeg command for streaming)
def run_bash_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f"Error: {stderr.decode()}")
    else:
        print(stdout.decode())

# ----------- CONFIG -----------

VIDEO_URL = "https://nsf-m4c-one-fr-01.sf-converter.com/prod-new/download/eyJtZWRpYUlkIjoiMmZEZkpHczVMN28iLCJ0aXRsZSI6IvCdkIfwnZCa8J2Qni3wnZCj8J2QqCAmIPCdkInwnZCa8J2Qni3wnZCm8J2QoiAtIERpZSBXaXRoIEEgU21pbGUgWyDwnZmI8J2Zpy4g8J2Zi_CdmaHwnZmW8J2Zo_CdmaDwnZmp8J2ZpPCdmaMgXSAja2RyYW1hICNrZHJhbWFlZGl0ICNtcnBsYW5rdG9uIiwiZm9ybWF0IjoibXA0IiwicXVhbGl0eSI6IjcyMCIsInRpbWVzdGFtcCI6MTc0NDcyODcxOX0.e101246462e2f1367ae33f8f6bc2933d"  # Replace with actual video URL
OUTPUT_FILE = "stream.mp4"
INSTAGRAM_URL = os.getenv("INSTAGRAM_URL")  # Get the Instagram RTMP URL from environment variable
RESOLUTION = "720x1280"
BITRATE = "2500k"

if not INSTAGRAM_URL:
    print("⚠️ Instagram RTMP URL not found in environment variable!")
    exit(1)

# ----------- DOWNLOAD VIDEO -----------

print("📥 Downloading video from Google Drive...")
run_bash_command(f"wget -O original.mp4 {VIDEO_URL}")

# ----------- RESIZE VIDEO FOR INSTAGRAM -----------

print(f"🎞️ Resizing video to {RESOLUTION}")
run_bash_command(f"ffmpeg -i original.mp4 -vf scale={RESOLUTION}:force_original_aspect_ratio=decrease,pad={RESOLUTION}:(ow-iw)/2:(oh-ih)/2 -c:v libx264 -c:a aac -y {OUTPUT_FILE}")

# ----------- START STREAM LOOP -----------

while True:
    print("📡 Streaming to Instagram...")
    
    stream_command = f"ffmpeg -re -stream_loop -1 -i {OUTPUT_FILE} -vcodec libx264 -preset veryfast -pix_fmt yuv420p -r 30 -g 60 -b:v {BITRATE} -maxrate {BITRATE} -bufsize 5000k -acodec aac -ar 44100 -b:a 128k -f flv {INSTAGRAM_URL}"
    
    run_bash_command(stream_command)

    print("⚠️ FFmpeg crashed or stopped. Restarting in 5 seconds...")
    time.sleep(5)
