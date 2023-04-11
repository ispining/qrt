import datetime
import random
import threading

from sources.config import *
from sources import texts


def fake_subs_loop():



    last_update = datetime.datetime.now()
    while True:
        secs = random.randint(1, 3 )
        peoples = random.randint(1, 5)
        while datetime.datetime.now() < last_update + datetime.timedelta(seconds=secs):
            time.sleep(10)

        def f():
            try:
                settings("fake_subs", str(int(settings("fake_subs")) + peoples))
                last_update = datetime.datetime.now()
            except:
                time.sleep(5)
                f()
        f()


def fake_views_loop():


    last_update = datetime.datetime.now()
    while True:

        secs = random.randint(1, 3)
        while last_update + datetime.timedelta(seconds=secs) > datetime.datetime.now():
            time.sleep(10)

        for soft in Softs().get(status="confirmed"):
            def f():
                try:
                    fv = Fake_views(soft['row_id'])
                    amount = fv.get() + random.randint(1, 5)
                    fv.set(amount)
                except:
                    time.sleep(5)
                    f()
            f()


threading.Thread(target=fake_subs_loop, daemon=True).start()
threading.main_thread()

threading.Thread(target=fake_views_loop, daemon=True).start()
threading.main_thread()


def start_message(chat_id):
    k = kmarkup()
    msg = texts.Content.start_message.format(**{
        "subs": str(settings("fake_subs")),
        "coders": str(len(Developers().get(status="regular")))
    })
    k.row(btn(texts.Buttons.dev_panel, callback_data="dev_panel"))
    # k.row(btn(texts.Buttons.bots, callback_data="bots_panel"), btn(texts.Buttons.scrypts, callback_data="scrypts_panel"))
    k.row(btn(texts.Buttons.catalog, callback_data="catalog||1"))
    k.row(btn(texts.Buttons.find_developer, callback_data="find_developer||1"))
    #k.row(btn(texts.Buttons.another_dev, callback_data="another_dev"))
    k.row(btn(texts.Buttons.garant, url="https://t.me/TGguaranteeService"))
    send(chat_id, msg, reply_markup=k)


