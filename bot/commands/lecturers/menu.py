from aiogram.types import CallbackQuery
from aiogram.types import Message

from bot import bot
from bot import dispatcher

from bot import students
from bot import metrics

from bot.commands.lecturers.utilities.keyboards import lecturer_chooser
from bot.commands.lecturers.utilities.keyboards import lecturer_info_type_chooser
from bot.commands.lecturers.utilities.constants import MAX_LECTURERS_NUMBER

from bot.shared.keyboards import cancel_option
from bot.shared.helpers import top_notification
from bot.shared.api.constants import LOADING_REPLIES
from bot.shared.api.types import ResponseError
from bot.shared.api.lecturers import get_lecturers_names
from bot.shared.commands import Commands

from random import choice


@dispatcher.message_handler(
    lambda message: students[message.chat.id].guard.text is None,
    commands=[ Commands.LECTURERS.value ]
)
@metrics.increment(Commands.LECTURERS)
async def lecturers(message: Message):
    guard_message: Message = await bot.send_message(
        chat_id=message.chat.id,
        text="Отправь фамилию или ФИО преподавателя.",
        reply_markup=cancel_option()
    )
    
    students[message.chat.id].guard.text = Commands.LECTURERS_NAME.value
    students[message.chat.id].guard.message = guard_message

@dispatcher.message_handler(lambda message: students[message.chat.id].guard.text == Commands.LECTURERS_NAME.value)
async def find_lecturer(message: Message):
    await bot.delete_message(
        chat_id=message.chat.id,
        message_id=message.message_id
    )
    await bot.edit_message_text(
        chat_id=students[message.chat.id].guard.message.chat.id,
        message_id=students[message.chat.id].guard.message.message_id,
        text=choice(LOADING_REPLIES)
    )
    
    names: [{str: str}] = get_lecturers_names(name_part=message.text)
    
    if names is None:
        await bot.edit_message_text(
            chat_id=students[message.chat.id].guard.message.chat.id,
            message_id=students[message.chat.id].guard.message.message_id,
            text=ResponseError.NO_RESPONSE.value,
            disable_web_page_preview=True
        )
        
        students[message.chat.id].guard.drop()
        return
    elif len(names) == 0:
        await bot.edit_message_text(
            chat_id=students[message.chat.id].guard.message.chat.id,
            message_id=students[message.chat.id].guard.message.message_id,
            text="Ничего не найдено :("
        )
        
        students[message.chat.id].guard.drop()
        return
    elif len(names) > MAX_LECTURERS_NUMBER:
        await bot.edit_message_text(
            chat_id=students[message.chat.id].guard.message.chat.id,
            message_id=students[message.chat.id].guard.message.message_id,
            text="Слишком мало букв, слишком много преподавателей…"
        )
        
        students[message.chat.id].guard.drop()
        return
    
    await bot.edit_message_text(
        chat_id=students[message.chat.id].guard.message.chat.id,
        message_id=students[message.chat.id].guard.message.message_id,
        text="Выбери преподавателя:",
        reply_markup=lecturer_chooser(names=names)
    )
    
    students[message.chat.id].guard.text = Commands.LECTURERS.value

@dispatcher.callback_query_handler(
    lambda callback:
        students[callback.message.chat.id].guard.text == Commands.LECTURERS.value and
        Commands.LECTURERS.value in callback.data
)
@top_notification
async def lecturers_schedule_type(callback: CallbackQuery):
    await bot.edit_message_text(
        chat_id=callback.message.chat.id,
        message_id=callback.message.message_id,
        text="Тебе нужны преподавателевы:",
        reply_markup=lecturer_info_type_chooser(lecturer_id=callback.data.split()[1])
    )