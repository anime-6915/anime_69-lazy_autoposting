from pyrogram.handlers import MessageHandler
from pyrogram import Client, filters
from python_gelbooru import AsyncGelbooru

from datetime import datetime, timedelta
from time import sleep

import aiohttp
import random
import string
import logging
import glob
import json
import re

import config as cfg # don't forget to rename config_safe.py

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO )

app = Client("anime_69", api_id=cfg.TELEGRAM_API_ID, api_hash=cfg.TELEGRAM_API_HASH)

#SETTINGS BLOCK
SourceChannel = cfg.SOURCE_CHANNEL
TargetChannel = cfg.TARGET_CHANNEL
LinkDump = cfg.LINKS_DUMP_CHAT
TwitterBot = cfg.TWITTER_LINKS_BOT
PixivBot = cfg.PIXIV_LINKS_BOT

# TIME BLOCK
CurrentTime = (datetime.strftime(datetime.send_now(), '%H:%M:%S  %d.%m.%y' ))
PlannedTime = datetime.send_now()
OutputTime = datetime.strftime(PlannedTime, '%A %H:%M %d.%m.%y' )

# print(f'Програма запущена та готова до роботи | {CurrentTime}')

try_to_post = 'Спроба створити пост у відложці'
def print_success(source = None, target = None, action = None):
    if source == SourceChannel:
        print('Отримано пост з відложки |', (datetime.strftime(datetime.send_now(), '%H:%M:%S  %d.%m.%y' )))
    elif source != None and target == None:
        print(f'> Отримано посилання на {source} |', (datetime.strftime(datetime.send_now(), '%H:%M:%S  %d.%m.%y' )))
    elif target == SourceChannel:
        print(f'Пост обработано та надіслано в відложку успішно |', (datetime.strftime(datetime.send_now(), '%H:%M:%S  %d.%m.%y' )))
    elif target != None and target != SourceChannel:
        print (f'Надіслано в {target} успішно |', (datetime.strftime(datetime.send_now(), '%H:%M:%S  %d.%m.%y' )))
    elif target == TargetChannel:
        print(f'Пост було заплановано на {OutputTime} успішно!!!! ^w^')
    else:
        print(f'{action} Виконано успішно |', (datetime.strftime(datetime.send_now(), '%H:%M:%S  %d.%m.%y' )), (target), (source))

def generate_caption(url):
    def generate_random_string(length):
        # Combine lowercase letters, uppercase letters, and digits
        characters = string.ascii_lowercase
        # Use random.choices() to pick 'length' number of characters with repetition
        random_string = ''.join(random.choices(characters, k=length))
        return random_string
    length = random.randint(10, 17)
    caption_final = str(f"[{generate_random_string(length)}]({url})")
    return caption_final

def generate_time (filename="latest.json", mode="r", send_now=None):
    if send_now == False:
        with open(filename, mode) as json_file: # відкриття з параметрами т.з. "батьківської" функції
            time_check = json.load(json_file)
            hrs_lst = [2, 3, 3, 5, 5, 4]
            new_hrs = random.choice(hrs_lst)
            new_min = random.randint(7, 30)
            global PlannedTime
            # генерація нового часу, з випадковим проміжком на основі часу який був взятий з .json файлу
            PlannedTime = datetime.strptime(time_check["time"], '%Y-%m-%d %H:%M:%S.%f') + timedelta(hours=new_hrs, minutes=new_min)
            # конвертація формату часу для рандомного багу
            unmatched_fix = datetime.strptime(time_check["time"], '%Y-%m-%d %H:%M:%S.%f')
            # конвертація часу для використання в "зміні дня"
            time_shenanigans = datetime.strptime(
                f"{datetime.strftime(unmatched_fix, format='%Y-%m-%d')} 08:{datetime.strftime(PlannedTime, format='%M:%S.%f')}",
                '%Y-%m-%d %H:%M:%S.%f'  )
            # призначення часу та перевірки для зміни дня
            if int(time_check["hour"]) > 20:
                latest_time = time_shenanigans + timedelta(days=1)
                PlannedTime = latest_time
                # print("------21------") was used for debug, to check new day and how daychange was triggered
            else :
                if int(datetime.strftime(PlannedTime, format ='%H')) < 8: # перевірка для зміни дня
                    latest_time = time_shenanigans + timedelta(days=1)
                    PlannedTime = latest_time
                    # print("------8------")  was used for debug, to check new day and how daychange was triggered
                else:
                    latest_time = PlannedTime
            # генерація та запис .json файлу
            latest_post_hour = datetime.strftime(PlannedTime, format ='%H')
            latest_post_minute = datetime.strftime(PlannedTime, format = '%M')
            latest_post_day = datetime.strftime(PlannedTime, format = '%d')
            latest_post_month = datetime.strftime(PlannedTime, format = '%m')
            global latest_post_write
            latest_post_write = {
                "time": str(latest_time),
                "hour": str(latest_post_hour),
                "minute": (latest_post_minute),
                "day": latest_post_day,
                "month": latest_post_month  }
            # запис файлу
        with open("latest.json", mode="w") as write_time:
            json.dump(latest_post_write, write_time, indent=4)
    else:
        PlannedTime = None

