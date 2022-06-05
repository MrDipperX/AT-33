import random
import config
import telebot
from threading import Thread
import time
import schedule
import requests
from hundred_proverbs import parse_proverbs

from db import PgConn
from telebot import types
from datetime import datetime
import json
import emoji

bot = telebot.TeleBot(config.TOKEN)

with open("lang.json", "r", encoding="utf-8") as lang_file:
    lang = json.load(lang_file)

items_btns_kir = ["лаб1", "лаб2", "лаб3", "лаб4", "лаб5", "лаб6", "лаб7", "лаб8", "лаб9", "лаб10", "лаб11", "лаб12",
                  "лаб13", "лаб14", "лаб15", "лаб16", "СР", "ПК", "ИК", "Курс"]
items_btns_lat = ["lab1", "lab2", "lab3", "lab4", "lab5", "lab6", "lab7", "lab8", "lab9", "lab10", "lab11", "lab12",
                  "lab13", "lab14", "lab15", "lab16", "SR", "PK", "IK", "Kurs"]


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id, f"<b>Привет, {message.from_user.first_name}.</b>", parse_mode='html')

    db = PgConn(config.host, config.dbname, config.user, config.port, config.password)
    db.set_time()
    db.create_tables()
    db.add_user(message.from_user.id, message.from_user.first_name, message.date)
    db.add_main_admin()
    menu(message)


@bot.message_handler(commands=['menu'])
def menu(message):
    try:
        db = PgConn(config.host, config.dbname, config.user, config.port, config.password)
        db.set_user_temp(message.from_user.id, "menu_panel")
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        subject_btn = types.KeyboardButton(f"{emoji.emojize(':books:')} {lang['Subjects_btn']}")
        profile_btn = types.KeyboardButton(f"{emoji.emojize(':busts_in_silhouette:')} {lang['Profile_btn']}")
        timetable_btn = types.KeyboardButton(f"{emoji.emojize(':clipboard:')} {lang['Timetable_btn']}")
        proverbs_btn = types.KeyboardButton(f"{emoji.emojize(':speech_balloon:')} {lang['Proverb_btn']}")
        keyboard.add(subject_btn)
        keyboard.add(profile_btn, timetable_btn)
        keyboard.add(proverbs_btn)
        bot.send_message(message.chat.id, f"{lang['Menu']}", parse_mode='html', reply_markup=keyboard)
    except Exception as e:
        print(e)


def set_date_birth(message):
    try:
        db = PgConn(config.host, config.dbname, config.user, config.port, config.password)
        db.add_user_date_birth(message.from_user.id, message.text)
        bot.send_message(message.from_user.id, f'{lang["Correct"]}')
    except Exception as e:
        bot.send_message(message.from_user.id, f'{lang["Rewrite_correct"]}')
        print(e)
        return


def set_user_name(message):
    try:
        db = PgConn(config.host, config.dbname, config.user, config.port, config.password)
        db.add_user_name(message.from_user.id, message.text)
        bot.send_message(message.from_user.id, f'{lang["Correct"]}')
    except Exception as e:
        bot.send_message(message.from_user.id, f'{lang["Rewrite_correct"]}')
        print(e)
        return


@bot.message_handler(commands=['end'])
def finish(message):
    db = PgConn(config.host, config.dbname, config.user, config.port, config.password)
    db.del_user(message.from_user.id)


@bot.message_handler(commands=['restart'])
def restart(message):
    finish(message)
    start(message)


@bot.message_handler(commands=['admin'])
def admin(message):
    try:
        db = PgConn(config.host, config.dbname, config.user, config.port, config.password)
        admin_info = db.get_admin_info(message.from_user.id)
        if admin_info[0] is not None:
            db.set_user_temp(message.from_user.id, "admin_panel")
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            users_btn = types.KeyboardButton(f"{emoji.emojize(':wheelchair_symbol:')} {lang['Users_btn']}")
            ad_btn = types.KeyboardButton(f"{emoji.emojize(':loudspeaker:')} {lang['Ad_btn']}")
            keyboard.add(users_btn, ad_btn)
            if admin_info[0] == 111312651:
                admin_btn = types.KeyboardButton(f"{emoji.emojize(':person_in_tuxedo_light_skin_tone:')} "
                                                 f"{lang['Admin_btn']}")
                keyboard.add(admin_btn)
            bot.send_message(message.from_user.id, f"Добро пожаловать, {admin_info[1]}!", reply_markup=keyboard)
    except Exception as e:
        print(e)


