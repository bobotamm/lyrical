from flask import Flask, request, jsonify, make_response, redirect, url_for, send_from_directory, current_app
import os
from celery import Celery
import time
import json
import subprocess
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
import pymysql
from song_recognization import recognize
import prompt_generation
import logging
import datetime
from pathlib import Path
from moviepy.editor import *

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config["CELERY_BACKEND_URL"],
        broker=app.config["CELERY_BROKER_URL"],
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

# Initializing flask app
app = Flask(__name__)
cors = CORS(app)
app.config.update(
    CELERY_BROKER_URL="amqp://lyrical:lyrical@localhost/lyrical",
    CELERY_BACKEND_URL="db+sqlite:///test.db",
)
celery = make_celery(app)
load_dotenv()
logging.basicConfig(filename='backend.log', level=logging.DEBUG)

SUCCESS = {"result":True}
FAILURE = {"result":False}
ALLOWED_AUDIO_EXTENSIONS = {'mp3', 'wav'}
BACKEND_ROOT_PATH = Path.cwd()
AUDIO_INPUT_DIRECTORY = BACKEND_ROOT_PATH / "input" / "audios"
LYRICS_PATH = BACKEND_ROOT_PATH / "input" / "lyrics"
MXLRC_PATH = BACKEND_ROOT_PATH / "MxLRC"
PROMPT_PATH = BACKEND_ROOT_PATH / "input" / "prompts"
IMAGES_PATH = BACKEND_ROOT_PATH / "DeforumStableDiffusionLocal" / "output"
VIDEOS_PATH = BACKEND_ROOT_PATH / "output"
FPS = 10
VIDEO_LENGTH_LIMIT = 30

# Check if audio file extention is supported
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_AUDIO_EXTENSIONS

def connect_to_db():
    db = pymysql.connect(
        host="localhost",
        database="lyrical",
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD")
    )
    return db
db = connect_to_db()
# Register
@app.route('/register', methods = ['POST'])
def register():
    requestData = json.loads(request.data)
    username = requestData['username']
    password = requestData['password']
    try:
        db = connect_to_db()
        cursor = db.cursor()
        cursor.execute(f"INSERT INTO user(user_name, user_password) VALUES (%s, %s); ", (str(username), str(password)))
        db.commit()
        db.close()
        response = SUCCESS.copy()
        response['id'] = cursor.lastrowid
        return jsonify(response)
    except:
        return jsonify(FAILURE)

# Login
@app.route('/login', methods = ['POST'])
def login():
    requestData = json.loads(request.data)
    username = requestData['username']
    password = requestData['password']
    cursor = connect_to_db().cursor()
    cursor.execute(f"SELECT user_id FROM user WHERE user_name = %s AND user_password = %s;", (str(username), str(password)))
    db_res = cursor.fetchall()
    if len(db_res) > 0:
        response = SUCCESS.copy()
        response['id'] = db_res[0][0]
        return jsonify(response)
    else:
        return jsonify(FAILURE)

# Display
@app.route('/display', methods = ['POST'])
def display():
    requestData = json.loads(request.data)
    user_id = requestData['user_id']
    print("User id", user_id)
    cursor = connect_to_db().cursor()
    cursor.execute(f"SELECT audio_id, audio_file_name, status FROM audio_input WHERE user_id = %s;", (str(user_id)))
    db_res = cursor.fetchall()
    response = SUCCESS.copy()
    print(db_res)
    response['audio_data'] = db_res
    return jsonify(response)


# Route for seeing a data
@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
    print("Upload Once")
    file = request.files['myFile']
    user_id = request.form['user_id']
    # Prevent processing not supported files
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify(FAILURE)

    # Save the audio file
    (AUDIO_INPUT_DIRECTORY / str(user_id)).mkdir(parents=True, exist_ok=True)
    (LYRICS_PATH / str(user_id)).mkdir(parents=True, exist_ok=True)
    (PROMPT_PATH / str(user_id)).mkdir(parents=True, exist_ok=True)
    (VIDEOS_PATH).mkdir(parents=True, exist_ok=True)
    target_directory = AUDIO_INPUT_DIRECTORY / str(user_id)
    ending = 1
    file_name_raw, file_name_extention = file.filename.split(".")
    while (target_directory / (file_name_raw+'_'+str(ending)+"."+file_name_extention)).exists():
        ending += 1
    file_name = file_name_raw+'_'+str(ending)+"."+file_name_extention
    with open(str(target_directory / file_name), 'wb') as f:
        file.save(f)
    
    # Insert into Database
    audio_id = None
    try:
        db = connect_to_db()
        cursor = db.cursor()
        cursor.execute(f"INSERT INTO audio_input(audio_file_name, status, user_id) VALUES (%s, %s, %s); ", (file_name, 0, int(user_id)))
        db.commit()
        audio_id = cursor.lastrowid
        db.close()
    except:
        return jsonify(FAILURE)

    # Initiate a task
    video_generation.delay(user_id, file_name, audio_id)

    response = jsonify(SUCCESS)
    return response


# file extension is hard coded 
@app.route('/download', methods = ['GET', 'POST'])
def download_file():
    requestData = json.loads(request.data)
    user_id = requestData['user_id']
    audio_id = requestData['audio_id']
    print("Downloading ", str(user_id) + "_" + str(audio_id) + ".mp4 from ", str(VIDEOS_PATH))
    return send_from_directory(str(VIDEOS_PATH), str(user_id) + "_" + str(audio_id) + ".mp4", as_attachment=True)
    # response = make_response("download!", 200)
    # return response  

