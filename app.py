from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from todo.todo import todo
import json

app = Flask(__name__)
app.register_blueprint(todo)
CORS(app)

@app.route('/')
@cross_origin()
def index():
    """
    Get the todo lists
    """
    return json.dumps({"status": "ok"}), 200

if __name__ == '__main__':
    app.run(debug=True)