def subject_task_view(message, table_name, list_kir, list_lat):
    try:
        task_btns = []
        db = PgConn(config.host, config.dbname, config.user, config.port, config.password)
        db.set_user_temp(message.from_user.id, table_name)
        for kir, lat in zip(list_kir, list_lat):
            task_status = db.get_task_status(message.from_user.id, table_name, lat)
            if task_status:
                task_btns.append(types.InlineKeyboardButton(f"{kir}{emoji.emojize(':check_mark_button:')}",
                                                            callback_data=f'{lat}'))
            else:
                task_btns.append(types.InlineKeyboardButton(f"{kir}", callback_data=f'{lat}'))
        return task_btns
    except Exception as e:
        print(e)


def del_old_subject(message):
    try:
        db = PgConn(config.host, config.dbname, config.user, config.port, config.password)
        user_temp = db.get_user_temp(message.from_user.id)
        if user_temp == "subjects_panel":
            pass
        else:
            bot.delete_message(message.chat.id, message.message_id - 2)
            bot.delete_message(message.chat.id, message.message_id - 1)
    except Exception as e:
        print(e)


@bot.message_handler(content_types=['contact'])
def get_contact(message):
    try:
        db = PgConn(config.host, config.dbname, config.user, config.port, config.password)
        db.add_user_contact(message.from_user.id, message.contact.phone_number)
        bot.send_message(message.from_user.id, "Номер телефона обновлён!")
    except Exception as e:
        print(e)


def ad_text(message):
    try:
        db = PgConn(config.host, config.dbname, config.user, config.port, config.password)
        db.add_ad_text(message.text)
        bot.send_message(message.from_user.id, lang['Send_pic'])
    except Exception as e:
        print(e)


@bot.message_handler(content_types=['photo'])
def ads_photo(message):
    try:
        db = PgConn(config.host, config.dbname, config.user, config.port, config.password)
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


def send_ads():
    try:
        db = PgConn(config.host, config.dbname, config.user, config.port, config.password)
        users = db.get_all_info_user()
        text_and_url = db.send_add()

        for user in users:
            bot.send_photo(user[3], open(f"{text_and_url[1]}", 'rb'), text_and_url[0])
    except Exception as e:
        print(e)


def add_admin(message):
    try:
        admin_data = message.text.splitlines()
        db = PgConn(config.host, config.dbname, config.user, config.port, config.password)
        db.add_admin(admin_data[0], admin_data[1])
    except Exception as e:
        print(e)


def edit_admin(message):
    try:
        admin_data = message.text.splitlines()
        db = PgConn(config.host, config.dbname, config.user, config.port, config.password)
        db.edit_admin(admin_data[0], admin_data[1])
    except Exception as e:
        print(e)


def is_admin(message):
    try:
        db = PgConn(config.host, config.dbname, config.user, config.port, config.password)
        user_temp = db.get_user_temp(message.from_user.id)
        if user_temp == 'admin_panel':
            return True
        else:
            return False
    except Exception as e:
        print(e)