class Admin:
    def __init__(self, chat_id):
        self.chat_id = chat_id

    def panel(self):
        k = kmarkup()
        msg = texts.Content.admin_panel
        k.row(btn(texts.Buttons.dev_checking, callback_data=f"admin_dev_checking"))
        k.row(btn(texts.Buttons.soft_checking, callback_data=f"admin_soft_checking"))
        k.row(back('home'))
        send(self.chat_id, msg, reply_markup=k)

    def dev_checking(self):
        k = kmarkup()
        msg = texts.Content.admin_dev_checking
        for user in Developers().get():
            try:
                k.row(btn(bot.get_chat(int(user['user_id'])).first_name, callback_data=f"admin_pre_view_dev||{user['user_id']}"))
            except:
                Developers(user['user_id']).remove()
        k.row(back("admin_panel"))
        send(self.chat_id, msg, reply_markup=k)

    def pre_view_dev(self, user_id):
        developer = Developers(user_id).get()
        k = kmarkup()
        msg = texts.Content.admin_pre_view_dev.format(**{
            "user_id": developer['user_id'],
            "username": bot.get_chat(int(developer['user_id'])).username,
            "bio": developer['bio']
        })
        k.row(btn(texts.Buttons.yes, callback_data=f"confirm_developer||{developer['user_id']}"),
              btn(texts.Buttons.no, callback_data=f"deni_developer||{developer['user_id']}"))
        k.row(back("admin_dev_checking"))
        send(self.chat_id, msg, reply_markup=k)

    def confirm_developer(self, user_id):
        developer = Developers(user_id)
        developer.set("status", "regular", ['user_id', user_id])
        crm = CRM(user_id)
        if not crm.exists():
            crm.new()

        self.panel()

    def deni_developer(self, user_id):
        developer = Developers(user_id)
        developer.remove()

        self.panel()

    def soft_checking(self):
        k = kmarkup()
        msg = texts.Content.soft_checking
        for soft in Softs().get(status="None"):
            k.row(btn(soft['soft_name'], callback_data=f"admin_check_soft||{str(soft['row_id'])}"))
        k.row(back(f"admin_panel"))
        send(self.chat_id, msg, reply_markup=k)

    def check_soft(self, soft_id):
        s = Softs(soft_id=soft_id)
        s.set('status', 'confirmed', ['row_id', soft_id])
        soft = s.get()
        k = kmarkup()
        msg = texts.Content.check_soft.format(**{
            "user_id": soft['developer_id'],
            "username": bot.get_chat(int(soft['developer_id'])).username,
            "s_name": soft['soft_name'],
            "s_desc": soft['soft_desc'],
            "s_link": soft['soft_link']
        })

        k.row(btn(texts.Buttons.yes, callback_data=f"admin_soft_confirm||{soft_id}"),
              btn(texts.Buttons.no, callback_data=f"admin_soft_deni||{soft_id}"))
        k.row(back("admin_soft_checking"))
        send(self.chat_id, msg, reply_markup=k)

    def soft_confirm(self, soft_id):
        s = Softs(soft_id=soft_id)
        s.set('status', 'confirmed', ['row_id', soft_id])

        msg = texts.Content.admin_soft_confirmed
        send(self.chat_id, msg)
        self.soft_checking()

        user_id = int(Softs(soft_id=soft_id).get()['developer_id'])
        send(user_id, texts.Content.dev_soft_confirmed)

    def soft_deni(self, soft_id):
        s = Softs(soft_id=soft_id)
        s.remove()

        msg = texts.Content.admin_soft_denied
        send(self.chat_id, msg)
        self.soft_checking()

        user_id = int(s.get()['developer_id'])
        send(user_id, texts.Content.dev_soft_denied)


