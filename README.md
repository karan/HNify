HNify
=====

![HNify](https://raw.github.com/karan/HackerNewsAPI/master/HN.jpg)

Unofficial REST API for [Hacker News](https://news.ycombinator.com/). Built using [HackerNewsAPI](https://github.com/karan/HackerNewsAPI).

Now uses memcached for increased performace!

Start
=====

    $ brew install memcached            # install memcached
    $ pip install -r requirements.txt   # install dependencies
    $ memcached -vv                     # start memcached server
    $ python app.py                     # start the api

Deploy to Heroku
=====

    $ pip install -r requirements.txt   # install dependencies
    $ heroku create
    $ heroku addons:add memcachedcloud
    $ heroku addons:add newrelic
    $ (git add, git commit)
    $ git push heroku master

If you get an error on the memcached line, see the following [help article](https://devcenter.heroku.com/articles/config-vars).

Usage
==========

**Base URL:** [http://hnify.herokuapp.com](http://hnify.herokuapp.com)

**Output:** JSON

### Get stories from top page

#### `GET /get/top`

**Parameters:**

| Name | Type | Description |
| ---- | ---- | ----------- |
| `limit` | integer | Return only at most these many stories, at least 30 |

### Get stories from newest page

#### `GET /get/newest`

**Parameters:**

| Name | Type | Description |
| ---- | ---- | ----------- |
| `limit` | integer | Return only at most these many stories, at least 30 |

### Get stories from best page

#### `GET /get/best`

**Parameters:**

| Name | Type | Description |
| ---- | ---- | ----------- |
| `limit` | integer | Return only at most these many stories, at least 30 |

### Currently trending topics on HN

#### `GET /get/trends`

### Get comments from story id

#### `GET /get/comments/<story_id>/`

--------

### Example

    karan:$ curl -i http://hnify.herokuapp.com/get/newest
    HTTP/1.1 200 OK
    Content-Type: application/json
    Date: Tue, 29 Oct 2013 06:23:39 GMT
    Server: gunicorn/18.0
    Content-Length: 16562
    Connection: keep-alive
    
    {
      "stories": [
        {
          "comments_link": "http://news.ycombinator.com/item?id=6632337", 
          "domain": "independent.co.uk", 
          "is_self": false, 
          "link": "http://www.independent.co.uk/news/science/lifi-breakthrough-internet-connections-using-light-bulbs-are-250-times-faster-than-broadband-8909320.html", 
          "num_comments": 0, 
          "points": 1, 
          "published_time": "1 minute ago", 
          "rank": 1, 
          "story_id": 6632337, 
          "submitter": "yapcguy", 
          "submitter_profile": "http://news.ycombinator.com/user?id=yapcguy", 
          "title": "Li-Fi: Internet connections using light bulbs are 250 x faster than broadband"
        }, 
        {
          "comments_link": "http://news.ycombinator.com/item?id=6632335", 
          "domain": "github.com", 
          "is_self": false, 
          "link": "https://github.com/postmodern/chruby", 
          "num_comments": 0, 
          "points": 2, 
          "published_time": "1 minute ago", 
          "rank": 2, 
          "story_id": 6632335, 
          "submitter": "michaelrkn", 
          "submitter_profile": "http://news.ycombinator.com/user?id=michaelrkn", 
          "title": "Chruby: a lightweight, elegant RVM alternative"
        }, 
        <-- snip -->
        ]
    }


Donations
=============

If HNify has helped you in any way, and you'd like to help the developer, please consider donating.

**- BTC: [19dLDL4ax7xRmMiGDAbkizh6WA6Yei2zP5](http://i.imgur.com/bAQgKLN.png)**

**- Flattr: [https://flattr.com/profile/thekarangoel](https://flattr.com/profile/thekarangoel)**


Contribute
========

If you want to add any new features, or improve existing ones, feel free to send a pull request!

[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/karan/hnify/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

