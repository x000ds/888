from aiogram.types import Message

from bot import bot
from bot import dispatcher

from bot import students

from bot.shared.commands import Commands


@dispatcher.message_handler(
    lambda message:
        students[message.chat.id].guard.text is not None and
        Commands.LOGIN.value in students[message.chat.id].guard.text
)
async def guard(message: Message): await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)