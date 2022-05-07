import json
import requests
from bs4 import BeautifulSoup

#tag filtering to check for js scripts
tag = "cooking"

response = requests.get(f"https://medium.com/tag/{tag}/latest")

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

h = open('raw_latest_posts.json', 'w', encoding="utf-8")

json.dump(graphql_query_data_json, h)
h.close()

related_tags = []
posts = []

for k, v in graphql_query_data_json.items():
    if k.startswith("Tag:") and k != f'Tag:{tag}':
        related_tags.append(k.split(':')[1])
    elif k.startswith("Post:"):
        posts.append(v["mediumUrl"])

f = open('latest_posts.json', 'w', encoding="utf-8")

json.dump({"related_tags": related_tags, "posts": posts}, f)
f.close()