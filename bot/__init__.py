from telebot import TeleBot
from telebot import apihelper

from bot.helpers           import load_from
from bot.helpers.metrics   import Metrics
from bot.helpers.constants import TOKEN

from sys import argv
from random import choice


# Bypassing the lockout of Russian government
apihelper.proxy = { "https": "socks5://163.172.152.192:1080" }


# Main data setup
kbot = TeleBot(TOKEN, threaded=False)
students = load_from(filename="data/users")
metrics = Metrics()


# Used to show "Loading..." notification on the top in a cleverer way
def top_notification(callback_handler):
    def wrapper(callback):
        callback_handler(callback)
        
        apihelper.answer_callback_query(
            token=TOKEN,
            callback_query_id=callback.id,
            cache_time=0
        )
    
    return wrapper


# Polling launcher
def main():
    if len(argv) == 2 and argv[1] == "t":
        print("Launched in test mode...")
        kbot.polling()
    elif len(argv) == 2 and argv[1] == "i":
        print("Launched in infinity mode...")
        kbot.infinity_polling(True)
    else:
        print(
            "\n"
            "  Incorrect options!\n\n"
            "> python3 startup.py t - to launch in test mode\n"
            "> python3 startup.py i - to launch in infinity mode\n"
        )


# All the commands & other stuff handlers
from bot import handlers
