from datetime import datetime, timedelta
import logging
import json


def write_current_time():
    PlannedTime = datetime.now()
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
        print(datetime.strftime(PlannedTime, '%A %H:%M %d.%m.%y'))


write_current_time()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO )






