from threading import Thread
from db.db import PgConn
from loader import bot
from utils.do_schedule import do_schedule
import handlers


def main_loop():
    db = PgConn()

    thread = Thread(target=do_schedule)
    thread.start()
    db.create_tables()
    bot.polling(none_stop=True)


if __name__ == '__main__':
    main_loop()
