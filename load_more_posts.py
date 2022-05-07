import json
import requests
from bs4 import BeautifulSoup

#tag filtering to check for js scripts
tag = "car"
page = 3

response = requests.get(f"https://medium.com/search?q={tag}?page={page}")

soup = BeautifulSoup(response.text, features='html.parser')

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
    print("graphql data not found")

graphql_query_data_json = json.loads(graphql_query_data)

del graphql_query_data_json["ROOT_QUERY"]

w = open('raw_posts.json', 'w', encoding="utf-8")

json.dump(graphql_query_data_json, w)
w.close()

search_data = graphql_query_data_json["Search:{}"]

# technically this could throw can exception but for unknown reasons medium is always returning articles
posts_map_list = search_data[
    f"posts-{tag}?page={page}(limit:10)(algoliaOptions:analyticsTags:web,clickAnalytics:true,filters:writtenByHighQualityUser:true)(searchInCollection:false)"][
        "items"]

post_ids = [post_map["__ref"] for post_map in posts_map_list]

posts = []

for post_id in post_ids:
    posts.append(graphql_query_data_json[post_id]["mediumUrl"])

f = open('posts.json', 'w', encoding="utf-8")

json.dump(posts, f)
f.close()