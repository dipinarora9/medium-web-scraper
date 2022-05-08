import asyncio
import json
from flask import Flask, render_template, request
from controller.post_controller import PostController
import aiohttp
import simple_websocket
from flask_ngrok import run_with_ngrok
from flask_cors import CORS, cross_origin

app = Flask(__name__, template_folder='views')
app.config['SECRET_KEY'] = 'secret!'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search/<string:tag>')
def search(tag):
    post_urls_and_related_tags = PostController.fetch_latest_post_urls_and_related_tags(
        tag)
    return post_urls_and_related_tags


@app.route('/crawl', websocket=True)
def crawl():
    ws = simple_websocket.Server(request.environ)
    post_urls = ws.receive()
    post_urls = json.loads(post_urls)
    try:
        #only for windows
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        asyncio.new_event_loop().run_until_complete(crawl_posts(post_urls, ws))
        ws.close()
    except (KeyboardInterrupt, EOFError, simple_websocket.ConnectionClosed):
        ws.close()
        print('connection closed')
    except Exception as e:
        ws.close()
        print('connection closed ' + e)
    return ""


async def crawl_posts(post_urls, ws):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for post_url in post_urls:
            task = asyncio.ensure_future(
                PostController.fetch_post(post_url, session, ws))
            tasks.append(task)
        await asyncio.gather(*tasks, return_exceptions=True)


if __name__ == "__main__":
    run_with_ngrok(app)
    CORS(app)
    app.run()