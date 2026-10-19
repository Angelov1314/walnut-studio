#!/bin/zsh
set -euo pipefail
cd "$(dirname "$0")/.."
ffmpeg -y -framerate 24 -i renders/frames/%04d.png -vf 'hqdn3d=1.2:1.2:3:3,fade=t=in:st=0:d=0.45,fade=t=out:st=14.45:d=0.55' -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -movflags +faststart Walnut_Studio_Film.mp4
ffprobe -v error -select_streams v:0 -show_entries stream=width,height,r_frame_rate,nb_frames,duration -of json Walnut_Studio_Film.mp4 > renders/video_validation.json
