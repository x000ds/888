from vkwave.bots import SimpleBotEvent
from vkwave.bots import PayloadContainsFilter

from bot.platforms.vk import vk_bot
from bot.platforms.vk import guards

from bot.platforms.vk.commands.schedule.utilities.keyboards import time_period_chooser
from bot.platforms.vk.commands.schedule.utilities.classes import common_show_chosen_date

from bot.utilities.types import Command
from bot.utilities.api.types import ScheduleType


@vk_bot.message_handler(
    lambda event: guards[event.object.object.message.peer_id].text == Command.LECTURERS.value,
    PayloadContainsFilter(key=ScheduleType.CLASSES.value)
)
async def lecturer_menu(event: SimpleBotEvent):
    lecturer_id: str = event.payload["lecturer_id"]

    await event.answer(
        message="Можешь выбрать нужный день, либо весь семестр целиком:",
        keyboard=time_period_chooser(lecturer_id=lecturer_id)
    )

@vk_bot.message_handler(PayloadContainsFilter(key=Command.LECTURERS_CLASSES_SHOW.value))
async def lecturer_show_chosen_date(event: SimpleBotEvent):
    await common_show_chosen_date(command=Command.LECTURERS, event=event)
