import json
import requests
from bs4 import BeautifulSoup

from models.post import Post

#tag filtering to check for js scripts
post_url = "https://medium.flutterdevs.com/implement-dark-mode-in-flutter-using-provider-158925112bf9"

post_id = post_url.split('-')[-1]

response = requests.get(post_url)

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

post = Post(graphql_query_data_json, post_id)

f = open('post.json', 'w', encoding="utf-8")

f.write(post.to_json())
f.close()