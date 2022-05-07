import asyncio
from flask_socketio import SocketIO, emit
from flask import Flask, render_template
from controller.post_controller import PostController
import aiohttp
from flask_cors import CORS, cross_origin

app = Flask(__name__, template_folder='views')
app.config['SECRET_KEY'] = 'secret!'
app.config['CORS_HEADERS'] = 'Content-Type'
socketio = SocketIO(app)


@app.route('/')
@cross_origin()
def index():
    return render_template('index.html')


@app.route('/search/<string:tag>')
@cross_origin()
def search(tag):
    post_urls_and_related_tags = PostController.fetch_latest_post_urls_and_related_tags(
        tag)

    return post_urls_and_related_tags


@socketio.on('crawl')
@cross_origin()
def handle_my_custom_event(post_urls):
    print('received post_urls: ' + str(post_urls))
    asyncio.get_event_loop().run_until_complete(crawl_posts(post_urls, emit))


@socketio.on('connect')
@cross_origin()
def connect(data):
    print('connected ' + data)


async def crawl_posts(post_urls, emit):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for post_url in post_urls:
            task = asyncio.ensure_future(
                PostController.fetch_post(post_url, session, emit))
            tasks.append(task)
        await asyncio.gather(*tasks, return_exceptions=True)


if __name__ == "__main__":
    socketio.run(app)