# Testing only, to be deleted
@app.route('/download_test/<filename>', methods = ['GET', 'POST'])
def download_test_file(filename):
    downloads = os.path.join(current_app.root_path, "DeforumStableDiffusionLocal", "output", "2022-11", "test")
    return send_from_directory(downloads, filename, as_attachment=True)

@app.route('/')
def home():
    logging.info("Testing Logger INFO")
    return make_response("Hello World!", 200)

@app.route('/generate', methods = ['GET', 'POST'])
@cross_origin(origin="*", headers = ['Content-Type', 'Authorization'])
def generate_video():
    ### data = request.get_json()
    response = jsonify(message = "the request worked!")
    return response

@celery.task(default_retry_delay=100000, max_retries=0)
def video_generation(user_id, file_name, audio_id):
    # Check video status, avoid repeating tasks
    cursor = connect_to_db().cursor()
    cursor.execute(f"SELECT status FROM audio_input WHERE user_id = %s AND audio_id = %s;", (str(user_id), str(audio_id)))
    db_res = cursor.fetchall()
    if int(db_res[0][0]) == 2:
        return

    # Find the author and title
    recognize_result = recognize(str(AUDIO_INPUT_DIRECTORY / str(user_id) / file_name), os.getenv("AUDD_API_TOKEN")).json()
    if recognize_result['status'] != "success":
        logging.error("Recognize Failed", recognize_result)
        return
    author = recognize_result['result']['artist']
    title = recognize_result['result']['title']

    # Download the lyrics
    lyrics_file_dir = LYRICS_PATH / str(user_id)
    subprocess.run(["python", "mxlrc.py", "--song", author+ "," +title, "--out", lyrics_file_dir], capture_output=True, text=True, cwd=str(MXLRC_PATH))
    lyrics_file_name = author + " - " + title + ".lrc"
    if not (lyrics_file_dir / lyrics_file_name).exists():
        logging.error("Download Lyrics Failed")
        return
    
    # Update DB
    lyric_id = None
    try:
        db = connect_to_db()
        cursor = db.cursor()
        cursor.execute(f"INSERT INTO lyric(lyric_file_name, audio_id) VALUES (%s, %s); ", (lyrics_file_name, str(audio_id)))
        lyric_id = cursor.lastrowid
        cursor.execute(f"UPDATE audio_input SET status = 1 WHERE audio_id = %s", [str(audio_id)])
        db.commit()
        db.close()
    except:
        logging.error("Update DB Failed")
        return

    # Generate Prompts
    prompt_file_dir = PROMPT_PATH / str(user_id)
    prompt_dict = prompt_generation.generate_prompt(user_id, audio_id, str(lyrics_file_dir / lyrics_file_name), author, title, VIDEO_LENGTH_LIMIT, FPS)
    max_frames = prompt_dict['max_frames']
    with open(str(prompt_file_dir/ (str(lyric_id) + ".txt")), 'w') as f:
        json.dump(prompt_dict, f)
    
    
    user_id_audio_id = str(user_id) + "_" + str(audio_id)
    images_dir = IMAGES_PATH / user_id_audio_id

    # Generate Images
    with open("celery_log.log", "a") as f:
        f.write("\nGenerating for" + str(lyric_id) + str(max_frames))
    logging.info("Generating for" + str(lyric_id))
    exit_code = subprocess.run(["python", "run.py", "--enable_animation_mode", "--settings", str(prompt_file_dir/ (str(lyric_id) + ".txt"))], cwd=str(BACKEND_ROOT_PATH / "DeforumStableDiffusionLocal"))
    logging.info("Generation Ends!")
    
    # Combine Videos
    timestring = find_timestring(images_dir)
    images_file_names = timestring + "_%05d.png"
    silent_video_file_name = str(VIDEOS_PATH / (user_id_audio_id + "_silent.mp4"))
    subprocess.run(["ffmpeg", "-nostdin", "-y", "-vcodec", "png", "-r", str(FPS), "-start_number", "0", "-i", str(images_dir / images_file_names), "-frames:v", str(max_frames), "-c:v", "libx264", "-vf", "fps="+str(FPS), "-pix_fmt", "yuv420p", "-crf", "17", "-preset", "veryfast", silent_video_file_name])

    # Sync Videos with Music
    sync_video_file_name = str(VIDEOS_PATH / (user_id_audio_id + ".mp4"))
    video_clip = VideoFileClip(silent_video_file_name)
    audio_clip = AudioFileClip(str(AUDIO_INPUT_DIRECTORY / str(user_id) / file_name))
    min_duration = min(video_clip.duration, audio_clip.duration)
    new_video_clip = video_clip.subclip(0, min_duration)
    new_audio_clip = audio_clip.subclip(0, min_duration)
    composite_audio = CompositeAudioClip([new_audio_clip])
    new_video_clip.audio = composite_audio
    new_video_clip.write_videofile(sync_video_file_name)
    

    # Update Database
    try:
        db = connect_to_db()
        cursor = db.cursor()
        cursor.execute(f"UPDATE audio_input SET status = 2 WHERE audio_id = %s", [str(audio_id)])
        db.commit()
        db.close()
    except:
        logging.error("Update DB After Generation Failed")
        return

def find_timestring(images_dir):
    timestring = None
    for f in images_dir.iterdir():
        file_name = f.name
        if file_name.endswith(".png"):
            timestring = file_name.split(".")[0].split("_")[0]
            break
    return timestring


# Running app
if __name__ == '__main__':
    app.run(debug=True)

