import subprocess
import os

STRONG_STRENGTH = str(0.4)
WEAK_STRENGTH = str(0.65)
OUTPUT_PATH = os.getcwd() + "\input\lyrics"
MXLRC_PATH = os.getcwd() + "\MxLRC"

def process_time(time_str):
    minutes, seconds = time_str.split(':')
    return float(minutes) * 60 + float(seconds)

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

def prompt_engineering(lyrics):
    return 'A detailed painting of ' + lyrics

def prompt_intialization(author, title):
    return 'A detailed painting of ' + title + ',' + ' a portrait of ' + author

def transform_lyrics_to_prompt(author, title, lyrics_list, fps):
    animation_prompts = {}
    animation_prompts[0] = prompt_intialization(author, title)
    for lyrics_time, lyrics in lyrics_list:
        lyrics_frame = int(lyrics_time * fps)
        prompt = prompt_engineering(lyrics)
        animation_prompts[lyrics_frame] = prompt
    return animation_prompts

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

def download_lrc(author, title):
    target = author + ", " + title
    output_file_name = author + " - " + title + ".lrc"
    subprocess.run(["python", "mxlrc.py", "--song", target, "--out", OUTPUT_PATH], capture_output=True, text=True, cwd=MXLRC_PATH)
    if os.path.exists(os.path.join(OUTPUT_PATH, output_file_name)):
        return output_file_name
    return None



# parsed_file = parse_lrc_file('Katy Perry - Roar.lrc')
# animation_prompts = transform_lyrics_to_prompt(parsed_file['author'], parsed_file['title'], parsed_file['lyrics'], 10)
# strength_schedule = strength_schedule_generation(animation_prompts)
# print(animation_prompts)
# print(strength_schedule)
download_lrc("Drake", "God's Plan")