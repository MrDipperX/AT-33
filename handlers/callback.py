from loader import bot
from db.db import PgConn
from utils.constants import items_btns_lat


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    try:
        if call.data in items_btns_lat:
            db = PgConn()
            subject_panel = db.get_user_temp(call.message.chat.id)
            db.set_task_status(call.message.chat.id, subject_panel, call.data, True)
    except Exception as e:
        print(e)