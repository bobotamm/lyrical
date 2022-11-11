import subprocess
ffmpeg -y -vcodec png -r 10 -start_number 0 -i ./20221104194552_%05d.png -frames:v 115 -c:v libx264 -vf fps=10 -pix_fmt yuv420p -crf 17 -preset veryfast ./output.mp4