import asyncio
import json
import sys
import simple_websocket
from medium_scraper.posts.helpers.asyncio_helper import AsyncioHelper


def posts_crawler(request):
    websocket = simple_websocket.Server(request.environ)
    post_urls = websocket.receive()
    post_urls = json.loads(post_urls)
    try:
        asyncio_helper = AsyncioHelper(websocket)

        if sys.platform == 'win32':
            #only for windows
            asyncio.set_event_loop_policy(
                asyncio.WindowsSelectorEventLoopPolicy())

        asyncio.new_event_loop().run_until_complete(
            asyncio_helper.crawl_posts(post_urls))
        websocket.close()
    except (KeyboardInterrupt, EOFError):
        websocket.close()
        print('closing connection')
    except simple_websocket.ConnectionClosed:
        print('connection closed')
    except Exception as e:
        websocket.close()
        print('closing connection due to ' + str(e))
    return ""