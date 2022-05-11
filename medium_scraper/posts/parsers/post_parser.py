import json
from medium_scraper.helpers.constants import MEDIUM_ASSETS_BASE_URL
from medium_scraper.posts.parsers.creator_parser import CreatorParser
from medium_scraper.posts.models.post import Post


class PostParser:

    def __init__(self, graphql_query_data_json, post_id):
        self.graphql_query_data_json = graphql_query_data_json
        post_object = graphql_query_data_json[f'Post:{post_id}']
        self.id = post_object["id"]
        self.title = post_object["title"]
        self.created_at = post_object["latestPublishedAt"]

        #TODO: description
        self.description = ""
        self.medium_url = post_object["mediumUrl"]

        self.paragraphs = self.get_paragraphs(post_object)
        creator_id = post_object["creator"]["__ref"]
        self.creator_parser = CreatorParser(
            graphql_query_data_json[creator_id])
        self.tags = PostParser.get_tags(post_object)
        self.claps_count = post_object["clapCount"]
        self.responses_count = post_object["postResponses"]["count"]

    def get_paragraphs(self, post_object):
        post_paragraphs_list = post_object[
            "content({\"postMeteringOptions\":null})"]["bodyModel"][
                "paragraphs"]

        post_paragraph_ids = [
            post_paragraph_map["__ref"]
            for post_paragraph_map in post_paragraphs_list
        ]
        paragraphs = [
            PostParser.paragraph_json_html_tag_converter(
                self.graphql_query_data_json[paragraph_id])
            for paragraph_id in post_paragraph_ids
        ]

        return list(filter(lambda paragraph: paragraph is not None,
                           paragraphs))

    def get_tags(post_object):
        return [
            post_tag_map["__ref"].split(":")[1]
            for post_tag_map in post_object["tags"]
        ]

    def to_post(self, time_taken) -> Post:
        creator = self.creator_parser.to_creator()
        post = Post(creator=creator)
        post.id = self.id
        post.title = self.title
        post.created_at = self.created_at
        post.description = self.description
        post.medium_url = self.medium_url
        post.paragraphs = json.dumps(self.paragraphs)
        post.tags = json.dumps(self.tags)
        post.claps_count = self.claps_count
        post.responses_count = self.responses_count
        post.time_taken_to_crawl = time_taken
        return post

    @staticmethod
    def paragraph_json_html_tag_converter(data):
        tag = data['type'].lower()
        source_url = None
        text = data['text']

        if tag == 'iframe':
            source_url = data['iframe']['mediaResource']['__ref'].split(
                "MediaResource:")[1]
            source_url = MEDIUM_ASSETS_BASE_URL + source_url
            return f"<{tag} src='{source_url}'>{text}</{tag}>"

        elif tag == 'img':
            image_url = data["metadata"]["__ref"].split("ImageMetadata:")[1]
            image_url = MEDIUM_ASSETS_BASE_URL + image_url
            return f"<img src='{image_url}' height=300>"

        elif tag == "mixtape_embeded":
            return None

        return f"<{tag}>{text}</{tag}>"
