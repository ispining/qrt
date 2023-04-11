import iluxaMod as ilm

tgbot = ilm.tgBot(open("connectors\\TOKEN", "r").read())
bot = tgbot.bot
kmarkup = tgbot.kmarkup
btn = tgbot.btn
def back(callback_data):
    return tgbot.back(callback_data=callback_data, bname="Назад")
send = tgbot.send

bot.parse_mode = "HTML"