from flask import Flask, request, jsonify
from flask_cors import CORS
  
# Initializing flask app
app = Flask(__name__)
CORS(app)
  
# Route for seeing a data
@app.route('/api/upload', methods = ['GET'])
def upload_file():
    file = request.json
    print(jsonify(file))
    return "done"
  
# Running app
if __name__ == '__main__':
    app.run(debug=True)