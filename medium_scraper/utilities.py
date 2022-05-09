import aiohttp
import asyncio
from medium_scraper.controller.post_controller import PostController


async def crawl_posts(post_urls, ws):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for post_url in post_urls:
            task = asyncio.ensure_future(
                PostController.fetch_post(post_url, session, ws))
            tasks.append(task)
        await asyncio.gather(*tasks, return_exceptions=True)
