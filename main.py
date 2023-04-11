import requests
import telebot

from sources.config import *
from sources import stg, models


@bot.message_handler(commands=['start'])
def start_handler(message):
    chat_id = message.chat.id
    Sub(chat_id).update()
    stg.start_message(chat_id)


@bot.message_handler(commands=['admin'])
def admin_panel(message):
    chat_id = message.chat.id
    stg.Admin(chat_id).panel()


@bot.message_handler(content_types=['photo'])
def allphotos(message):
    photo_id = message.photo[-1].file_id
    print(photo_id)


@bot.message_handler(content_types=['text'])
def text_handler(message):
    chat_id = message.chat.id
    if message.chat.type == "private":
        Sub(chat_id).update()
        stage = stages(chat_id)
        cd = stage.split("||")

        if cd[0] == "add_softs":
            #
            stg.Developer(chat_id).add_softs_name(message.text)
        elif cd[0] == "add_soft_desc":
            #
            stg.Developer(chat_id).add_soft_desc(cd[1], message.text)
        elif cd[0] == "reg_vev_new_bio":
            #
            stg.Developer(chat_id).reg_rev_new_bio(message.text)
        elif cd[0] == "add_soft_link":
            #
            stg.Developer(chat_id).add_soft_link(cd[1], message.text)
        elif cd[0] == "edit_soft_name":
            #
            stg.Developer(chat_id).soft_name_edited(cd[1], message.text)
        elif cd[0] == "edit_soft_desc":
            #
            stg.Developer(chat_id).soft_desc_edited(cd[1], message.text)
        elif cd[0] == "edit_soft_link":
            #
            stg.Developer(chat_id).soft_link_edited(cd[1], message.text)
        elif cd[0] == "dev_edit_link1":
            #
            stg.Developer(chat_id).dev_link1_edited(message.text)
        elif cd[0] == "dev_edit_link2":
            #
            stg.Developer(chat_id).dev_link2_edited(message.text)
        elif cd[0] == "dev_edit_phone1":
            #
            stg.Developer(chat_id).dev_phone1_edited(message.text)
        elif cd[0] == "dev_edit_phone2":
            #
            stg.Developer(chat_id).dev_phone2_edited(message.text)
        elif cd[0] == "dev_edit_country":
            #
            stg.Developer(chat_id).dev_country_edited(message.text)
        elif cd[0] == "dev_edit_city":
            #
            stg.Developer(chat_id).dev_city_edited(message.text)
        elif cd[0] == "dev_add_money":
            #
            stg.Developer(chat_id).dev_add_money_link(message.text)


@bot.callback_query_handler(func=lambda m: True)
def callbacks_handler(call):
    chat_id = call.message.chat.id
    cd = call.data.split("||")

    def dm():
        try:
            bot.delete_message(chat_id, call.message.message_id)
        except:
            pass

    if call.message.chat.type == "private":
        if cd[0] == "dev_panel":
            if call.message.chat.username == None:
                bot.answer_callback_query(call.id, stg.texts.Alerts.Callback.only_with_username, show_alert=True)
            else:
                d = Developers(chat_id).get()
                if d == None:
                    stg.Developer(chat_id).not_a_dev()
                    dm()
                elif d['status'] == "regular":
                    stg.Developer(chat_id).panel()
                    dm()
                elif d['status'] == "checking":
                    stg.Developer(chat_id).checking(call)
        elif cd[0] == "dev_my_soft":
            stg.Developer(chat_id).dev_my_soft()
            dm()
        elif cd[0] == "home":
            start_handler(call.message)
            dm()
        elif cd[0] == "dev_add_softs":
            stg.Developer(chat_id).add_softs()
            dm()
        elif cd[0] == "add_softs":
            stg.Developer(chat_id).add_softs()
            dm()
        elif cd[0] == "reg_dev":
            stg.Developer(chat_id).register()
            dm()
        elif cd[0] == "admin_panel":
            stg.Admin(chat_id).panel()
            dm()
        elif cd[0] == "admin_dev_checking":
            stg.Admin(chat_id).dev_checking()
            dm()
        elif cd[0] == "admin_pre_view_dev":
            stg.Admin(chat_id).pre_view_dev(cd[1])
            dm()
        elif cd[0] == "confirm_developer":
            stg.Admin(chat_id).confirm_developer(cd[1])
            dm()
        elif cd[0] == "deni_developer":
            stg.Admin(chat_id).deni_developer(cd[1])
            dm()
        elif cd[0] == "admin_soft_checking":
            stg.Admin(chat_id).soft_checking()
            dm()
        elif cd[0] == "admin_check_soft":
            stg.Admin(chat_id).check_soft(cd[1])
            dm()
        elif cd[0] == "admin_soft_confirm":
            stg.Admin(chat_id).soft_confirm(cd[1])
            dm()
        elif cd[0] == "admin_soft_deni":
            stg.Admin(chat_id).soft_deni(cd[1])
            dm()
        elif cd[0] == "dev_select_soft":
            stg.Developer(chat_id).soft_panel(cd[1])
            dm()
        elif cd[0] == "edit_soft_name":
            stg.Developer(chat_id).edit_soft_name(cd[1])
            dm()
        elif cd[0] == "delete_soft":
            stg.Developer(chat_id).delete_soft(cd[1])
            dm()
        elif cd[0] == "edit_soft_desc":
            stg.Developer(chat_id).edit_soft_desc(cd[1])
            dm()
        elif cd[0] == "edit_soft_link":
            stg.Developer(chat_id).edit_soft_link(cd[1])
            dm()
        elif cd[0] == "edit_personal_info":
            stg.Developer(chat_id).edit_personal_info()
            dm()
        elif cd[0] == "dev_edit_phone1":
            stg.Developer(chat_id).dev_edit_phone1()
            dm()
        elif cd[0] == "dev_edit_phone2":
            stg.Developer(chat_id).dev_edit_phone2()
            dm()
        elif cd[0] == "dev_edit_link1":
            stg.Developer(chat_id).dev_edit_link1()
            dm()
        elif cd[0] == "dev_edit_link2":
            stg.Developer(chat_id).dev_edit_link2()
            dm()
        elif cd[0] == "dev_edit_country":
            stg.Developer(chat_id).dev_edit_country()
            dm()
        elif cd[0] == "dev_edit_city":
            stg.Developer(chat_id).dev_edit_city()
            dm()
        elif cd[0] == "catalog":
            stg.Customer(chat_id).catalog(int(cd[1]))
            dm()
        elif cd[0] == "client_soft_select":
            stg.Customer(chat_id).client_soft_select(cd[1])
            dm()
        elif cd[0] == "find_developer":
            stg.Customer(chat_id).find_developer(cd[1])
            dm()
        elif cd[0] == "client_dev_select":
            stg.Customer(chat_id).client_dev_panel(cd[1])
            dm()
        elif cd[0] == "client_dev_softs":
            stg.Customer(chat_id).client_dev_softs(cd[1])
            dm()
        elif cd[0] == "client_dev_soft_selected":
            stg.Customer(chat_id).client_dev_soft_selected(cd[1], cd[2])
            dm()
        elif cd[0] == "dev_balance":
            stg.Developer(chat_id).dev_balance()
            dm()
        elif cd[0] == "dev_add_money":
            stg.Developer(chat_id).dev_add_money()
            dm()


def botstart():
    while True:
        try:
            bot.polling()
        except telebot.apihelper.ApiTelegramException:
            time.sleep(5)
        except requests.exceptions.ReadTimeout:
            time.sleep(5)



botstart()