@bot.message_handler(content_types=['text'])
def mess(message):
    try:
        get_message_bot = message.text.strip()

        inline_markup = types.InlineKeyboardMarkup()

        if get_message_bot == f"{emoji.emojize(':busts_in_silhouette:')} {lang['Profile_btn']}":
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            add_telp_numb_btn = types.KeyboardButton(f"{emoji.emojize(':mobile_phone:')} {lang['Add_telp_numb_btn']}",
                                                     request_contact=True)
            edit_telp_numb_btn = types.KeyboardButton(f"{emoji.emojize(':mobile_phone:')} {lang['Edit_telp_numb_btn']}",
                                                      request_contact=True)
            add_birth_date_btn = types.KeyboardButton(f"{emoji.emojize(':tear-off_calendar:')} "
                                                      f"{lang['Add_birth_date_btn']}")
            edit_birth_date_btn = types.KeyboardButton(f"{emoji.emojize(':tear-off_calendar:')} "
                                                       f"{lang['Edit_birth_date_btn']}")
            add_name_btn = types.KeyboardButton(f"{emoji.emojize(':pencil:')} {lang['Add_name_btn']}")
            edit_name_btn = types.KeyboardButton(f"{emoji.emojize(':pencil:')} {lang['Edit_name_btn']}")
            back_btn = types.KeyboardButton(f"{emoji.emojize(':left_arrow:')} {lang['Back_btn']}")
            db = PgConn(config.host, config.dbname, config.user, config.port, config.password)
            db.set_user_temp(message.from_user.id, 'Profile_panel')
            name, telp_numb, birth_date = db.get_user_info(message.from_user.id)[0]
            if telp_numb is None and birth_date is None and name is None:
                keyboard.add(add_telp_numb_btn, add_birth_date_btn, add_name_btn, back_btn)
                bot.send_message(message.from_user.id, f"Ваше имя: -\nВаш номер телефона: -\nВаш день рождения: -",
                                 reply_markup=keyboard)
            elif telp_numb is None and name is None:
                keyboard.add(add_telp_numb_btn, edit_birth_date_btn, add_name_btn, back_btn)
                bot.send_message(message.from_user.id, f"Ваше имя: -\nВаш номер телефона: -\nВаш день рождения: "
                                                       f"{birth_date}", reply_markup=keyboard)
            elif birth_date is None and name is None:
                keyboard.add(edit_telp_numb_btn, add_birth_date_btn, add_name_btn, back_btn)
                bot.send_message(message.from_user.id, f"Ваш ник: -\nВаш номер телефона: {telp_numb}\n"
                                                       f"Ваш день рождения: -", reply_markup=keyboard)

            elif telp_numb is None and birth_date is None:
                keyboard.add(add_telp_numb_btn, add_birth_date_btn, edit_name_btn, back_btn)
                bot.send_message(message.from_user.id, f"Ваше имя: {name}\nВаш номер телефона: -\nВаш день рождения: "
                                                       f"-", reply_markup=keyboard)

            elif telp_numb is None:
                keyboard.add(add_telp_numb_btn, edit_birth_date_btn, edit_name_btn, back_btn)
                bot.send_message(message.from_user.id, f"Ваше имя: {name}\nВаш номер телефона: -\nВаш день рождения: "
                                                       f"{birth_date}", reply_markup=keyboard)

            elif name is None:
                keyboard.add(edit_telp_numb_btn, edit_birth_date_btn, add_name_btn, back_btn)
                bot.send_message(message.from_user.id, f"Ваше имя: -\nВаш номер телефона: {telp_numb}\n"
                                                       f"Ваш день рождения: {birth_date}", reply_markup=keyboard)

            elif birth_date is None:
                keyboard.add(edit_telp_numb_btn, add_birth_date_btn, edit_name_btn, back_btn)
                bot.send_message(message.from_user.id, f"Ваше имя: {name}\nВаш номер телефона: {telp_numb}\nВаш день "
                                                       f"рождения: -", reply_markup=keyboard)

            else:
                keyboard.add(edit_telp_numb_btn, edit_birth_date_btn, edit_name_btn, back_btn)
                bot.send_message(message.from_user.id, f"Ваш ник: {name}\nВаш номер телефона: {telp_numb}\n"
                                                       f"Ваш день рождения: {birth_date}", reply_markup=keyboard)

        elif get_message_bot == f"{emoji.emojize(':tear-off_calendar:')} {lang['Add_birth_date_btn']}":
            bot.send_message(message.from_user.id, "Вводите дату рождения в формате: '26-10-2001'!")
            bot.register_next_step_handler(message, set_date_birth)

        elif get_message_bot == f"{emoji.emojize(':tear-off_calendar:')} {lang['Edit_birth_date_btn']}":
            bot.send_message(message.from_user.id, "Вводите дату рождения в формате: '26-10-2001'!")
            bot.register_next_step_handler(message, set_date_birth)

        elif get_message_bot == f"{emoji.emojize(':pencil:')} {lang['Add_name_btn']}":
            bot.send_message(message.from_user.id, "Введите ваше настоящее имя!")
            bot.register_next_step_handler(message, set_user_name)

        elif get_message_bot == f"{emoji.emojize(':pencil:')} {lang['Edit_name_btn']}":
            bot.send_message(message.from_user.id, "Введите ваше новое имя!")
            bot.register_next_step_handler(message, set_user_name)

        elif get_message_bot == f"{emoji.emojize(':clipboard:')} {lang['Timetable_btn']}":
            db = PgConn(config.host, config.dbname, config.user, config.port, config.password)
            db.set_user_temp(message.from_user.id, 'Timetable_panel')
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            monday_btn = types.KeyboardButton(f"{emoji.emojize(':keycap_1:')} {lang['Monday_btn']}")
            tuesday_btn = types.KeyboardButton(f"{emoji.emojize(':keycap_2:')} {lang['Tuesday_btn']}")
            wednesday_btn = types.KeyboardButton(f"{emoji.emojize(':keycap_3:')} {lang['Wednesday_btn']}")
            thursday_btn = types.KeyboardButton(f"{emoji.emojize(':keycap_4:')} {lang['Thursday_btn']}")
            friday_btn = types.KeyboardButton(f"{emoji.emojize(':keycap_5:')} {lang['Friday_btn']}")
            back_btn = types.KeyboardButton(f"{emoji.emojize(':left_arrow:')} {lang['Back_btn']}")
            keyboard.add(monday_btn, tuesday_btn, wednesday_btn, thursday_btn, friday_btn, back_btn)
            bot.send_message(message.from_user.id, "Выберите день", reply_markup=keyboard)

        elif get_message_bot == f"{emoji.emojize(':speech_balloon:')} {lang['Proverb_btn']}":
            random_proverb = random.choice(parse_proverbs())
            bot.send_message(message.from_user.id, f'<b>{random_proverb}</b>', parse_mode='html')

        elif get_message_bot == f"{emoji.emojize(':books:')} {lang['Subjects_btn']}":
            db = PgConn(config.host, config.dbname, config.user, config.port, config.password)
            db.set_user_temp(message.from_user.id, "subjects_panel")
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            eng_btn = types.KeyboardButton(f"{emoji.emojize(':United_Kingdom:')} {lang['Eng_btn']}")
            kis_btn = types.KeyboardButton(f"{emoji.emojize(':card_file_box:')} {lang['Kis_btn']}")
            iis_btn = types.KeyboardButton(f"{emoji.emojize(':atom_symbol:')} {lang['Iis_btn']}")
            java_btn = types.KeyboardButton(f"{emoji.emojize(':hot_beverage:')} {lang['Java_btn']}")
            web_btn = types.KeyboardButton(f"{emoji.emojize(':globe_with_meridians:')} {lang['Web_btn']}")
            info_sys_btn = types.KeyboardButton(f"{emoji.emojize(':satellite:')} {lang['Info_sys_btn']}")
            tech_auto_btn = types.KeyboardButton(f"{emoji.emojize(':battery:')} {lang['Tech_auto_btn']}")
            psy_btn = types.KeyboardButton(f"{emoji.emojize(':speaking_head:')} {lang['Psychology_btn']}")
            graj_zash_btn = types.KeyboardButton(f"{emoji.emojize(':shield:')} {lang['Graj_zash_btn']}")
            back_btn = types.KeyboardButton(f"{emoji.emojize(':left_arrow:')} {lang['Back_btn']}")
            keyboard.add(eng_btn, kis_btn, iis_btn, java_btn, web_btn, info_sys_btn, tech_auto_btn, psy_btn,
                         graj_zash_btn, back_btn)
            bot.send_message(message.from_user.id, "Предметы", reply_markup=keyboard)

        elif get_message_bot == f"{emoji.emojize(':United_Kingdom:')} {lang['Eng_btn']}":
            del_old_subject(message)
            eng_task_btns = subject_task_view(message, "English", items_btns_kir[-4:-1], items_btns_lat[-4:-1])
            inline_markup.add(*eng_task_btns)
            bot.send_message(message.from_user.id, lang['Eng_btn'], reply_markup=inline_markup)

        elif get_message_bot == f"{emoji.emojize(':card_file_box:')} {lang['Kis_btn']}":
            del_old_subject(message)
            kis_items_kir = items_btns_kir[0:8] + items_btns_kir[-3:]
            kis_items_lat = items_btns_lat[0:8] + items_btns_lat[-3:]
            kis_task_btns = subject_task_view(message, "KIS", kis_items_kir, kis_items_lat)
            inline_markup.add(*kis_task_btns)
            bot.send_message(message.from_user.id, lang['Kis_btn'], reply_markup=inline_markup)

        elif get_message_bot == f"{emoji.emojize(':atom_symbol:')} {lang['Iis_btn']}":
            del_old_subject(message)
            iis_items_kir = items_btns_kir[0:8] + items_btns_kir[-4:-1]
            iis_items_lat = items_btns_lat[0:8] + items_btns_lat[-4:-1]
            kis_task_btns = subject_task_view(message, "IIS", iis_items_kir, iis_items_lat)
            inline_markup.add(*kis_task_btns)
            bot.send_message(message.from_user.id, lang['Iis_btn'], reply_markup=inline_markup)

        elif get_message_bot == f"{emoji.emojize(':hot_beverage:')} {lang['Java_btn']}":
            del_old_subject(message)
            java_items_kir = items_btns_kir[0:5] + items_btns_kir[-4:-1]
            java_items_lat = items_btns_lat[0:5] + items_btns_lat[-4:-1]
            java_task_btns = subject_task_view(message, "Java", java_items_kir, java_items_lat)
            inline_markup.add(*java_task_btns)
            bot.send_message(message.from_user.id, lang['Java_btn'], reply_markup=inline_markup)

        elif get_message_bot == f"{emoji.emojize(':globe_with_meridians:')} {lang['Web_btn']}":
            del_old_subject(message)
            web_items_kir = items_btns_kir[0:7] + items_btns_kir[-3:]
            web_items_lat = items_btns_lat[0:7] + items_btns_lat[-3:]
            web_task_btns = subject_task_view(message, "WEB", web_items_kir, web_items_lat)
            inline_markup.add(*web_task_btns)
            bot.send_message(message.from_user.id, lang['Web_btn'], reply_markup=inline_markup)

        elif get_message_bot == f"{emoji.emojize(':satellite:')} {lang['Info_sys_btn']}":
            del_old_subject(message)
            info_sys_items_kir = items_btns_kir[0:8] + items_btns_kir[-4:-1]
            info_sys_items_lat = items_btns_lat[0:8] + items_btns_lat[-4:-1]
            info_sys_task_btns = subject_task_view(message, "Info_sys", info_sys_items_kir, info_sys_items_lat)
            inline_markup.add(*info_sys_task_btns)
            bot.send_message(message.from_user.id, lang['Info_sys_btn'], reply_markup=inline_markup)

        elif get_message_bot == f"{emoji.emojize(':battery:')} {lang['Tech_auto_btn']}":
            del_old_subject(message)
            tech_auto_task_btns = subject_task_view(message, "Tech_auto", items_btns_kir[:19], items_btns_lat[:19])
            inline_markup.add(*tech_auto_task_btns)
            bot.send_message(message.from_user.id, lang['Tech_auto_btn'], reply_markup=inline_markup)

        elif get_message_bot == f"{emoji.emojize(':speaking_head:')} {lang['Psychology_btn']}":
            del_old_subject(message)
            psy_task_btns = subject_task_view(message, "Psychology", items_btns_kir[-4:-1], items_btns_lat[-4:-1])
            inline_markup.add(*psy_task_btns)
            bot.send_message(message.from_user.id, lang['Psychology_btn'], reply_markup=inline_markup)

        elif get_message_bot == f"{emoji.emojize(':shield:')} {lang['Graj_zash_btn']}":
            del_old_subject(message)
            gz_task_btns = subject_task_view(message, "Graj_zash", items_btns_kir[-4:-1], items_btns_lat[-4:-1])
            inline_markup.add(*gz_task_btns)
            bot.send_message(message.from_user.id, lang['Graj_zash_btn'], reply_markup=inline_markup)

        elif get_message_bot == f"{emoji.emojize(':person_in_tuxedo_light_skin_tone:')} {lang['Admin_btn']}":
            if is_admin(message):
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
                add_btn = types.KeyboardButton(f"{emoji.emojize(':plus:')} {lang['Add_btn']}")
                edit_btn = types.KeyboardButton(f"{emoji.emojize(':double_curly_loop:')} {lang['Edit_btn']}")
                back_btn = types.KeyboardButton(f"{emoji.emojize(':BACK_arrow:')} {lang['Back_btn']}")
                keyboard.add(add_btn, edit_btn, back_btn)
                bot.send_message(message.from_user.id, "Выберите", reply_markup=keyboard)
            else:
                pass

        elif get_message_bot == f"{emoji.emojize(':plus:')} {lang['Add_btn']}":
            if is_admin(message):
                bot.send_message(message.from_user.id, "Введите данные нового админа")
                bot.register_next_step_handler(message, add_admin)
            else:
                pass

        elif get_message_bot == f"{emoji.emojize(':double_curly_loop:')} {lang['Edit_btn']}":
            if is_admin(message):
                bot.send_message(message.from_user.id, "Введите изминения")
                bot.register_next_step_handler(message, edit_admin)
            else:
                pass

        elif get_message_bot == f"{emoji.emojize(':BACK_arrow:')} {lang['Back_btn']}":
            admin(message)

        elif get_message_bot == f"{emoji.emojize(':wheelchair_symbol:')} {lang['Users_btn']}":
            if is_admin(message):
                db = PgConn(config.host, config.dbname, config.user, config.port, config.password)
                users = db.get_all_info_user()
                users_list = 'Имя   |   Никнейм   |   Номер тел\n--------------------------------------------------\n\n'
                for i in range(len(users)):
                    users_list += f'{users[i - 1][0]} | {users[i - 1][1]} | {users[i - 1][2]}\n'
                bot.send_message(message.from_user.id, users_list)
            else:
                pass

        elif get_message_bot == f"{emoji.emojize(':loudspeaker:')} {lang['Ad_btn']}":
            if is_admin(message):
                bot.send_message(message.from_user.id, lang['Write_ad_text'])
                bot.register_next_step_handler(message, ad_text)
            else:
                pass

        elif get_message_bot == f"{emoji.emojize(':keycap_1:')} {lang['Monday_btn']}":
            bot.send_message(message.from_user.id, "<b>1.Граж. защита(прак) | 454\n2.ИИС(лб) | 583a\n3.КИС(лб) | 583a"
                                                   "</b>", parse_mode='html')

        elif get_message_bot == f"{emoji.emojize(':keycap_2:')} {lang['Tuesday_btn']}":
            bot.send_message(message.from_user.id, "<b>1.ИИС(лек) | 588\n2.КИС(лек) | 589\n3.Java(лб) | 585</b>",
                             parse_mode='html')

        elif get_message_bot == f"{emoji.emojize(':keycap_3:')} {lang['Wednesday_btn']}":
            bot.send_message(message.from_user.id, "<b>1.ВЕБ(лб) | 580\n2.Java(лек) | 589\n3.Психология | 384</b>",
                             parse_mode='html')

        elif get_message_bot == f"{emoji.emojize(':keycap_4:')} {lang['Thursday_btn']}":
            bot.send_message(message.from_user.id, "<b>1.ВЕБ(лек) | 581\n2.Тех. авто.(лек) | 255 / Граж. защита(прак)"
                                                   " | 454\n3.Тех. авто.(лб) | 255</b>", parse_mode='html')

        elif get_message_bot == f"{emoji.emojize(':keycap_5:')} {lang['Friday_btn']}":
            bot.send_message(message.from_user.id, "<b>1.Инф. сис.(лек) | 589\n2.Англ. язык | 398а\n3.Инф. сис.(лб) | "
                                                   "583</b>", parse_mode='html')

        elif get_message_bot == f"{emoji.emojize(':left_arrow:')} {lang['Back_btn']}":
            db = PgConn(config.host, config.dbname, config.user, config.port, config.password)
            user_tmp = db.get_user_temp(message.from_user.id)
            if user_tmp in ['English', 'WEB', 'Java', 'KIS', 'IIS', 'Info_sys', 'Tech_auto', 'Psychology', 'Graj_zash']:
                del_old_subject(message)
            else:
                pass
            menu(message)

        else:
            pass
    except Exception as e:
        print(e)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    try:
        if call.data in items_btns_lat:
            db = PgConn(config.host, config.dbname, config.user, config.port, config.password)
            subject_panel = db.get_user_temp(call.message.chat.id)
            db.set_task_status(call.message.chat.id, subject_panel, call.data, True)
    except Exception as e:
        print(e)


def happy_birthday():
    try:
        db = PgConn(config.host, config.dbname, config.user, config.port, config.password)
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
    db = PgConn(config.host, config.dbname, config.user, config.port, config.password)
    users = db.get_users_id_db()
    weather_news = ''
    try:
        res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                           params={'id': config.city_id, 'units': 'metric', 'lang': 'ru', 'APPID': config.appid})
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
        db = PgConn(config.host, config.dbname, config.user, config.port, config.password)
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


def main_loop():
    thread = Thread(target=do_schedule)
    thread.start()
    bot.polling(none_stop=True)


if __name__ == '__main__':
    main_loop()
