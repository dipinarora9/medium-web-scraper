import aiohttp
import asyncio
from medium_scraper.services.post_service import PostService
from medium_scraper.services.database_service import DatabaseService


class AsyncioHelper:

    def __init__(self, websocket) -> None:
        self.websocket = websocket

    def send_post_to_client(self, post):
        self.websocket.send(post.to_json())

    def save_post_to_db(self, post):
        DatabaseService.add_post_and_creator_to_db(post)

    def send_post_to_client_and_save_to_db(self, future):
        post = future.result()
        self.send_post_to_client(post)
        self.save_post_to_db(post)

    async def crawl_posts(self, post_urls):
        async with aiohttp.ClientSession() as session:
            tasks = []
            for post_url in post_urls:
                post = DatabaseService.get_post_from_post_url(post_url)
                if post is None:
                    task = asyncio.ensure_future(
                        PostService.fetch_post(post_url, session))
                    task.add_done_callback(
                        self.send_post_to_client_and_save_to_db)
                    tasks.append(task)
                else:
                    self.send_post_to_client(post)

            await asyncio.gather(*tasks, return_exceptions=True)