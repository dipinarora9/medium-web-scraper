import asyncio
import json
import simple_websocket
from flask import Blueprint, jsonify, request
from medium_scraper.controller.post_controller import PostController
from medium_scraper.utilities import crawl_posts

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return jsonify("its working done worry!")


@main.route('/search/<string:tag>')
def search(tag):
    post_urls_and_related_tags = PostController.fetch_latest_post_urls_and_related_tags(
        tag)
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
        #only for windows
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
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
