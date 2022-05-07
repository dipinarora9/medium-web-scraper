import json
import requests
from bs4 import BeautifulSoup

#tag filtering to check for js scripts
post_url = "https://medium.flutterdevs.com/implement-dark-mode-in-flutter-using-provider-158925112bf9"

post_id = post_url.split('-')[-1]

response = requests.get(post_url)

soup = BeautifulSoup(response.text, features='html.parser')

a = open("post.html", 'w', encoding="utf-8")
a.write(response.text)
a.close()

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

h = open('raw_post.json', 'w', encoding="utf-8")

json.dump(graphql_query_data_json, h)
h.close()

post_data = graphql_query_data_json[f"Post:{post_id}"]

# # technically this could throw can exception but for unknown reasons medium is always returning articles
post_paragraphs_list = post_data["content({\"postMeteringOptions\":null})"][
    "bodyModel"]["paragraphs"]
post_tags_list = post_data["tags"]

post_paragraph_ids = [
    post_paragraph_map["__ref"] for post_paragraph_map in post_paragraphs_list
]
post_tags = [
    post_tag_map["__ref"].split(":")[1] for post_tag_map in post_tags_list
]

post_paragraphs = []

for post_paragraph_id in post_paragraph_ids:
    #switch case statement here for categorize post type
    post_paragraphs.append(graphql_query_data_json[post_paragraph_id])

f = open('post.json', 'w', encoding="utf-8")

json.dump({"paragraphs": post_paragraphs, "tags": post_tags}, f)
f.close()