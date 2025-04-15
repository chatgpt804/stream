#!/bin/bash

set -e

# ----------- CONFIG -----------

# Google Drive direct download URL (replace YOUR_FILE_ID below)
VIDEO_URL="https://nsf-m4c-one-fr-01.sf-converter.com/prod-new/download/eyJtZWRpYUlkIjoiMmZEZkpHczVMN28iLCJ0aXRsZSI6IvCdkIfwnZCa8J2Qni3wnZCj8J2QqCAmIPCdkInwnZCa8J2Qni3wnZCm8J2QoiAtIERpZSBXaXRoIEEgU21pbGUgWyDwnZmI8J2Zpy4g8J2Zi_CdmaHwnZmW8J2Zo_CdmaDwnZmp8J2ZpPCdmaMgXSAja2RyYW1hICNrZHJhbWFlZGl0ICNtcnBsYW5rdG9uIiwiZm9ybWF0IjoibXA0IiwicXVhbGl0eSI6IjcyMCIsInRpbWVzdGFtcCI6MTc0NDcyODcxOX0.e101246462e2f1367ae33f8f6bc2933d"

# Output file
OUTPUT_FILE="stream.mp4"

# Instagram resolution (portrait)
RESOLUTION="720x1280"
BITRATE="2500k"

# ----------- INSTALL FFMPEG IF NEEDED -----------

if ! command -v ffmpeg &> /dev/null; then
  echo "🔧 FFmpeg not found. Installing..."
  apt-get update && apt-get install -y ffmpeg
else
  echo "✅ FFmpeg is already installed."
fi

# ----------- DOWNLOAD VIDEO -----------

echo "📥 Downloading video from Google Drive..."
wget -O original.mp4 "$VIDEO_URL"

# ----------- RESIZE VIDEO FOR INSTAGRAM -----------

echo "🎞️ Resizing video to $RESOLUTION"
ffmpeg -i original.mp4 -vf "scale=${RESOLUTION}:force_original_aspect_ratio=decrease,pad=${RESOLUTION}:(ow-iw)/2:(oh-ih)/2" -c:v libx264 -c:a aac -y "$OUTPUT_FILE"

# ----------- START STREAM LOOP -----------

while true
do
  echo "📡 Streaming to Instagram..."
  
  ffmpeg \
    -re \
    -stream_loop -1 \
    -i "$OUTPUT_FILE" \
    -vcodec libx264 \
    -preset veryfast \
    -pix_fmt yuv420p \
    -r 30 \
    -g 60 \
    -b:v "$BITRATE" \
    -maxrate "$BITRATE" \
    -bufsize 5000k \
    -acodec aac \
    -ar 44100 \
    -b:a 128k \
    -f flv \
    "$INSTAGRAM_URL"

  echo "⚠️ FFmpeg crashed or stopped. Restarting in 5 seconds..."
  sleep 5
done
