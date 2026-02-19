import re
from datetime import datetime, timedelta
import logging
import json
import random
from python_gelbooru import AsyncGelbooru
import asyncio
import config as cfg

post_id = re.search(r'\d{1,}', r'https://gelbooru.com/index.php?page=post&s=view&id=13500674&tags=umamusume+rating%3Ageneral')
print(post_id[0] if post_id else "couldn't find post id" )

async def booru():
    async with AsyncGelbooru(api_key=cfg.GELBOORU_API_KEY,
                             user_id=cfg.GELBOORU_USER_ID) as gel:
        yuyu = await gel.search_posts(['saigyouji yuyuko', 'rating:explicit'], limit=10, random=True)

        tasks = [i.async_download(f"./arts/{i.id}") for i in yuyu]
        print("done")
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(booru())

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO )






