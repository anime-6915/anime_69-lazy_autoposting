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
import pandas

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



print(datetime.now())

app.run()

