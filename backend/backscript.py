from flask import Flask, request, jsonify, make_response
# from flask_cors import CORS
  
# Initializing flask app
app = Flask(__name__)
# CORS(app)
  
DONE = {"result":True}

# Route for seeing a data
@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
    file = request.files['myFile']
    print(file.mimetype)
    with open('test.jpeg', 'wb') as f:
        file.save(f)
    # print(jsonify(file))

    return jsonify(DONE)

@app.route('/')
def home():
    return make_response("Hello World!", 200)
  
# Running app
if __name__ == '__main__':
    app.run(debug=True)

