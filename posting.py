from datetime import datetime, timedelta
from time import sleep
import random
import string
from pyrogram import Client, filters
from pyrogram.handlers import MessageHandler
import config as cfg
# don't forget change config_safe.py of you are copying this code
import logging
import json

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO )

app = Client("anime_69", api_id=cfg.API_ID, api_hash=cfg.API_HASH)

#SETTINGS BLOCK
TargetChannel = cfg.TARGET_CHANNEL
LinkDump = cfg.LINKS_DUMP_CHAT
TwitterBot = cfg.TWITTER_LINKS_BOT
PixivBot = cfg.PIXIV_LINKS_BOT

# TIME BLOCK
CurrentTime = (datetime.strftime(datetime.now(), '%H:%M:%S  %d.%m.%y' ))
PlannedTime = datetime.now() + timedelta(hours=5)
PlndIntTime = datetime.timestamp(PlannedTime)
OutputTime = datetime.strftime(PlannedTime, '%A %H:%M %d.%m.%y' )

# print(f'Програма запущена та готова до роботи | {CurrentTime}')

try_to_post = 'Спроба створити пост у відложці'
def print_success(source = None, target = None, action = None):
    if source == SourceChannel:
        print('Отримано пост з відложки |', (datetime.strftime(datetime.now(), '%H:%M:%S  %d.%m.%y' )))
    elif source != None and target == None:
        print(f'> Отримано посилання на {source} |', (datetime.strftime(datetime.now(), '%H:%M:%S  %d.%m.%y' )))
    elif target == SourceChannel:
        print(f'Пост обработано та надіслано в відложку успішно |', (datetime.strftime(datetime.now(), '%H:%M:%S  %d.%m.%y' )))
    elif target != None and target != SourceChannel:
        print (f'Надіслано в {target} успішно |', (datetime.strftime(datetime.now(), '%H:%M:%S  %d.%m.%y' )))
    elif target == TargetChannel:
        print(f'Пост було заплановано на {OutputTime} успішно!!!! ^w^')
    else:
        print(f'{action} Виконано успішно |', (datetime.strftime(datetime.now(), '%H:%M:%S  %d.%m.%y' )), (target), (source))

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

def generate_time (filename="latest.json", mode="r"):
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

# URL DETECTION AND HANDLING BLOCK
async def twi_detection(client, message):
    print_success(source='Twitter', action='oбнаруженіе поста')
    # print(f'message id: {message.id} time: {datetime.now()}')
    await app.forward_messages(
        chat_id=TwitterBot,
        from_chat_id = LinkDump,
        message_ids = message.id, )
    print_success(target='Twitter_Bot')
    await message.reply(text="`❕ — ПОСТ ОТРИМАНО, ЗАЧЕКАЙ`")
    generate_time()
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
    print(f'message id: {message.id} {datetime.now()}')
    await app.forward_messages(
        chat_id=PixivBot,
        from_chat_id=LinkDump,
        message_ids=message.id, )
    print_success(target='Pixiv_Bot')
    await message.reply(text="`❕ — ПОСТ ОТРИМАНО, ЗАЧЕКАЙ`")
    generate_time()
    sleep(3)
    await app.copy_message(
        chat_id=TargetChannel,
        from_chat_id=PixivBot,
        message_id=message.id + 3,
        caption=generate_caption(message.text),
        schedule_date=PlannedTime, )
    await app.edit_message_text(chat_id=LinkDump, message_id=message.id + 2, text=f"`✅ — УСПІШНО ЗАПЛАНОВАНО НА {OutputTime}`")
    print_success(target=TargetChannel)

def gel_detection(client, message):
    print_success(source='Gelbooru')

app.add_handler(MessageHandler(twi_detection, filters.chat(LinkDump) & filters.regex("x.com")))
app.add_handler(MessageHandler(pix_detection, filters.chat(LinkDump) & filters.regex("pixiv.net")))
app.add_handler(MessageHandler(gel_detection, filters.chat(LinkDump) & filters.regex("gelbooru.com")))

# async def test(client, message):
#   print('test')

# app.add_handler(MessageHandler(test, filters.chat(LinkDump)))


#print(f'Програма завершена | {CurrentTime}')


app.run()