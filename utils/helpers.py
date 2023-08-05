from loader import bot
from db.db import PgConn

from keyboards.menu import menu_button
from utils.lang import lang
from datetime import datetime
import emoji
import requests

from config.config import CITY_ID, APP_ID


def set_date_birth(message):
    try:
        db = PgConn()
        db.add_user_date_birth(message.from_user.id, message.text)
        bot.send_message(message.from_user.id, f'{lang["Correct"]}')
    except Exception as e:
        bot.send_message(message.from_user.id, f'{lang["Rewrite_correct"]}')
        print(e)
        return


def set_user_name(message):
    try:
        db = PgConn()
        db.add_user_name(message.from_user.id, message.text)
        bot.send_message(message.from_user.id, f'{lang["Correct"]}')
    except Exception as e:
        bot.send_message(message.from_user.id, f'{lang["Rewrite_correct"]}')
        print(e)
        return


def subject_task_view(user_id, table_name, list_kir, list_lat):
    try:
        task_btns = []
        db = PgConn()
        db.set_user_temp(user_id, table_name)
        for kir, lat in zip(list_kir, list_lat):
            task_status = db.get_task_status(user_id, table_name, lat)
            if task_status:
                task_btns.append((f"{kir}{emoji.emojize(':check_mark_button:')}", lat))
            else:
                task_btns.append((f"{kir}", lat))
        return task_btns
    except Exception as e:
        print(e)


def del_old_subject(message):
    try:
        db = PgConn()
        user_temp = db.get_user_temp(message.from_user.id)
        if user_temp == "subjects_panel":
            pass
        else:
            bot.delete_message(message.chat.id, message.message_id - 2)
            bot.delete_message(message.chat.id, message.message_id - 1)
    except Exception as e:
        print(e)


def ad_text(message):
    try:
        db = PgConn()
        db.add_ad_text(message.text)
        bot.send_message(message.from_user.id, lang['Send_pic'])
    except Exception as e:
        print(e)


def send_ads():
    try:
        db = PgConn()
        users = db.get_all_info_user()
        text_and_url = db.send_add()

        for user in users:
            bot.send_photo(user[3], open(f"{text_and_url[1]}", 'rb'), text_and_url[0])
    except Exception as e:
        print(e)


def add_admin(message):
    try:
        admin_data = message.text.splitlines()
        db = PgConn()
        db.add_admin(admin_data[0], admin_data[1])
    except Exception as e:
        print(e)


def edit_admin(message):
    try:
        admin_data = message.text.splitlines()
        db = PgConn()
        db.edit_admin(admin_data[0], admin_data[1])
    except Exception as e:
        print(e)


def is_admin(message):
    try:
        db = PgConn()
        user_temp = db.get_user_temp(message.from_user.id)
        if user_temp == 'admin_panel':
            return True
        else:
            return False
    except Exception as e:
        print(e)


def happy_birthday():
    try:
        db = PgConn()
        users = db.get_users_id_db()
        for user in users:
            if user[1] is not None or user[2] is not None:
                if user[1].month == datetime.today().month and user[1].day == datetime.today().day:
                    hb = f"Поздравим, {user[2]} {emoji.emojize(':graduation_cap:')}. Имениннику исполнилось " \
                         f"{datetime.today().year-user[1].year}!"
                    bot.send_message(user[0], hb, parse_mode='html')
    except Exception as e:
        print(e)


def request_forecast():
    db = PgConn()
    users = db.get_users_id_db()
    weather_news = ''
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                           params={'id': CITY_ID, 'units': 'metric', 'lang': 'ru', 'APPID': APP_ID})
        data = res.json()
        temp_list = []
        for user in users:
            for i in data['list']:
                weather_day = datetime.fromisoformat(i['dt_txt'])
                if datetime.today().day == weather_day.day:
                    temp_list.append(i['main']['temp'])
                    if weather_day.hour == 12:
                        weather_news = f"<b>{emoji.emojize(':calendar:')} Дата</b> : {i['dt_txt'][:16]}\n" \
                            f"<b>{emoji.emojize(':thermometer:')} Температура</b> : " \
                                       f"{'{0:+3.0f}'.format(i['main']['temp'])}\n" \
                            f"<b>{emoji.emojize(':cloud:')} Небо </b> : {i['weather'][0]['description']}\n" \
                            f"<b>{emoji.emojize(':sunset:')} Максимальная температура</b> : " \
                                       f"{'{0:+3.0f}'.format(max(temp_list))+' °C'}\n" \
                            f"<b>{emoji.emojize(':cityscape:')} Минимальная температура</b> : " \
                                       f"{'{0:+3.0f}'.format(min(temp_list))+' °C'}\n"
            bot.send_message(user[0], f"{emoji.emojize(':school:')} Сегодня погода в Ташкенте"
                                               f"\n\n{weather_news}\n", parse_mode='html')

    except Exception as e:
        print("Exception (forecast):", e)


def timetable():
    try:
        db = PgConn()
        users = db.get_users_id_db()
        today = 'Сегодня '
        everyday_start = 'Сегодняшний экзамен:\n'
        send_mess = ""
        day = ""

        for user in users:
            if datetime.today().month == 6:
                if datetime.today().day == 6:
                    day = f'6 - июня\n'
                    send_mess = f'{everyday_start} КИС "Нима киласила уйга бориб?" (устно) 9-00 587(kaf) Aliyev R.M.'

                elif datetime.today().day == 7:
                    day = f'7 - июня\n'
                    send_mess = f'{everyday_start} ИС на ЖТ "ТОЙЧОК" (устно) 10-00 587 (kaf) Gulyamov J.N'

                elif datetime.today().day == 8:
                    day = f'8 - июня\n'
                    send_mess = f'{everyday_start} ВЕБ "Мужик" (письменно) 9-00 587(kaf) Aliyev R.M.'

                elif datetime.today().day == 9:
                    day = f'9 - июня\n'
                    send_mess = f'{everyday_start} Психолония "керемас фан ©Ислом" (письменно) 10-00 387a (kaf) ' \
                                f"Cho'lponova X.T"

                elif datetime.today().day == 10:
                    day = f'10 - июня\n'
                    send_mess = f'{everyday_start} JAVA "кетти дарсдан" (письменно) 9-00 587 (kaf) Toshmetov T.Sh.'

                elif datetime.today().day == 13:
                    day = f'13 - июня\n'
                    send_mess = f'{everyday_start} Английский "30 та соз" (тест) 10-00 442 Samandarova G.I.'

                elif datetime.today().day == 14:
                    day = f'14 - июня\n'
                    send_mess = f'{everyday_start} ИИС "Тоймаган Тимур" (письменно) 10-00 587 (kaf) Azimov A.'

                elif datetime.today().day == 15:
                    day = f'15 - июня\n'
                    send_mess = f'{everyday_start} ЧС "кейинги дарс дафтарилани текшираман" (письменно) 10-00 457 ' \
                                f'(kaf) Nurmatov X.M'

                elif datetime.today().day == 16:
                    day = f'16 - июня\n'
                    send_mess = f'{everyday_start} Автоматика телемаханика "Как моя фамилия?" (письменно) 08-00 255 ' \
                                f'V.M.Zakirov'

            bot.send_message(user[0], f'{today} {day}\n{send_mess}', parse_mode='html')
    except Exception as e:
        print(e)