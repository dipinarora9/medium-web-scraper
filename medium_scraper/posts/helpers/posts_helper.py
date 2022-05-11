from flask import jsonify
from medium_scraper.services.post_service import PostService
from medium_scraper.services.database_service import DatabaseService
from medium_scraper import autocomplete


def get_trending_tags():
    trending_tags = DatabaseService.get_trending_tags()
    return jsonify(trending_tags)


def get_post_urls_and_related_tags_for_tag(tag):
    post_urls_and_related_tags = PostService.fetch_latest_post_urls_and_related_tags(
        tag)
    if post_urls_and_related_tags['post_urls']:
        DatabaseService.update_tag_counter(tag)
        autocomplete.insert_word(tag)

    return jsonify(post_urls_and_related_tags)


def load_more_posts_for_tag(tag, page):
    post_urls = PostService.fetch_more_post_urls(tag, page)
    return jsonify(post_urls)