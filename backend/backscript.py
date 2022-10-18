from flask import Flask, request, jsonify
from flask_cors import CORS
  
# Initializing flask app
app = Flask(__name__)
CORS(app)
  
# Route for seeing a data
@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
    file = request.json
    print(file)
    print(request)
    print(jsonify(file))

    return "done"
  
# Running app
if __name__ == '__main__':
    app.run(debug=True)

