import json
from models.constants import MEDIUM_ASSETS_BASE_URL
from models.creator import Creator


class Post:

    def __init__(self, graphql_query_data_json, post_id):
        self.graphql_query_data_json = graphql_query_data_json
        post_object = graphql_query_data_json[f'Post:{post_id}']
        self.id = post_object["id"]
        self.title = post_object["title"]
        self.created_at = post_object["latestPublishedAt"]
        self.description = ""
        self.medium_url = post_object["mediumUrl"]

        self.paragraphs = self.get_paragraphs(post_object)
        creator_id = post_object["creator"]["__ref"]
        self.creator = Creator(graphql_query_data_json[creator_id])
        self.tags = Post.get_tags(post_object)
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
            Post.paragraph_json_html_tag_converter(
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

    def to_json(self) -> str:
        data = {}
        data["id"] = self.id
        data["title"] = self.title
        data["created_at"] = self.created_at
        data["description"] = self.description
        data["medium_url"] = self.medium_url
        data["paragraphs"] = self.paragraphs
        data["creator"] = self.creator.to_dict()
        data["tags"] = self.tags
        data["claps_count"] = self.claps_count
        data["responses_count"] = self.responses_count
        return json.dumps(data)

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
            return f"<img src='{image_url}'>"

        elif tag == "mixtape_embeded":
            return None

        return f"<{tag}>{text}</{tag}>"
