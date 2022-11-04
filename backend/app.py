from flask import Flask, request, jsonify, make_response, redirect, url_for, send_from_directory, current_app
import os
from celery import Celery
import time
import requests
import json
import subprocess
from flask_cors import CORS, cross_origin

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
DONE = {"result":True}

# Route for seeing a data
@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
    file = request.files['myFile']
    print(file.mimetype)
    with open('test.jpeg', 'wb') as f:
        file.save(f)
    response = jsonify(DONE)
    response.headers.add("Access-Control-Allow-Origin","*")
    return response


# file extension is hard coded 
@app.route('/download', methods = ['GET', 'POST'])
def download_file():
    downloads = os.path.join(current_app.root_path)
    return send_from_directory(downloads, "test.jpeg", as_attachment=True)
    # response = make_response("download!", 200)
    # return response  


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

