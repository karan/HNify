#!/usr/bin/env python

import sys
sys.setrecursionlimit(1000)

import time
import re
from collections import Counter
import os

from hn import *
from flask import Flask, jsonify, make_response, render_template, redirect, request
import bmemcached as memcache


app = Flask(__name__)

# cache time to live in seconds
timeout = 600

mc = memcache.Client(os.environ.get('MEMCACHEDCLOUD_SERVERS').split(','),
                       os.environ.get('MEMCACHEDCLOUD_USERNAME'),
                       os.environ.get('MEMCACHEDCLOUD_PASSWORD'))

mc.set('top', None, time=timeout)
mc.set('best', None, time=timeout)
mc.set('newest', None, time=timeout)
mc.set('trends', None, time=timeout)

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


@app.route('/get/<story_type>/', methods=['GET'])
@app.route('/get/<story_type>', methods=['GET'])
def get_stories(story_type):
    '''
    Returns stories from the requested page of HN.
    story_type is one of:
    \ttop
    \tnewest
    \tbest
    '''
    story_type = str(story_type)
    limit = request.args.get('limit')
    limit = int(limit) if limit is not None else 30
    
    temp_cache = mc.get(story_type) # get the cache from memory
    
    if temp_cache is not None and len(temp_cache['stories']) >= limit:
        # we have enough in cache already
        return jsonify({'stories': temp_cache['stories'][:limit]})
    else:
        hn = HN()
        if story_type == 'top':
            stories = [story for story in hn.get_stories(limit=limit)]
        elif story_type in ['newest', 'best']:
            stories = [story for story in hn.get_stories(story_type=story_type, limit=limit)]
        else:
            abort(404)
        mc.set(story_type, {'stories': serialize(stories)}, time=timeout)
        return jsonify(mc.get(story_type))


@app.route('/get/comments/<story_id>', methods=['GET'])
@app.route('/get/comments/<story_id>/', methods=['GET'])
def comments(story_id):
    story_id = int(story_id)
    memcache_key = "%s_comments" % (story_id)

    temp_cache = mc.get(memcache_key) # get the cache from memory
    result = []

    if temp_cache is None:
        story = Story.fromid(story_id)
        comments = story.get_comments()
        for comment in comments:
            result.append({
                    "comment_id": comment.comment_id,
                    "level": comment.level,
                    "user": comment.user,
                    "time_ago": comment.time_ago,
                    "body": comment.body,
                    "body_html": comment.body_html
                })
        mc.set(memcache_key, {'comments': result}, time=timeout)
    return jsonify(mc.get(memcache_key))


@app.route('/get/trends', methods=['GET'])
def trends():
    '''
    Returns currently trending topics.
    '''
    temp_cache = mc.get('trends') # get the cache from memory
    if temp_cache is not None:
        return jsonify(temp_cache)
    else:
        hn = HN()
        mc.set('trends', {'trends': get_trends()}, time=timeout)
        return jsonify(mc.get('trends'))


def get_trends():
    '''
    Returns a list of trending topics on HN.
    '''
    hn = HN()
    
    titles = [story.title for story in hn.get_stories(limit=90)]

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
     
def serialize(stories):
    '''
    Takes a list of Story objects and returns a list of dict's.
    '''
    result = []
    
    for story in stories:
        result.append(
            {
                "comments_link": story.comments_link, 
                "domain": story.domain, 
                "is_self": story.is_self, 
                "link": story.link,
                "num_comments": story.num_comments, 
                "points": story.points, 
                "published_time": story.published_time, 
                "rank": story.rank, 
                "story_id": story.story_id, 
                "submitter": story.submitter, 
                "submitter_profile": story.submitter_profile, 
                "title": story.title
            }
        )
    return result


@app.errorhandler(404)
def not_found(error):
    '''
    Returns a jsonified 404 error message instead of a HTTP 404 error.
    '''
    return make_response(jsonify({ 'error': '404 not found' }), 404)


@app.errorhandler(503)
def not_found(error):
    '''
    Returns a jsonified 503 error message instead of a HTTP 404 error.
    '''
    return make_response(jsonify({ 'error': '503 something wrong' }), 503)


@app.errorhandler(500)
def not_found(error):
    '''
    Returns a jsonified 500 error message instead of a HTTP 404 error.
    '''
    return make_response(jsonify({ 'error': '500 something wrong' }), 500)


if __name__ == '__main__':
    app.run(debug=True)