# URL DETECTION AND HANDLING BLOCK
async def twi_detection(client, message):
    print_success(source='Twitter', action='oбнаруженіе поста')
    # print(f'message id: {message.id} time: {datetime.send_now()}')
    await app.forward_messages(
        chat_id=TwitterBot,
        from_chat_id = LinkDump,
        message_ids = message.id, )
    print_success(target='Twitter_Bot')
    await message.reply(text="`❕ — ПОСТ ОТРИМАНО, ЗАЧЕКАЙ`")
    generate_time(send_now=False)
    sleep(2)
    await app.copy_message(
        chat_id=TargetChannel,
        from_chat_id=TwitterBot,
        message_id=message.id + 3,
        caption=generate_caption(message.text),
        schedule_date=PlannedTime,
    )
    await app.edit_message_text(chat_id=LinkDump, message_id=message.id + 2, text=f"`✅ — УСПІШНО ЗАПЛАНОВАНО НА {OutputTime}`")
    print_success(target=TargetChannel)

async def pix_detection(client, message):
    print_success(source='Pixiv', action='oбнаруженіе поста')
    await app.forward_messages(
        chat_id=PixivBot,
        from_chat_id=LinkDump,
        message_ids=message.id, )
    print_success(target='Pixiv_Bot')
    await message.reply(text="`❕ — ПОСТ ОТРИМАНО, ЗАЧЕКАЙ`")
    generate_time(send_now=False)
    sleep(4)
    await app.copy_message(
        chat_id=TargetChannel,
        from_chat_id=PixivBot,
        message_id=message.id + 3,
        caption=generate_caption(message.text),
        schedule_date=PlannedTime, )
    await app.edit_message_text(chat_id=LinkDump, message_id=message.id + 2, text=f"`✅ — УСПІШНО ЗАПЛАНОВАНО НА {OutputTime}`")
    print_success(target=TargetChannel)

async def gel_detection(client, message):
    print_success(source='Gelbooru')
    headers = { # needed to go around gelbooru's CDN protection
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://gelbooru.com/"
    }
    await message.reply(text="`❕ — ПОСТ ОТРИМАНО, ЗАЧЕКАЙ`")
    link_id = re.search(r'\d{1,}', string = message.text)
    # downloading
    async with aiohttp.ClientSession(headers=headers) as custom_session:
        async with AsyncGelbooru(api_key=cfg.GELBOORU_API_KEY,
                                 user_id=cfg.GELBOORU_USER_ID) as gel:
            post = await gel.get_post(post_id=link_id[0])

            if post:
                print(f"Пост #{post.id} знайдено! Завантаження...")
                await post.async_download(f"./arts/{post.id}", session=custom_session)

                print("Завантажено!")
                filepath = glob.glob(f"./arts/{post.id}.*") # setting up filepath to just-downloaded image
                print(filepath)
            else:
                print(f"Помилка! Пост з ID:{post.id} не знайден! Як ти цього взагалі добився? В Gelbooru ID йдуть з 1 до нескінченності!")
    generate_time(send_now=False)
    await app.send_photo(
        chat_id=TargetChannel,
        photo = filepath[0],
        caption=generate_caption(f'https://gelbooru.com/index.php?page=post&s=view&id={post.id}'),
        schedule_date=PlannedTime, )
    await app.edit_message_text(chat_id=LinkDump, message_id=message.id + 1,
                                text=f"`✅ — УСПІШНО ЗАПЛАНОВАНО НА {OutputTime}`")
    print_success(target=TargetChannel)



app.add_handler(MessageHandler(twi_detection, filters.chat(LinkDump) & filters.regex("x.com")))
app.add_handler(MessageHandler(pix_detection, filters.chat(LinkDump) & filters.regex("pixiv.net")))
app.add_handler(MessageHandler(gel_detection, filters.chat(LinkDump) & filters.regex("gelbooru.com")))

# async def test(client, message):
#   print('test')

# app.add_handler(MessageHandler(test, filters.chat(LinkDump)))


#print(f'Програма завершена | {CurrentTime}')


app.run()
