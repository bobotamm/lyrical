import subprocess
exit_code = subprocess.run(["python", "run.py", "--enable_animation_mode", "--settings", "runSettings_Template.txt"], capture_output=True, cwd="./DeforumStableDiffusionLocal/")