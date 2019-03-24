from bot import kaishnik
from bot import students

from bot.constants import BRS

from bot.keyboards import remove_keyboard
from bot.keyboards import skipper

@kaishnik.message_handler(commands=["card"])
def card(message):
    kaishnik.send_chat_action(chat_id=message.chat.id, action="typing")
    
    if students[message.chat.id].get_student_card_number() is None:
        kaishnik.send_message(
            chat_id=message.chat.id,
            text="Отправь номер своей зачётки "
                 "(интересный факт — номер твоего студенческого и номер твоей зачётки одинаковы!).",
            reply_markup=remove_keyboard()
        )
        kaishnik.send_message(
            chat_id=message.chat.id,
            text="Можешь не указывать, если не хочешь, но баллы показать не смогу.",
            reply_markup=skipper(
                text="пропустить",
                callback_data="skip"
            )
        )
    elif students[message.chat.id].get_institute() == "КИТ":
        kaishnik.send_message(
            chat_id=message.chat.id,
            text="Не доступно :("
        )
    else:
        kaishnik.send_message(
            chat_id=message.chat.id,
            text=students[message.chat.id].get_card(),
            parse_mode="Markdown"
        )

@kaishnik.message_handler(commands=["brs"])
def brs(message):
    kaishnik.send_chat_action(chat_id=message.chat.id, action="typing")
        
    kaishnik.send_message(
        chat_id=message.chat.id,
        text=BRS,
        parse_mode="Markdown"
    )

