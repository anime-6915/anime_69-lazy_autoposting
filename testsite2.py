import random
import string
import asyncio
from datetime import datetime, timedelta
from time import sleep
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
import config as cfg
import logging
import asyncio
from python_gelbooru import AsyncGelbooru
import re
import aiohttp

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO )

#SETTINGS BLOCK
TargetChannel = cfg.TARGET_CHANNEL
SourceChannel = cfg.SOURCE_CHANNEL
LinkDump = cfg.LINKS_DUMP_CHAT
TwitterBot = cfg.TWITTER_LINKS_BOT
PixivBot = cfg.PIXIV_LINKS_BOT

# TIME BLOCK
CurrentTime = (datetime.strftime(datetime.now(), '%H:%M:%S  %d.%m.%y' ))
PlannedTime = datetime.now() + timedelta(hours=5)
PlndIntTime = datetime.timestamp(PlannedTime)
OutputTime = datetime.strftime(PlannedTime, '%A %H:%M %d.%m.%y' )

app = Client("anime_69", api_id=cfg.TELEGRAM_API_ID, api_hash=cfg.TELEGRAM_API_HASH)



async def gel_detection(client, message):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://gelbooru.com/"
    }
    ididid = re.search(r'\d{1,}', string = message.text)
    print("message detected")
    async with aiohttp.ClientSession(headers=headers) as custom_session:
        async with AsyncGelbooru(api_key=cfg.GELBOORU_API_KEY,
                                 user_id=cfg.GELBOORU_USER_ID) as gel:
            posts = await gel.get_post(post_id=ididid[0])

            if posts:
                post = posts  # Get the first (and likely only) post from the tuple
                print(f"Found post {post.id}! Downloading...")

                # 2. Download the post
                # The library automatically adds the correct file extension (e.g., .png or .jpg)
                # Make sure the target directory (e.g., './arts/') exists!
                await post.async_download(f"./arts/{post.id}", session=custom_session)

                print("Download complete!")
            else:
                print(f"Could not find a post with ID {post_id}.")
print(datetime.now())

app.add_handler(MessageHandler(gel_detection, filters.chat(LinkDump) & filters.regex("gelbooru.com")))
app.run()

