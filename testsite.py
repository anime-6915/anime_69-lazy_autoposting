import re
from datetime import datetime, timedelta
import logging
import json
import random
from python_gelbooru import AsyncGelbooru
import asyncio
import config as cfg
from posting import PlannedTime

post_id = re.search(r'\d{1,}', r'https://gelbooru.com/index.php?page=post&s=view&id=13500674&tags=umamusume+rating%3Ageneral')
print(post_id[0] if post_id else "couldn't find post id" )



if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(booru())

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO )






