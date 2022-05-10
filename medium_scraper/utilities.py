import aiohttp
import asyncio
from medium_scraper.controller.post_controller import PostController
from medium_scraper.models.creator import Creator
from medium_scraper.models.post import Post
from medium_scraper import db


async def crawl_posts(post_urls, ws):

    def send_post_to_client(post):
        ws.send(post.to_json())

    def save_post_to_db(post):
        creator = Creator.query.filter_by(
            profile_url=post.creator.profile_url).first()
        if creator is not None:
            creator = post.creator
            creator.posts.append(post)
            del post.creator
            post.creator_id = creator.profile_url
            db.session.add(post)
        else:
            creator = post.creator
            del post.creator
            creator.posts.append(post)
            db.session.add(creator)
            db.session.add(post)
        db.session.commit()

    def send_post_to_client_and_save_to_db(future):
        post = future.result()
        send_post_to_client(post)
        save_post_to_db(post)

    async with aiohttp.ClientSession() as session:
        tasks = []
        for post_url in post_urls:
            post_id = post_url.split('-')[-1]
            post = Post.query.filter_by(id=post_id).first()
            if post is None:
                task = asyncio.ensure_future(
                    PostController.fetch_post(post_url, session))
                task.add_done_callback(send_post_to_client_and_save_to_db)
                tasks.append(task)
            else:
                send_post_to_client(post)

        await asyncio.gather(*tasks, return_exceptions=True)