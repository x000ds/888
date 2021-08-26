from typing import List

from random import choice

from aiogram.types import Message
from aiogram.types import CallbackQuery
from aiogram.types import ChatType
from aiogram.types import ParseMode

from bot.platforms.telegram import dispatcher
from bot.platforms.telegram import guards
from bot.platforms.telegram import states

from bot.platforms.telegram.commands.score.utilities.keyboards import semester_chooser
from bot.platforms.telegram.commands.score.utilities.keyboards import subjects_type_chooser
from bot.platforms.telegram.commands.score.utilities.keyboards import subject_chooser
from bot.platforms.telegram.commands.score.utilities.helpers import collect_subjects

from bot.platforms.telegram.utilities.helpers import top_notification

from bot.models.user import User

from bot.utilities.helpers import note_metrics
from bot.utilities.types import Platform
from bot.utilities.types import Command
from bot.utilities.api.constants import LOADING_REPLIES
from bot.utilities.api.student import get_last_available_semester
from bot.utilities.api.student import get_scoretable


@dispatcher.message_handler(
    lambda message: message.chat.type != ChatType.PRIVATE,
    commands=[ Command.SCORE.value ]
)
@dispatcher.message_handler(
    lambda message:
        message.chat.type == ChatType.PRIVATE and
        guards[message.chat.id].text is None,
    commands=[ Command.SCORE.value ]
)
@note_metrics(platform=Platform.TELEGRAM, command=Command.SCORE)
async def choose_semester(message: Message):
    user: User = User.get(User.telegram_id == message.chat.id)
    
    if user.bb_login is None or user.bb_password is None:
        await message.answer(text="Не доступно :(")
        
        if message.chat.type == ChatType.PRIVATE:
            await message.answer(text="Чтобы видеть баллы, нужно отправить /login и войти через ББ.")
        
        return
    
    loading_message: Message = await message.answer(
        text=choice(LOADING_REPLIES),
        disable_web_page_preview=True
    )
    
    (last_available_semester, response_error) = get_last_available_semester(user_id=user.user_id)
    
    if last_available_semester is None:
        await loading_message.edit_text(
            text=response_error.value,
            disable_web_page_preview=True
        )
        return
    
    await loading_message.edit_text(
        text="Выбери номер семестра:",
        reply_markup=semester_chooser(last_available_semester)
    )
    
    guards[message.chat.id].text = Command.SCORE.value

@dispatcher.callback_query_handler(
    lambda callback:
        guards[callback.message.chat.id].text == Command.SCORE.value and
        Command.SCORE_SEMESTER.value in callback.data
)
@top_notification
async def choose_subjects_type(callback: CallbackQuery):
    await callback.message.edit_text(
        text=choice(LOADING_REPLIES),
        disable_web_page_preview=True
    )
    
    user: User = User.get(User.telegram_id == callback.message.chat.id)
    
    semester: str = callback.data.split()[1]
    (scoretable, response_error) = get_scoretable(semester=semester, user_id=user.user_id)
    
    if scoretable is None:
        await callback.message.edit_text(
            text=response_error.value,
            disable_web_page_preview=True
        )
        
        guards[callback.message.chat.id].drop()
        return
    
    states[callback.message.chat.id].scoretable = scoretable
    
    await callback.message.edit_text(
        text="Выбери тип предметов:",
        reply_markup=subjects_type_chooser(
            has_exams=any(map(lambda score: ScoreSubjectType.EXAM.value in score[1], scoretable)),
            has_courseworks=any(map(lambda score: ScoreSubjectType.COURSEWORK.value in score[1], scoretable)),
            has_tests=any(map(lambda score: ScoreSubjectType.TEST.value in score[1], scoretable))
        )
    )

@dispatcher.callback_query_handler(
    lambda callback:
        guards[callback.message.chat.id].text == Command.SCORE.value and any([
            callback.data == Command.SCORE_ALL.value,
            callback.data == Command.SCORE_EXAMS.value,
            callback.data == Command.SCORE_COURSEWORKS.value,
            callback.data == Command.SCORE_TESTS.value
        ])
)
@top_notification
async def choose_subject(callback: CallbackQuery):
    subjects: List[str] = collect_subjects(
        subject_type=callback.data,
        scoretable=states[callback.message.chat.id].scoretable,
        attribute_index=0
    )
    
    await callback.message.edit_text(
        text="Выбери предмет:",
        reply_markup=subject_chooser(subjects=subjects, subject_type=callback.data)
    )

@dispatcher.callback_query_handler(
    lambda callback:
        guards[callback.message.chat.id].text == Command.SCORE.value and any([
            Command.SCORE_ALL.value in callback.data,
            Command.SCORE_EXAMS.value in callback.data,
            Command.SCORE_COURSEWORKS.value in callback.data,
            Command.SCORE_TESTS.value in callback.data
        ])
)
@top_notification
async def show_subjects(callback: CallbackQuery):
    (subject_type, string_index) = callback.data.split()
    
    subjects: List[str] = collect_subjects(
        subject_type=subject_type,
        scoretable=states[callback.message.chat.id].scoretable,
        attribute_index=1
    )
    
    if string_index != "-":
        await callback.message.edit_text(
            text=subjects[int(string_index)],
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        await callback.message.delete()
        
        for score in subjects:
            await callback.message.answer(
                text=score,
                parse_mode=ParseMode.MARKDOWN
            )
        
        subjects_number: int = len(subjects)
        
        ending: str = "" if subjects_number == 1 else "а" if subjects_number in range(2, 5) else "ов"
        
        await callback.message.answer(
            text="*{subjects_number}* предмет{ending} всего!".format(subjects_number=subjects_number, ending=ending),
            parse_mode=ParseMode.MARKDOWN
        )
    
    guards[callback.message.chat.id].drop()
