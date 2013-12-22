![HNify](https://raw.github.com/karan/HackerNewsAPI/master/HN.jpg)

Unofficial REST API for [Hacker News](https://news.ycombinator.com/). Built using [HackerNewsAPI](https://github.com/karan/HackerNewsAPI).


[Donate](https://www.gittip.com/Karan%20Goel/)
=============

If you love and use *HNify*, please consider [donating via gittip](https://www.gittip.com/Karan%20Goel/), or [flattring me](https://flattr.com/profile/thekarangoel). Any support is appreciated!

Start
=====

    $ python app.py

Usage
==========

**Base URL:** [http://hnify.herokuapp.com](http://hnify.herokuapp.com)

**Output:** JSON

### `/get/top`

Returns stories from the front page of HN.

### `/get/newest`

Returns stories from the newest page of HN.

### `/get/best`

Returns stories from the best page of HN.

### `/get/trends`

Returns currently trending topics from HN.


![](https://blockchain.info/Resources/buttons/donate_64.png)
=============

If Hacker News API has helped you in any way, and you'd like to help the developer, please consider donating.

**- BTC: [19dLDL4ax7xRmMiGDAbkizh6WA6Yei2zP5](http://i.imgur.com/bAQgKLN.png)**

**- Flattr: [https://flattr.com/profile/thekarangoel](https://flattr.com/profile/thekarangoel)**

**- Dogecoin: DGJxQkPqfxGkPYazHdPpAfatyagpDdG4qJ**

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

Contribute
========

If you want to add any new features, or improve existing ones, feel free to send a pull request!

[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/karan/hnify/trend.png)](https://bitdeli.com/free "Bitdeli Badge")

