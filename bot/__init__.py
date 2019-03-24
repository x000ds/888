from telebot import TeleBot
from telebot import apihelper

from bot.constants import TOKEN
from bot.helpers   import load_users

from sys import argv

apihelper.proxy = { "https": "socks5://163.172.152.192:1080" }
kaishnik = TeleBot(TOKEN, threaded=False)
students = load_users()

from bot import handlers

def main():
    if len(argv) == 1:
        print("Launched in test mode")
        kaishnik.polling()
    else:
        print("Launched in infinite mode")
        kaishnik.infinity_polling(True)
