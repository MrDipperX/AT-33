from telebot import types
import emoji
from utils.lang import lang

from utils.helpers import subject_task_view


def subjects_button():
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

    return keyboard


def subject_task_buttons(user_id, subject, items_kir, items_lat):
    inline_markup = types.InlineKeyboardMarkup()

    task_btns = subject_task_view(user_id, subject, items_kir, items_lat)
    task_btns = [types.InlineKeyboardButton(text=task[0], callback_data=task[1]) for task in task_btns]
    inline_markup.add(*task_btns)

    return inline_markup