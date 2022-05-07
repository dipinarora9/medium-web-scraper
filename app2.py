import asyncio
from flask import Flask, render_template, request
from controller.post_controller import PostController
import aiohttp
import simple_websocket

app = Flask(__name__, template_folder='views')
app.config['SECRET_KEY'] = 'secret!'


@app.route('/echo', websocket=True)
def echo():
    ws = simple_websocket.Server(request.environ)
    try:
        while True:
            data = ws.receive()
            print(data)
            ws.send(data)
    except simple_websocket.ConnectionClosed:
        pass
    return ''


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search/<string:tag>', websocket=True)
def search(tag):
    ws = simple_websocket.Server(request.environ)
    post_urls_and_related_tags = PostController.fetch_latest_post_urls_and_related_tags(
        tag)
    try:
        asyncio.new_event_loop().run_until_complete(
            crawl_posts(post_urls_and_related_tags['post_urls'], ws))
        ws.close()
    except (KeyboardInterrupt, EOFError, simple_websocket.ConnectionClosed):
        ws.close()
        print('connection closed')
    return post_urls_and_related_tags


# @app.route('/crawl', websocket=True)
# def handle_my_custom_event(post_urls):
#     print('received post_urls: ' + str(post_urls))
#     ws = simple_websocket.Server(request.environ)
#     try:
#         while True:
#             data = ws.receive()
#             print(data)
#             ws.send(data)
#             asyncio.get_event_loop().run_until_complete(
#                 crawl_posts(post_urls, ws))
#     except simple_websocket.ConnectionClosed:
#         pass
#     return ''


async def crawl_posts(post_urls, ws):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for post_url in post_urls:
            task = asyncio.ensure_future(
                PostController.fetch_post(post_url, session, ws))
            tasks.append(task)
        await asyncio.gather(*tasks, return_exceptions=True)


if __name__ == "__main__":
    app.run()