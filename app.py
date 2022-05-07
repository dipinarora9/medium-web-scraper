from flask_socketio import SocketIO
from flask import Flask, render_template
from controller.post_controller import PostController

app = Flask(__name__, template_folder='views')
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search/<string:tag>')
def search(tag):
    post_urls_and_related_tags = PostController.fetch_latest_post_urls_and_related_tags(
        tag)

    return post_urls_and_related_tags


@socketio.on('crawl')
def handle_my_custom_event(json):
    print('received json: ' + str(json))


if __name__ == "__main__":
    socketio.run(app)