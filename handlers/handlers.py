from loader import bot
from db.db import PgConn

from keyboards.menu import menu_button
from keyboards.admin import admin_button
from utils.lang import lang
from datetime import datetime


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id, f"<b>Привет, {message.from_user.first_name}.</b>", parse_mode='html')

    db = PgConn()
    # db.set_time()

    db.add_user(message.from_user.id, message.from_user.first_name, message.date)
    db.add_main_admin()
    menu(message)


@bot.message_handler(commands=['menu'])
def menu(message):
    try:
        db = PgConn()
        db.set_user_temp(message.from_user.id, "menu_panel")

        bot.send_message(message.chat.id, f"{lang['Menu']}", parse_mode='html', reply_markup=menu_button())
    except Exception as e:
        print(e)


@bot.message_handler(commands=['end'])
def finish(message):
    db = PgConn()
    db.del_user(message.from_user.id)


@bot.message_handler(commands=['restart'])
def restart(message):
    finish(message)
    start(message)


@bot.message_handler(commands=['admin'])
def admin(message):
    try:
        db = PgConn()
        user_id = message.from_user.id
        admin_info = db.get_admin_info(user_id)
        if admin_info[0] is not None:
            db.set_user_temp(user_id, "admin_panel")

            bot.send_message(user_id, f"Добро пожаловать, {admin_info[1]}!", reply_markup=admin_button(admin_info[0]))
    except Exception as e:
        print(e)


@bot.message_handler(content_types=['contact'])
def get_contact(message):
    try:
        db = PgConn()
        db.add_user_contact(message.from_user.id, message.contact.phone_number)
        bot.send_message(message.from_user.id, "Номер телефона обновлён!")
    except Exception as e:
        print(e)


@bot.message_handler(content_types=['photo'])
def ads_photo(message):
    try:
        db = PgConn()
        user_temp = db.get_user_temp(message.from_user.id)
        if user_temp == "admin_panel":
            file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            now = datetime.now()
            src = f'Ads/{now.year}_{now.month}_{now.day}_{now.hour}_{now.minute}_{now.second}.jpg'
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)
            db.add_ad_photo(src)
            bot.send_message(message.from_user.id, lang['Correct'])
            send_ads()
        else:
            pass
    except Exception as e:
        print(e)