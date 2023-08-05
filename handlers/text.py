from loader import bot
from db.db import PgConn
from utils.constants import subjects

from utils.hundred_proverbs import parse_proverbs
from utils.lang import lang
import emoji
import random
from utils.constants import items_btns_kir, items_btns_lat

from utils.helpers import set_date_birth, set_user_name, del_old_subject, is_admin, add_admin, ad_text, edit_admin
from handlers.handlers import menu, admin

from keyboards.profile import profile_button
from keyboards.timetable import timetable_button
from keyboards.subjects import subjects_button, subject_task_buttons
from keyboards.admin import admin_add_button


@bot.message_handler(content_types=['text'])
def mess(message):
    try:
        get_message_bot = message.text.strip()

        user_id = message.from_user.id

        if get_message_bot == f"{emoji.emojize(':busts_in_silhouette:')} {lang['Profile_btn']}":

            db = PgConn()
            db.set_user_temp(user_id, 'Profile_panel')
            name, telp_numb, birth_date = db.get_user_info(user_id)[0]

            keyboard, text = profile_button(telp_numb, birth_date, name)

            bot.send_message(user_id, text, reply_markup=keyboard)

        elif get_message_bot == f"{emoji.emojize(':tear-off_calendar:')} {lang['Add_birth_date_btn']}":
            bot.send_message(user_id, lang['Birthday_pattern'])
            bot.register_next_step_handler(message, set_date_birth)

        elif get_message_bot == f"{emoji.emojize(':tear-off_calendar:')} {lang['Edit_birth_date_btn']}":
            bot.send_message(user_id, lang['Birthday_pattern'])
            bot.register_next_step_handler(message, set_date_birth)

        elif get_message_bot == f"{emoji.emojize(':pencil:')} {lang['Add_name_btn']}":
            bot.send_message(user_id, lang['Real_name'])
            bot.register_next_step_handler(message, set_user_name)

        elif get_message_bot == f"{emoji.emojize(':pencil:')} {lang['Edit_name_btn']}":
            bot.send_message(user_id, lang['Edit_name'])
            bot.register_next_step_handler(message, set_user_name)

        elif get_message_bot == f"{emoji.emojize(':clipboard:')} {lang['Timetable_btn']}":
            db = PgConn()
            db.set_user_temp(user_id, 'Timetable_panel')

            bot.send_message(user_id, lang['Choose_day'], reply_markup=timetable_button())

        elif get_message_bot == f"{emoji.emojize(':speech_balloon:')} {lang['Proverb_btn']}":
            random_proverb = random.choice(parse_proverbs())
            bot.send_message(user_id, f'<b>{random_proverb}</b>', parse_mode='html')

        elif get_message_bot == f"{emoji.emojize(':books:')} {lang['Subjects_btn']}":
            db = PgConn()
            db.set_user_temp(user_id, "subjects_panel")
            bot.send_message(user_id, lang['Subjects_btn'], reply_markup=subjects_button())

        elif get_message_bot == f"{emoji.emojize(':United_Kingdom:')} {lang['Eng_btn']}":
            del_old_subject(message)
            eng_task_btns = subject_task_buttons(user_id, "english", items_btns_kir[-4:-1], items_btns_lat[-4:-1])
            bot.send_message(user_id, lang['Eng_btn'], reply_markup=eng_task_btns)

        elif get_message_bot == f"{emoji.emojize(':card_file_box:')} {lang['Kis_btn']}":
            del_old_subject(message)
            kis_items_kir = items_btns_kir[0:8] + items_btns_kir[-3:]
            kis_items_lat = items_btns_lat[0:8] + items_btns_lat[-3:]
            kis_task_btns = subject_task_buttons(user_id, "kis", kis_items_kir, kis_items_lat)
            bot.send_message(user_id, lang['Kis_btn'], reply_markup=kis_task_btns)

        elif get_message_bot == f"{emoji.emojize(':atom_symbol:')} {lang['Iis_btn']}":
            del_old_subject(message)
            iis_items_kir = items_btns_kir[0:8] + items_btns_kir[-4:-1]
            iis_items_lat = items_btns_lat[0:8] + items_btns_lat[-4:-1]
            kis_task_btns = subject_task_buttons(user_id, "iis", iis_items_kir, iis_items_lat)
            bot.send_message(user_id, lang['Iis_btn'], reply_markup=kis_task_btns)

        elif get_message_bot == f"{emoji.emojize(':hot_beverage:')} {lang['Java_btn']}":
            del_old_subject(message)
            java_items_kir = items_btns_kir[0:5] + items_btns_kir[-4:-1]
            java_items_lat = items_btns_lat[0:5] + items_btns_lat[-4:-1]
            java_task_btns = subject_task_buttons(user_id, "java", java_items_kir, java_items_lat)
            bot.send_message(user_id, lang['Java_btn'], reply_markup=java_task_btns)

        elif get_message_bot == f"{emoji.emojize(':globe_with_meridians:')} {lang['Web_btn']}":
            del_old_subject(message)
            web_items_kir = items_btns_kir[0:7] + items_btns_kir[-3:]
            web_items_lat = items_btns_lat[0:7] + items_btns_lat[-3:]
            web_task_btns = subject_task_buttons(user_id, "web", web_items_kir, web_items_lat)
            bot.send_message(user_id, lang['Web_btn'], reply_markup=web_task_btns)

        elif get_message_bot == f"{emoji.emojize(':satellite:')} {lang['Info_sys_btn']}":
            del_old_subject(message)
            info_sys_items_kir = items_btns_kir[0:8] + items_btns_kir[-4:-1]
            info_sys_items_lat = items_btns_lat[0:8] + items_btns_lat[-4:-1]
            info_sys_task_btns = subject_task_buttons(user_id, "info_sys", info_sys_items_kir, info_sys_items_lat)
            bot.send_message(user_id, lang['Info_sys_btn'], reply_markup=info_sys_task_btns)

        elif get_message_bot == f"{emoji.emojize(':battery:')} {lang['Tech_auto_btn']}":
            del_old_subject(message)
            tech_auto_task_btns = subject_task_buttons(user_id, "tech_auto", items_btns_kir[:19], items_btns_lat[:19])
            bot.send_message(user_id, lang['Tech_auto_btn'], reply_markup=tech_auto_task_btns)

        elif get_message_bot == f"{emoji.emojize(':speaking_head:')} {lang['Psychology_btn']}":
            del_old_subject(message)
            psy_task_btns = subject_task_buttons(user_id, "psychology", items_btns_kir[-4:-1], items_btns_lat[-4:-1])
            bot.send_message(user_id, lang['Psychology_btn'], reply_markup=psy_task_btns)

        elif get_message_bot == f"{emoji.emojize(':shield:')} {lang['Graj_zash_btn']}":
            del_old_subject(message)
            gz_task_btns = subject_task_buttons(user_id, "graj_zash", items_btns_kir[-4:-1], items_btns_lat[-4:-1])
            bot.send_message(user_id, lang['Graj_zash_btn'], reply_markup=gz_task_btns)

        elif get_message_bot == f"{emoji.emojize(':person_in_tuxedo_light_skin_tone:')} {lang['Admin_btn']}":
            if is_admin(message):

                bot.send_message(user_id, "Выберите", reply_markup=admin_add_button())
            else:
                pass

        elif get_message_bot == f"{emoji.emojize(':plus:')} {lang['Add_btn']}":
            if is_admin(message):
                bot.send_message(user_id, lang['New_admin_data'])
                bot.register_next_step_handler(message, add_admin)
            else:
                pass

        elif get_message_bot == f"{emoji.emojize(':double_curly_loop:')} {lang['Edit_btn']}":
            if is_admin(message):
                bot.send_message(user_id, lang['Send_edit'])
                bot.register_next_step_handler(message, edit_admin)
            else:
                pass

        elif get_message_bot == f"{emoji.emojize(':BACK_arrow:')} {lang['Back_btn']}":
            admin(message)

        elif get_message_bot == f"{emoji.emojize(':wheelchair_symbol:')} {lang['Users_btn']}":
            if is_admin(message):
                db = PgConn()
                users = db.get_all_info_user()
                users_list = lang['User_list']
                for i in range(len(users)):
                    users_list += f'{users[i - 1][0]} | {users[i - 1][1]} | {users[i - 1][2]}\n'
                bot.send_message(user_id, users_list)
            else:
                pass

        elif get_message_bot == f"{emoji.emojize(':loudspeaker:')} {lang['Ad_btn']}":
            if is_admin(message):
                bot.send_message(user_id, lang['Write_ad_text'])
                bot.register_next_step_handler(message, ad_text)
            else:
                pass

        elif get_message_bot == f"{emoji.emojize(':keycap_1:')} {lang['Monday_btn']}":
            bot.send_message(user_id, "<b>1.Граж. защита(прак) | 454\n2.ИИС(лб) | 583a\n3.КИС(лб) | 583a</b>",
                             parse_mode='html')

        elif get_message_bot == f"{emoji.emojize(':keycap_2:')} {lang['Tuesday_btn']}":
            bot.send_message(user_id, "<b>1.ИИС(лек) | 588\n2.КИС(лек) | 589\n3.Java(лб) | 585</b>",
                             parse_mode='html')

        elif get_message_bot == f"{emoji.emojize(':keycap_3:')} {lang['Wednesday_btn']}":
            bot.send_message(user_id, "<b>1.ВЕБ(лб) | 580\n2.Java(лек) | 589\n3.Психология | 384</b>",
                             parse_mode='html')

        elif get_message_bot == f"{emoji.emojize(':keycap_4:')} {lang['Thursday_btn']}":
            bot.send_message(user_id, "<b>1.ВЕБ(лек) | 581\n2.Тех. авто.(лек) | 255 / Граж. защита(прак)"
                                      " | 454\n3.Тех. авто.(лб) | 255</b>", parse_mode='html')

        elif get_message_bot == f"{emoji.emojize(':keycap_5:')} {lang['Friday_btn']}":
            bot.send_message(user_id, "<b>1.Инф. сис.(лек) | 589\n2.Англ. язык | 398а\n3.Инф. сис.(лб) | 583</b>",
                             parse_mode='html')

        elif get_message_bot == f"{emoji.emojize(':left_arrow:')} {lang['Back_btn']}":
            db = PgConn()
            user_tmp = db.get_user_temp(user_id)
            if user_tmp in subjects:
                del_old_subject(message)
            else:
                pass
            menu(message)

        else:
            pass
    except Exception as e:
        print(e)
