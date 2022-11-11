import subprocess
ffmpeg -y -vcodec png -r 10 -start_number 0 -i ./20221104194552_%05d.png -frames:v 115 -c:v libx264 -vf fps=10 -pix_fmt yuv420p -crf 17 -preset veryfast ./output.mp4
subprocess.run("ffmpeg", "-y", "-vcodec", "png", "-r", "10", "-start_number", "0", "-i", location, "-frames:v", max_frames, "-c:v", "libx264", "-vf", "fps=10", "-pix_fmt", "yuv420p", "-crf", "17", "-preset", "veryfast", "./output.mp4")

subprocess.run(["ffmpeg", "-y", "-vcodec", "png", "-r", "10", "-start_number", "0", "-i", "./20221111041155_%05d.png", "-frames:v", "100", "-c:v", "libx264", "-vf", "fps=10", "-pix_fmt", "yuv420p", "-crf", "17", "-preset", "veryfast", "./output.mp4"])
subprocess.run(["ffmpeg", "-y", "-vcodec", "png", "-r", str(10), "-start_number", "0", "-i", "/root/lyrical/backend/DeforumStableDiffusionLocal/output/1_3", "-frames:v", str(10), "-c:v", "libx264", "-vf", "fps="+str(10), "-pix_fmt", "yuv420p", "-crf", "17", "-preset", "veryfast", "./test.mp4"])