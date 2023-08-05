from telebot import types
import emoji
from utils.lang import lang


def timetable_button():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    monday_btn = types.KeyboardButton(f"{emoji.emojize(':keycap_1:')} {lang['Monday_btn']}")
    tuesday_btn = types.KeyboardButton(f"{emoji.emojize(':keycap_2:')} {lang['Tuesday_btn']}")
    wednesday_btn = types.KeyboardButton(f"{emoji.emojize(':keycap_3:')} {lang['Wednesday_btn']}")
    thursday_btn = types.KeyboardButton(f"{emoji.emojize(':keycap_4:')} {lang['Thursday_btn']}")
    friday_btn = types.KeyboardButton(f"{emoji.emojize(':keycap_5:')} {lang['Friday_btn']}")
    back_btn = types.KeyboardButton(f"{emoji.emojize(':left_arrow:')} {lang['Back_btn']}")
    keyboard.add(monday_btn, tuesday_btn, wednesday_btn, thursday_btn, friday_btn, back_btn)

    return keyboard