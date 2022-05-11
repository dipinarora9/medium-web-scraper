import asyncio
import json
import sys
import simple_websocket
from flask import Blueprint, jsonify, request
from medium_scraper import db, autocomplete
from medium_scraper.controller.post_controller import PostController
from medium_scraper.utilities import crawl_posts
from medium_scraper.models.tag import Tag

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return jsonify("its working don't worry!")


@main.route('/trending_tags')
def trending_tags():
    t = Tag.query.order_by(Tag.counter.desc()).limit(5).all()
    tags = []
    for tag in t:
        tags.append(tag.tag)
    return jsonify(tags)


@main.route('/search/<string:tag>')
def search(tag):
    post_urls_and_related_tags = PostController.fetch_latest_post_urls_and_related_tags(
        tag)
    if post_urls_and_related_tags['post_urls']:
        t = Tag.query.filter_by(tag=tag).first()
        autocomplete.insert_word(tag)
        if t is None:
            db.session.add(Tag(tag=tag, counter=1))
        else:
            t.counter = Tag.counter + 1
        db.session.commit()
    return jsonify(post_urls_and_related_tags)


@main.route('/load_more_posts/<string:tag>/<int:page>')
def load_more_posts(tag, page):
    post_urls = PostController.fetch_more_post_urls(tag, page)
    return jsonify(post_urls)


@main.route('/crawl', websocket=True)
def crawl():
    ws = simple_websocket.Server(request.environ)
    post_urls = ws.receive()
    post_urls = json.loads(post_urls)
    try:
        if sys.platform == 'win32':
            #only for windows
            asyncio.set_event_loop_policy(
                asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.new_event_loop().run_until_complete(crawl_posts(post_urls, ws))
        ws.close()
    except (KeyboardInterrupt, EOFError):
        ws.close()
        print('closing connection')
    except simple_websocket.ConnectionClosed:
        print('connection closed')
    except Exception as e:
        ws.close()
        print('closing connection due to ' + str(e))
    return ""
