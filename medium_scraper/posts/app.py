from flask import Blueprint, request
from medium_scraper.posts.helpers.websocket_socket_helper import posts_crawler
from medium_scraper.posts.helpers.posts_helper import *

posts = Blueprint('posts', __name__)


@posts.route('/trending_tags')
def trending_tags():
    return get_trending_tags()


@posts.route('/search/<string:tag>')
def search(tag):
    return get_post_urls_and_related_tags_for_tag(tag)


@posts.route('/load_more_posts/<string:tag>/<int:page>')
def load_more_posts(tag, page):
    return load_more_posts_for_tag(tag, page)


@posts.route('/crawl', websocket=True)
def crawl():
    return posts_crawler(request)
