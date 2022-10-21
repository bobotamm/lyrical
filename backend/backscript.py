from flask import Flask, request, jsonify
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
  
# Running app
if __name__ == '__main__':
    app.run(debug=True)

