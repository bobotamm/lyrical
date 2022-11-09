from flask import Flask, request, jsonify, make_response, redirect, url_for, send_from_directory, current_app
import os
from celery import Celery
import time
import requests
import json
import subprocess
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
import MySQLdb

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


SUCCESS = {"result":True}
FAILURE = {"result":False}
ALLOWED_AUDIO_EXTENSIONS = {'mp3', 'wav'}

# Check if audio file extention is supported
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_AUDIO_EXTENSIONS

def connect_to_db():
    db = MySQLdb.connect(
        host="localhost",
        database="lyrical",
        user="root",
        password=os.getenv("DB_PASSWORD")
    )
    return db

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
    print(request.data)
    print(request)
    requestData = json.loads(request.data)
    user_id = requestData['user_id']
    print("User id", user_id)
    db = MySQLdb.connect(
        host="localhost",
        database="lyrical",
        user="root",
        password=os.getenv("DB_PASSWORD")
    )
    cursor = connect_to_db().cursor()
    cursor.execute(f"SELECT audio_id, audio_file_name, status FROM audio_input WHERE user_id = %s;", (str(user_id)))
    db_res = cursor.fetchall()
    response = SUCCESS.copy()
    response['audio_data'] = db_res
    return jsonify(response)


# Route for seeing a data
@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
    file = request.files['myFile']
    user_id = request.form['user_id']
    # Prevent processing not supported files
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify(FAILURE)

    # Save the audio file
    target_directory = os.path.join(current_app.root_path, "audios", str(user_id))
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)
    ending = 1
    file_name_raw, file_name_extention = file.filename.split(".")
    while os.path.exists(os.path.join(current_app.root_path, "audios", str(user_id), file_name_raw+'_'+str(ending)+"."+file_name_extention)):
        ending += 1
    file_name = file_name_raw+'_'+str(ending)+"."+file_name_extention
    with open(os.path.join(current_app.root_path, "audios", str(user_id), file_name), 'wb') as f:
        file.save(f)
    
    # Insert into Database
    try:
        db = connect_to_db()
        cursor = db.cursor()
        cursor.execute(f"INSERT INTO audio_input(audio_file_name, status, user_id) VALUES (%s, %s, %s); ", (file_name, 0, int(user_id)))
        db.commit()
        db.close()
    except:
        return jsonify(FAILURE)

    # Initiate a task

    response = jsonify(SUCCESS)
    return response


# file extension is hard coded 
@app.route('/download', methods = ['GET', 'POST'])
def download_file():
    downloads = os.path.join(current_app.root_path)
    return send_from_directory(downloads, "test.mp3", as_attachment=True)
    # response = make_response("download!", 200)
    # return response  

# Testing only, to be deleted
@app.route('/download_test/<filename>', methods = ['GET', 'POST'])
def download_test_file(filename):
    downloads = os.path.join(current_app.root_path, "DeforumStableDiffusionLocal", "output", "2022-11", "test")
    return send_from_directory(downloads, filename, as_attachment=True)

@app.route('/')
def home():
    return make_response("Hello World!", 200)

@app.route('/test_celery')
def test_celery():
    test_celery_c.delay()
    return redirect(url_for("home"))


@app.route('/generate', methods = ['GET', 'POST'])
@cross_origin(origin="*", headers = ['Content-Type', 'Authorization'])
def generate_video():
    ### data = request.get_json()
    response = jsonify(message = "the request worked!")
    return response

@celery.task()
def test_celery_c():
    print("Testing Start")
    with open('log.log', 'w') as f:
        f.write('Working!' + str(time.time()))
    exit_code = subprocess.run(["python", "run.py", "--enable_animation_mode", "--settings", "runSettings_Template.txt"], capture_output=True, text=True, cwd="./DeforumStableDiffusionLocal/")
    with open('log.log', 'w') as f:
        f.write('Complete')
        f.write(str(exit_code.returncode))
        f.write(str(exit_code.stdout))
  
# Running app
if __name__ == '__main__':
    app.run(debug=True)