class Developer:
    def __init__(self, chat_id):
        self.chat_id = chat_id

    def panel(self):
        k = kmarkup()
        msg = texts.Content.developer_panel
        k.row(btn(texts.Buttons.mySoft, callback_data=f"dev_my_soft"))
        k.row(btn(texts.Buttons.edit_info, callback_data="edit_personal_info"))
        k.row(btn(texts.Buttons.balance, callback_data=f"dev_balance"))
        k.row(back("home"))
        send(self.chat_id, msg, reply_markup=k)

    def dev_my_soft(self):
        k = kmarkup()
        msg = texts.Content.my_soft
        k.row(btn(texts.Buttons.add, callback_data=f"dev_add_softs"))
        for soft in Softs(developer_id=self.chat_id).get():
            if soft['status'] == "confirmed":
                k.row(btn(soft['soft_name'], callback_data=f"dev_select_soft||{soft['row_id']}"))
        k.row(back("dev_panel"))
        send(self.chat_id, msg, reply_markup=k)

    def add_softs(self):
        k = kmarkup()
        msg = texts.Content.dev_add_softs
        k.row(back(f"dev_my_soft"))
        send(self.chat_id, msg, reply_markup=k)
        database.stages(self.chat_id, f"add_softs")

    def add_softs_name(self, soft_name):
        soft_id = str(random.randint(1, 999999999))
        soft = Softs(developer_id=self.chat_id, soft_id=soft_id)
        soft.new(soft_name=soft_name,
                 soft_desc="None",
                 soft_link="None")

        k = kmarkup()
        msg = texts.Content.add_soft_desc

        k.row(back(f'dev_add_softs'))
        send(self.chat_id, msg, reply_markup=k)
        database.stages(self.chat_id, f"add_soft_desc||{str(soft_id)}")

    def add_soft_desc(self, soft_id, soft_desc):
        soft = Softs(developer_id=self.chat_id, soft_id=soft_id)
        soft.set("soft_desc", soft_desc, ["row_id", soft_id])

        k = kmarkup()
        msg = texts.Content.add_soft_link

        k.row(back(f'dev_add_softs'))
        send(self.chat_id, msg, reply_markup=k)
        database.stages(self.chat_id, f"add_soft_link||{str(soft_id)}")

    def not_a_dev(self):
        k = kmarkup()
        msg = texts.Content.panel_not_a_dev
        k.row(btn(texts.Buttons.reg_dev, callback_data=f"reg_dev"))
        k.row(back("home"))
        send(self.chat_id, msg, reply_markup=k)

    def register(self):
        k = kmarkup()
        msg = texts.Content.register_as_developer
        k.row(back("dev_panel"))
        send(self.chat_id, msg, reply_markup=k)
        stages(self.chat_id, "reg_vev_new_bio")

    def reg_rev_new_bio(self, bio):
        developer = Developers(self.chat_id)
        developer.new()
        developer.set("bio", bio, ['user_id', str(self.chat_id)])
        developer.set("status", "checking", ['user_id', str(self.chat_id)])

        msg = texts.Content.reg_rev_new
        send(self.chat_id, msg)

        start_message(self.chat_id)

    def checking(self, call):
        bot.answer_callback_query(call.id, texts.Alerts.Callback.checking_a_developer, show_alert=True)

    def add_soft_link(self, soft_id, link):
        soft = Softs(developer_id=self.chat_id, soft_id=soft_id)
        soft.set("soft_link", link, ["row_id", soft_id])

        msg = texts.Content.added_soft_link
        send(self.chat_id, msg)

        self.panel()

    def soft_panel(self, soft_id):
        soft = Softs(soft_id=soft_id).get()

        k = kmarkup()
        msg = texts.Content.soft_panel.format(**{
            "soft_id": soft['row_id'],
            "s_name": soft['soft_name'],
            "s_desc": soft['soft_desc'],
            "s_link": soft['soft_link'],
            "s_views": str(Fake_views(soft['row_id']).get())
        })
        k.row(btn(texts.Buttons.edit_soft_name, callback_data=f"edit_soft_name||{str(soft['row_id'])}"))
        k.row(btn(texts.Buttons.edit_soft_desc, callback_data=f"edit_soft_desc||{str(soft['row_id'])}"))
        k.row(btn(texts.Buttons.edit_soft_link, callback_data=f"edit_soft_link||{str(soft['row_id'])}"))
        k.row(btn(texts.Buttons.delete, callback_data=f"delete_soft||{str(soft_id)}"))

        k.row(back('dev_my_soft'))
        send(self.chat_id, msg, reply_markup=k)

    def edit_soft_name(self, soft_id):
        k = kmarkup()
        msg = texts.Content.edit_soft_name
        k.row(back(f"dev_select_soft||{soft_id}"))
        send(self.chat_id, msg, reply_markup=k)
        stages(self.chat_id, f"edit_soft_name||{str(soft_id)}")

    def soft_name_edited(self, soft_id, soft_name):
        soft = Softs(soft_id=soft_id)
        soft.set("soft_name", soft_name, ['row_id', soft_id])

        send(self.chat_id, texts.Content.soft_name_edited)

        self.soft_panel(soft_id=soft_id)
        database.stages(self.chat_id, "None")

    def edit_soft_desc(self, soft_id):
        k = kmarkup()
        msg = texts.Content.edit_soft_desc
        k.row(back(f"dev_select_soft||{soft_id}"))
        send(self.chat_id, msg, reply_markup=k)
        stages(self.chat_id, f"edit_soft_desc||{str(soft_id)}")

    def soft_desc_edited(self, soft_id, soft_desc):
        soft = Softs(soft_id=soft_id)
        soft.set("soft_desc", soft_desc, ['row_id', soft_id])

        send(self.chat_id, texts.Content.soft_desc_edited)

        self.soft_panel(soft_id=soft_id)
        database.stages(self.chat_id, "None")

    def edit_soft_link(self, soft_id):
        k = kmarkup()
        msg = texts.Content.edit_soft_link
        k.row(back(f"dev_select_soft||{soft_id}"))
        send(self.chat_id, msg, reply_markup=k)
        stages(self.chat_id, f"edit_soft_link||{str(soft_id)}")

    def soft_link_edited(self, soft_id, soft_link):
        soft = Softs(soft_id=soft_id)
        soft.set("soft_link", soft_link, ['row_id', soft_id])

        send(self.chat_id, texts.Content.soft_link_edited)

        self.soft_panel(soft_id=soft_id)
        database.stages(self.chat_id, "None")

    def delete_soft(self, soft_id):
        soft = Softs(soft_id=soft_id)
        soft.remove()

        msg = texts.Content.soft_deleted
        send(self.chat_id, msg)

        self.dev_my_soft()

    def edit_personal_info(self):
        k = kmarkup()
        pd = PersonalData(self.chat_id)
        if not pd.exists():
            pd.new("None", "None", "None", "None")
        user_data = pd.get()
        dev = Developers(self.chat_id).get()
        msg = texts.Content.edit_personal_info.format(**{
            "country": user_data['country'],
            "city": user_data['city'],
            "phone1": user_data['phone1'],
            "phone2": user_data['phone2'],
            "link1": dev['link1'],
            "link2": dev['link2']
        })
        k.row(btn(texts.Buttons.locations, callback_data=f"sdgdsg"))
        k.row(btn(texts.Buttons.edit_country, callback_data=f"dev_edit_country"),
              btn(texts.Buttons.edit_city, callback_data=f"dev_edit_city"))
        k.row(btn(texts.Buttons.phones, callback_data=f"gdfg"))
        k.row(btn(texts.Buttons.edit_phone1, callback_data=f"dev_edit_phone1"),
              btn(texts.Buttons.edit_phone2, callback_data=f"dev_edit_phone2"))
        k.row(btn(texts.Buttons.links, callback_data=f"fghfgd"))
        k.row(btn(texts.Buttons.edit_link1, callback_data=f"dev_edit_link1"),
              btn(texts.Buttons.edit_link2, callback_data=f"dev_edit_link2"))

        k.row(back("dev_panel"))
        send(self.chat_id, msg, reply_markup=k)

    def dev_edit_phone1(self):
        k = kmarkup()
        msg = texts.Content.dev_edit_phone1
        k.row(back("edit_personal_info"))
        send(self.chat_id, msg, reply_markup=k)
        database.stages(self.chat_id, f"dev_edit_phone1")

    def dev_edit_phone2(self):
        k = kmarkup()
        msg = texts.Content.dev_edit_phone2
        k.row(back("edit_personal_info"))
        send(self.chat_id, msg, reply_markup=k)
        database.stages(self.chat_id, f"dev_edit_phone2")

    def dev_phone1_edited(self, new_phone):
        PersonalData(self.chat_id).set("phone1", new_phone, ["user_id", str(self.chat_id)])

        msg = texts.Content.dev_phone1_edited
        send(self.chat_id, msg)
        self.edit_personal_info()
        database.stages(self.chat_id, "None")

    def dev_phone2_edited(self, new_phone):
        PersonalData(self.chat_id).set("phone2", new_phone, ["user_id", str(self.chat_id)])

        msg = texts.Content.dev_phone2_edited
        send(self.chat_id, msg)
        self.edit_personal_info()
        database.stages(self.chat_id, "None")

    def dev_edit_link1(self):
        k = kmarkup()
        msg = texts.Content.dev_edit_link1
        k.row(back("edit_personal_info"))
        send(self.chat_id, msg, reply_markup=k)
        database.stages(self.chat_id, f"dev_edit_link1")

    def dev_link1_edited(self, new_link):
        Developers(self.chat_id).set("link1", new_link, ["user_id", str(self.chat_id)])

        msg = texts.Content.dev_link1_edited
        send(self.chat_id, msg)
        self.edit_personal_info()
        database.stages(self.chat_id, "None")

    def dev_edit_link2(self):
        k = kmarkup()
        msg = texts.Content.dev_edit_link2
        k.row(back("edit_personal_info"))
        send(self.chat_id, msg, reply_markup=k)
        database.stages(self.chat_id, f"dev_edit_link2")

    def dev_link2_edited(self, new_link):
        Developers(self.chat_id).set("link2", new_link, ["user_id", str(self.chat_id)])

        msg = texts.Content.dev_link2_edited
        send(self.chat_id, msg)
        self.edit_personal_info()
        database.stages(self.chat_id, "None")

    def dev_edit_country(self):
        k = kmarkup()
        msg = texts.Content.dev_edit_country
        k.row(back("edit_personal_info"))
        send(self.chat_id, msg, reply_markup=k)
        database.stages(self.chat_id, f"dev_edit_country")

    def dev_country_edited(self, country):
        PersonalData(self.chat_id).set("country", country, ["user_id", str(self.chat_id)])

        msg = texts.Content.dev_country_edited
        send(self.chat_id, msg)
        self.edit_personal_info()
        database.stages(self.chat_id, "None")

    def dev_edit_city(self):
        k = kmarkup()
        msg = texts.Content.dev_edit_city
        k.row(back("edit_personal_info"))
        send(self.chat_id, msg, reply_markup=k)
        database.stages(self.chat_id, f"dev_edit_city")

    def dev_city_edited(self, city):
        PersonalData(self.chat_id).set("city", city, ["user_id", str(self.chat_id)])

        msg = texts.Content.dev_city_edited
        send(self.chat_id, msg)
        self.edit_personal_info()
        database.stages(self.chat_id, "None")

    def dev_balance(self):
        k = kmarkup()
        msg = texts.Content.dev_balance.format(**{
            "bal": str(database.balance(self.chat_id))
        })
        k.row(btn(texts.Buttons.dev_add_money, callback_data=f"dev_add_money"))
        k.row(back("dev_panel"))
        send(self.chat_id, msg, reply_markup=k)

    def dev_add_money(self):
        k = kmarkup()
        msg = texts.Content.dev_add_money.format(**{"wallet": "13EYqHMnQ5v4RkEadaf495k42LmFynKk7A"}) #Dcent
        k.row(back(f"dev_balance"))
        bot.send_photo(chat_id=self.chat_id,
                       photo="AgACAgQAAxkBAAIBa2Q0oaWY3sft1nBnoULEze3Gp3hjAAJOvTEbgfygUZ7M-mzXZypZAQADAgADeQADLwQ",
                       caption=msg, reply_markup=k)
        database.stages(self.chat_id, "dev_add_money")

    def dev_add_money_link(self, link):
        k = kmarkup()
        msg = texts.Content.dev_add_money_link
        k.row(back('dev_add_money'))
        send(self.chat_id, msg, reply_markup=k)

        send(admin_id, f"Balance \n\nuser id: {self.chat_id}\nlink:\n<code>{link}</code>")


