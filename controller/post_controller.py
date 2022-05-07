import json
from bs4 import BeautifulSoup
import requests

from models.post import Post


class PostController:

    @staticmethod
    def fetch_post(post_url) -> Post:

        #tag filtering to check for js scripts
        post_id = post_url.split('-')[-1]

        response = requests.get(post_url)

        graphql_query_data_json = PostController._parse_graphql_response_in_json(
            response.text)

        post = Post(graphql_query_data_json, post_id)
        return post

    @staticmethod
    def fetch_latest_post_urls_and_related_tags(tag):
        #tag filtering to check for js scripts

        response = requests.get(f"https://medium.com/tag/{tag}/latest")

        graphql_query_data_json = PostController._parse_graphql_response_in_json(
            response.text)

        related_tags = []
        post_urls = []

        for k, v in graphql_query_data_json.items():
            if k.startswith("Tag:") and k != f'Tag:{tag}':
                related_tags.append(k.split(':')[1])
            elif k.startswith("Post:"):
                post_urls.append(v["mediumUrl"])

        return {"related_tags": related_tags, "post_urls": post_urls}

    @staticmethod
    def fetch_more_post_urls(tag, page):
        #tag filtering to check for js scripts
        response = requests.get(
            f"https://medium.com/search?q={tag}?page={page}")

        graphql_query_data_json = PostController._parse_graphql_response_in_json(
            response.text)

        search_data = graphql_query_data_json["Search:{}"]

        # technically this could throw can exception but for unknown reasons medium is always returning articles
        posts_map_list = search_data[
            f"posts-{tag}?page={page}(limit:10)(algoliaOptions:analyticsTags:web,clickAnalytics:true,filters:writtenByHighQualityUser:true)(searchInCollection:false)"][
                "items"]

        post_ids = [post_map["__ref"] for post_map in posts_map_list]

        post_urls = []

        for post_id in post_ids:
            post_urls.append(graphql_query_data_json[post_id]["mediumUrl"])

        return post_urls

    @staticmethod
    def _parse_graphql_response_in_json(response):
        soup = BeautifulSoup(response, features='html.parser')

        scripts = soup.find_all("script")

        graphql_query_data = None
        for script in scripts:
            if script.text.startswith("window.__APOLLO_STATE__"):
                graphql_query_data = script.text
                #this is to remove the extra elements from string
                graphql_query_data = graphql_query_data.split(
                    "window.__APOLLO_STATE__ =")[1]
                graphql_query_data = graphql_query_data.strip()
                break

        if not graphql_query_data:
            raise Exception("graphql data not found")
        graphql_query_data_json = json.loads(graphql_query_data)

        del graphql_query_data_json["ROOT_QUERY"]
        return graphql_query_data_json