#!/bin/env python

from flask import Flask, jsonify
from hn import HN

app = Flask(__name__)

@app.route('/get/top', methods = ['GET'])
def get_top():
    hn = HN()
    return jsonify({'stories': hn.get_stories()})

@app.route('/get/<story_type>', methods = ['GET'])
def get_stories(story_type):
    hn = HN()
    return jsonify({'stories': hn.get_stories(story_type=story_type)})

if __name__ == '__main__':
    app.run(debug=True)