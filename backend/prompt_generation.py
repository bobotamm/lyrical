import subprocess
import os
import json
import random
from pathlib import Path

STRONG_STRENGTH = str(0.4)
WEAK_STRENGTH = str(0.65)
BACKEND_ROOT_PATH = Path.cwd()
AUDIO_INPUT_DIRECTORY = BACKEND_ROOT_PATH / "input" / "audios"
LYRICS_PATH = BACKEND_ROOT_PATH / "input" / "lyrics"
MXLRC_PATH = BACKEND_ROOT_PATH / "MxLRC"
PROMPT_PATH = BACKEND_ROOT_PATH / "input" / "prompts"

# Transform time string to seconds in float
def process_time(time_str):
    minutes, seconds = time_str.split(':')
    return float(minutes) * 60 + float(seconds)

# Parse .lrc file. Output a dictionary with author, title, length, and lyrics (list)
def parse_lrc_file(file_name):
    if file_name[-4:] != '.lrc':
        return None
    res = {}
    with open(file_name) as f:
        lines = f.readlines()
        author = lines[1].strip().lstrip('[').rstrip(']')[3:]
        song_title = lines[2].strip().lstrip('[').rstrip(']')[3:]
        total_time_str = lines[4].strip().lstrip('[').rstrip(']')[7:]
        total_seconds = process_time(total_time_str)
        res['author'] = author
        res['title'] = song_title
        res['length'] = total_seconds
        res['lyrics'] = []
        for i in range(5, len(lines)):
            lyrics_time_str, lyrics = lines[i].lstrip('[').split(']')
            lyrics_time = process_time(lyrics_time_str)
            lyrics = lyrics.strip()
            res['lyrics'].append((lyrics_time, lyrics))
    return res

# Generate prompt from lyrics
# TODO: Extend prompt engineering
def prompt_engineering(lyrics):
    return 'A detailed painting of ' + lyrics

# Generate intial prompt for frame 0
def prompt_intialization(author, title):
    return 'A detailed painting of ' + title + ',' + ' a portrait of ' + author

# Generate animation_prompts for Stable Diffusion
def transform_lyrics_to_prompt(author, title, lyrics_list, fps):
    animation_prompts = {}
    animation_prompts[0] = prompt_intialization(author, title)
    for lyrics_time, lyrics in lyrics_list:
        lyrics_frame = int(lyrics_time * fps)
        prompt = prompt_engineering(lyrics)
        animation_prompts[lyrics_frame] = prompt
    return animation_prompts

# Generate strength_schedule for Stable Diffusion
def strength_schedule_generation(animation_prompts):
    frames = [frame for frame in sorted(animation_prompts.keys())]
    str_joiner = [(0, ':(' + STRONG_STRENGTH +')')]
    for i in range(1, len(frames)):
        prev_frame = str_joiner[-1][0]
        curr_frame = frames[i]
        mid_frame = (prev_frame + curr_frame) // 2
        if prev_frame < mid_frame and mid_frame < curr_frame:
            str_joiner.append((mid_frame, ':(' + WEAK_STRENGTH + ')'))
        str_joiner.append((curr_frame, ':(' + STRONG_STRENGTH +')'))
    res = ','.join([str(f[0]) + f[1] for f in str_joiner])
    return res

# Generate prompt given author, title, and fps
def generate_prompt(user_id, audio_id, lrc_file_name, author, title, length = -1, fps = 10):
    parsed_file = parse_lrc_file(lrc_file_name)
    animation_prompts = transform_lyrics_to_prompt(author, title, parsed_file['lyrics'], fps)
    strength_schedule = strength_schedule_generation(animation_prompts)

    f = open(str(PROMPT_PATH / "template.txt"))
    template = json.load(f)
    f.close()

    seed = random.randint(0, 2**32)
    template['seed'] = seed
    template['animation_prompts'] = animation_prompts
    template['strength_schedule'] = strength_schedule
    # Set batch_name as userId_audioId so that it can be found easily in the future
    template['batch_name'] = str(user_id) + "_" + str(audio_id)
    if length == -1:
        template['max_frames'] = int(parsed_file['length']) * fps
    else:
        template['max_frames'] = length * fps
    return template
    