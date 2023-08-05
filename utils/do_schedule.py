import time
import schedule
from utils.helpers import timetable, request_forecast, happy_birthday


def do_schedule():
    try:
        schedule.every().day.at("06:40").do(timetable)
        schedule.every().day.at("06:45").do(request_forecast)
        schedule.every().day.at("06:50").do(happy_birthday)

        while True:
            schedule.run_pending()
            time.sleep(1)
    except Exception as e:
        print(e)