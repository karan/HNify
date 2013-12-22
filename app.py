#!/usr/bin/env python

import time
import re
from collections import Counter

from hn import HN
from flask import Flask, jsonify, make_response, render_template, redirect

app = Flask(__name__)
temp_cache = {
    'top': {
        'response_json' : None,
        'time' : time.time()
        },
    'best': {
        'response_json' : None,
        'time' : time.time()
        },
    'newest': {
        'response_json' : None,
        'time' : time.time()
        },
    'trends': {
        'response_json': None,
        'time': time.time()
    }
}

# cache time to live in seconds
timeout = 600

stopwords = ["a","able","about","across","after","all","almost","also","am",
             "among","an","and","any","are","as","at","be","because","been",
             "but","by","can","cannot","could","dear","did","do","does",
             "either","else","ever","every","for","from","get","got","had",
             "has","have","he","her","hers","him","his","how","however","i",
             "if","in","into","is","it","its","just","least","let","like",
             "likely","may","me","might","most","must","my","neither","no",
             "nor","not","of","off","often","on","only","or","other","our",
             "own","rather","said","say","says","she","should","since","so",
             "some","than","that","the","their","them","then","there","these",
             "they","this","tis","to","too","twas","us","wants","was","we",
             "were","what","when","where","which","while","who","whom","why",
             "will","with","would","yet","you","your", 'show hn', 'ask hn',
             'hn', 'show', 'ask']

@app.route('/')
def index():
    '''
    This page is displayed when index page is requested.
    '''
    return render_template('main.html')

@app.route('/get/top', methods=['GET'])
def get_top():
    '''
    Returns stories from the front page of HN.
    '''
    if temp_cache['top']['response_json'] is not None \
       and temp_cache['top']['time'] + timeout < time.time():
        return jsonify(temp_cache['top']['response_json'])
    else:
        hn = HN()
        temp_cache['top']['response_json'] = {'stories': hn.get_stories()}
        temp_cache['top']['time'] = time.time()
        return jsonify(temp_cache['top']['response_json'])

@app.route('/get/<story_type>', methods=['GET'])
def get_stories(story_type):
    '''
    Returns stories from the requested page of HN.
    story_type is one of:
    \tnewest
    \tbest
    '''
    if temp_cache[story_type]['response_json'] is not None \
       and temp_cache[story_type]['time'] + timeout < time.time():
        return temp_cache[story_type]['response_json']
    else:
        hn = HN()
        temp_cache[story_type]['response_json'] = {'stories': hn.get_stories(story_type=story_type)}
        temp_cache[story_type]['time'] = time.time()
        return jsonify(temp_cache[story_type]['response_json'])

@app.route('/get/trends', methods=['GET'])
def trends():
    '''
    Returns currently trending topics.
    '''
    if temp_cache['trends']['response_json'] is not None \
       and temp_cache['trends']['time'] + timeout < time.time():
        return temp_cache['trends']['response_json']
    else:
        temp_cache['trends']['response_json'] = {'trends': get_trends()}
        temp_cache['trends']['time'] = time.time()
        return jsonify(temp_cache['trends']['response_json'])

@app.errorhandler(404)
def not_found(error):
    '''
    Returns a jsonified 404 error message instead of a HTTP 404 error.
    '''
    return make_response(jsonify({ 'steve_martin': 'A day without sunshine is like, you know, night.' }), 404)

@app.errorhandler(503)
def not_found(error):
    '''
    Returns a jsonified 503 error message instead of a HTTP 404 error.
    '''
    return make_response(jsonify({ 'einstein': 'If the facts don\'t fit the theory, change the facts.' }), 503)

def get_trends():
    '''
    Returns a list of trending topics on HN.
    '''
    hn = HN()
    
    titles = [story.title for story in hn.get_stories(page_limit=4)]

    one_grams = [] # list of 1-grams
    two_grams = [] # list of 2-grams
    
    # Single word regex
    one_word_pat = re.compile('[A-Z][A-Za-z.]+')
    # Two consecutive word @ http://regex101.com/r/xE2vT0
    two_word_pat = re.compile('(?=((?<![A-Za-z.])[A-Z][a-z.]*[\s-][A-Z][a-z.]+))')
    
    for title in titles:
        # get list of capitalized words
        one_words = re.findall(one_word_pat, title)
        # remove stop words
        one_words = [word for word in one_words if word.lower() not in stopwords]
        one_grams.extend(one_words)

        two_grams.extend(re.findall(two_word_pat, title))
    
    grams = Counter(one_grams).most_common() + Counter(two_grams).most_common()
    return [{'phrase': phrase[0], 'count': phrase[1]} for phrase in grams if phrase[1] > 1]
    
    
if __name__ == '__main__':
    app.run(debug=True)
