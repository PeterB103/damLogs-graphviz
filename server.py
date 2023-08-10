import sqlite3
import json
from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import parseFile
import sys

app = Flask(__name__)
CORS(app)  # Allows cross-origin requests

@app.route('/dotCode', methods=['GET'])
def get_dot_code():
    return parseFile.dotCode

if __name__ == '__main__':
    app.run(port=5000)
