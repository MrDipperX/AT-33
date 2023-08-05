from telebot import types
import emoji
from utils.lang import lang


def menu_button():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    subject_btn = types.KeyboardButton(f"{emoji.emojize(':books:')} {lang['Subjects_btn']}")
    profile_btn = types.KeyboardButton(f"{emoji.emojize(':busts_in_silhouette:')} {lang['Profile_btn']}")
    timetable_btn = types.KeyboardButton(f"{emoji.emojize(':clipboard:')} {lang['Timetable_btn']}")
    proverbs_btn = types.KeyboardButton(f"{emoji.emojize(':speech_balloon:')} {lang['Proverb_btn']}")
    keyboard.add(subject_btn)
    keyboard.add(profile_btn, timetable_btn)
    keyboard.add(proverbs_btn)

    return keyboard

