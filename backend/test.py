# import subprocess
# ffmpeg -y -vcodec png -r 10 -start_number 0 -i ./20221104194552_%05d.png -frames:v 115 -c:v libx264 -vf fps=10 -pix_fmt yuv420p -crf 17 -preset veryfast ./output.mp4
# subprocess.run("ffmpeg", "-y", "-vcodec", "png", "-r", "10", "-start_number", "0", "-i", location, "-frames:v", max_frames, "-c:v", "libx264", "-vf", "fps=10", "-pix_fmt", "yuv420p", "-crf", "17", "-preset", "veryfast", "./output.mp4")

# subprocess.run(["ffmpeg", "-y", "-vcodec", "png", "-r", "10", "-start_number", "0", "-i", "./20221111041155_%05d.png", "-frames:v", "100", "-c:v", "libx264", "-vf", "fps=10", "-pix_fmt", "yuv420p", "-crf", "17", "-preset", "veryfast", "./output.mp4"])
# subprocess.run(["ffmpeg", "-y", "-vcodec", "png", "-r", str(10), "-start_number", "0", "-i", "/root/lyrical/backend/DeforumStableDiffusionLocal/output/1_3/20221111050537_%05d.png", "-frames:v", str(10), "-c:v", "libx264", "-vf", "fps="+str(10), "-pix_fmt", "yuv420p", "-crf", "17", "-preset", "veryfast", "./test.mp4"])
from moviepy.editor import *
video_clip = VideoFileClip("./input/test.mp4")
audio_clip = AudioFileClip("./input/test.mp3")
min_duration = min(video_clip.duration, audio_clip.duration)
new_video_clip = video_clip.subclip(0, min_duration)
new_audio_clip = audio_clip.subclip(0, min_duration)
composite_audio = CompositeAudioClip([new_audio_clip])
new_video_clip.audio = composite_audio
new_video_clip.write_videofile("./output/output.mp4")