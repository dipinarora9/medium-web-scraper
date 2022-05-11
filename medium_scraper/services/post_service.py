import json
from bs4 import BeautifulSoup
import requests
import time
from medium_scraper.posts.models.post import Post
from medium_scraper.posts.parsers.post_parser import PostParser


class PostService:

    @staticmethod
    async def fetch_post(post_url, session) -> Post:

        async def scrape(session):
            async with session.get(post_url) as res:
                if res.status == 200:
                    text = await res.text()
                    return text

        t = time.time()
        #tag filtering to check for js scripts
        post_id = post_url.split('-')[-1]

        response_text = await scrape(session)

        graphql_query_data_json = PostService._parse_graphql_response_in_json(
            response_text)

        parsed_post = PostParser(graphql_query_data_json, post_id)
        time_taken = time.time() - t
        time_taken = round(time_taken, 3)
        return parsed_post.to_post(time_taken)

    @staticmethod
    def fetch_latest_post_urls_and_related_tags(tag):
        #tag filtering to check for js scripts

        response = requests.get(f"https://medium.com/tag/{tag}/latest")

        graphql_query_data_json = PostService._parse_graphql_response_in_json(
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
    def fetch_more_post_urls(tag, page_number):
        if page_number > 2:
            return []

        #tag filtering to check for js scripts
        pages = ['year', "all-time"]
        page = pages[page_number - 1]
        response = requests.get(f"https://medium.com/tag/{tag}/top/{page}")

        graphql_query_data_json = PostService._parse_graphql_response_in_json(
            response.text)
        post_urls = []

        for k, v in graphql_query_data_json.items():
            if k.startswith("Post:"):
                post_urls.append(v["mediumUrl"])
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