class Customer:
    def __init__(self, chat_id):
        self.chat_id = chat_id

    def catalog(self, list_num=1):
        k = kmarkup()
        msg = texts.Content.client_catalog

        minimum = list_num
        maximum = minimum + 10
        num = 1
        for soft in Softs().get(status="confirmed"):
            if all((num >= minimum, num <= maximum)):
                k.row(btn(soft['soft_name'], callback_data=f"client_soft_select||{soft['row_id']}"))
            num += 1

        btns = []
        if list_num > 1:
            btns.append(btn("<<<", callback_data=f"catalog||{str(list_num + 10)}"))
        if len(Softs().get(status="confirmed")) > maximum:
            btns.append(btn(">>>", callback_data=f"catalog||{str(list_num - 10)}"))

        if len(btns) == 1:
            k.row(btns[0])
        elif len(btns) == 2:
            k.row(btns[0], btns[1])

        k.row(back("home"))
        send(self.chat_id, msg, reply_markup=k)

    def client_soft_select(self, soft_id):
        soft = Softs(soft_id=soft_id).get()
        k = kmarkup()
        msg = texts.Content.client_soft_select.format(**{
            "name": soft['soft_name'],
            "desc": soft['soft_desc'],
            "developer": bot.get_chat(int(soft['developer_id'])).username,
            "s_views": str(Fake_views(soft['row_id']).get())

        })
        k.row(btn("Посетить", url=soft["soft_link"]))
        k.row(back("catalog||1"))
        send(self.chat_id, msg, reply_markup=k)

    def find_developer(self, list_num=1):
        k = kmarkup()
        msg = texts.Content.find_developer

        minimum = int(list_num)
        maximum = minimum + 10
        num = 1
        for dev in Developers().get(status="regular"):
            if all((num >= minimum, num <= maximum)):
                k.row(btn(bot.get_chat(int(dev['user_id'])).first_name, callback_data=f"client_dev_select||{dev['user_id']}"))
            num += 1

        btns = []
        if minimum > 1:
            btns.append(btn("<<<", callback_data=f"find_developer||{str(minimum + 10)}"))
        if len(Developers().get(status="regular")) > maximum:
            btns.append(btn(">>>", callback_data=f"find_developer||{str(minimum - 10)}"))

        if len(btns) == 1:
            k.row(btns[0])
        elif len(btns) == 2:
            k.row(btns[0], btns[1])

        k.row(back("home"))
        send(self.chat_id, msg, reply_markup=k)

    def client_dev_panel(self, dev_id):
        k = kmarkup()
        developer = PersonalData(dev_id)
        if not developer.exists():
            developer.new("None", "None", "None", "None")

        developer = PersonalData(dev_id).get()

        phone1 = "Не назначено"
        if developer['phone1'] != "None":
            phone1 = developer['phone1']
        phone2 = "Не назначено"
        if developer['phone2'] != "None":
            phone2 = developer['phone2']
        country = "Не назначено"
        if developer['country'] != "None":
            country = developer['country']
        city = "Не назначено"
        if developer['city'] != "None":
            city = developer['city']

        pnum = 0
        projects = Softs(developer['user_id']).get()
        for i in projects:
            if i['status'] == "confirmed":
                pnum += 1
        msg = texts.Content.client_dev_panel.format(**{
            "title": bot.get_chat(int(developer['user_id'])).first_name,
            "username": bot.get_chat(int(developer['user_id'])).username,
            "phone1": phone1,
            "phone2": phone2,
            "country": country,
            "city": city,
            "projects_num": pnum
        })
        k.row(btn(texts.Buttons.client_dev_softs, callback_data=f"client_dev_softs||{str(dev_id)}"))
        k.row(btn(texts.Buttons.contact_dev, url=f"https://t.me/{bot.get_chat(dev_id).username}"))
        k.row(back(f"find_developer||1"))
        send(self.chat_id, msg, reply_markup=k)

    def client_dev_softs(self, dev_id):

        k = kmarkup()
        msg = texts.Content.client_dev_softs.format(**{"dev_username": bot.get_chat(int(dev_id)).username})
        for soft in Softs(developer_id=dev_id).get():
            if soft['status'] == "confirmed":
                k.row(btn(soft['soft_name'], callback_data=f"client_dev_soft_selected||{dev_id}||{soft['row_id']}"))
        k.row(back(f"client_dev_select||{dev_id}"))
        send(self.chat_id, msg, reply_markup=k)

    def client_dev_soft_selected(self, dev_id, soft_id):
        soft = Softs(soft_id=soft_id).get()
        k = kmarkup()
        msg = texts.Content.client_dev_soft_selected.format(**{
            "name": soft['soft_name'],
            "desc": soft['soft_desc'],
            "developer": bot.get_chat(int(dev_id)).username,
            "s_views": str(Fake_views(soft['row_id']).get())

        })
        k.row(btn("Посетить", url=soft['soft_link']))
        k.row(back(f"client_dev_softs||{dev_id}"))
        send(self.chat_id, msg, reply_markup=k)


