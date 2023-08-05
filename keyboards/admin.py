from telebot import types
import emoji
from utils.lang import lang
from config.config import ADMIN


def admin_button(admin_info):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    users_btn = types.KeyboardButton(f"{emoji.emojize(':wheelchair_symbol:')} {lang['Users_btn']}")
    ad_btn = types.KeyboardButton(f"{emoji.emojize(':loudspeaker:')} {lang['Ad_btn']}")
    keyboard.add(users_btn, ad_btn)
    if admin_info == ADMIN:
        admin_btn = types.KeyboardButton(f"{emoji.emojize(':person_in_tuxedo_light_skin_tone:')} "
                                         f"{lang['Admin_btn']}")
        keyboard.add(admin_btn)

    return keyboard


def admin_add_button():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    add_btn = types.KeyboardButton(f"{emoji.emojize(':plus:')} {lang['Add_btn']}")
    edit_btn = types.KeyboardButton(f"{emoji.emojize(':double_curly_loop:')} {lang['Edit_btn']}")
    back_btn = types.KeyboardButton(f"{emoji.emojize(':BACK_arrow:')} {lang['Back_btn']}")
    keyboard.add(add_btn, edit_btn, back_btn)

    return keyboard
