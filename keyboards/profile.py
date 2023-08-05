from telebot import types
import emoji
from utils.lang import lang
from config.config import ADMIN


def profile_button(telp_numb, birth_date, name):

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

    if telp_numb is None and birth_date is None and name is None:
        keyboard.add(add_telp_numb_btn, add_birth_date_btn, add_name_btn, back_btn)
        text = f"Ваше имя: -\nВаш номер телефона: -\nВаш день рождения: -"

    elif telp_numb is None and name is None:
        keyboard.add(add_telp_numb_btn, edit_birth_date_btn, add_name_btn, back_btn)
        text = f"Ваше имя: -\nВаш номер телефона: -\nВаш день рождения: {birth_date}"

    elif birth_date is None and name is None:
        keyboard.add(edit_telp_numb_btn, add_birth_date_btn, add_name_btn, back_btn)
        text = f"Ваш ник: -\nВаш номер телефона: {telp_numb}\nВаш день рождения: -"

    elif telp_numb is None and birth_date is None:
        keyboard.add(add_telp_numb_btn, add_birth_date_btn, edit_name_btn, back_btn)
        text = f"Ваше имя: {name}\nВаш номер телефона: -\nВаш день рождения: -"

    elif telp_numb is None:
        keyboard.add(add_telp_numb_btn, edit_birth_date_btn, edit_name_btn, back_btn)
        text = f"Ваше имя: {name}\nВаш номер телефона: -\nВаш день рождения: {birth_date}"

    elif name is None:
        keyboard.add(edit_telp_numb_btn, edit_birth_date_btn, add_name_btn, back_btn)
        text = f"Ваше имя: -\nВаш номер телефона: {telp_numb}\n Ваш день рождения: {birth_date}"

    elif birth_date is None:
        keyboard.add(edit_telp_numb_btn, add_birth_date_btn, edit_name_btn, back_btn)
        text = f"Ваше имя: {name}\nВаш номер телефона: {telp_numb}\nВаш день рождения: -"
    else:
        keyboard.add(edit_telp_numb_btn, edit_birth_date_btn, edit_name_btn, back_btn)
        text = f"Ваш ник: {name}\nВаш номер телефона: {telp_numb}\nВаш день рождения: {birth_date}"

    return keyboard, text
