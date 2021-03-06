from typing import Optional

from random import choice

from vkwave.bots import SimpleBotEvent

from bot.platforms.vk import states
from bot.platforms.vk import guards

from bot.platforms.vk.commands.schedule.utilities.keyboards import dates_scroller
from bot.platforms.vk.utilities.keyboards import to_menu

from bot.models.user import User

from bot.utilities.helpers import remove_markdown
from bot.utilities.types import Command
from bot.utilities.api.constants import LOADING_REPLIES
from bot.utilities.api.types import ResponseError
from bot.utilities.api.types import ScheduleType
from bot.utilities.api.student import get_schedule_by_group_schedule_id
from bot.utilities.api.lecturers import get_lecturers_schedule


async def common_show_chosen_date(command: Command, event: SimpleBotEvent):
    await event.answer(
        message=choice(LOADING_REPLIES),
        dont_parse_links=True
    )
    
    date_string: Optional[str] = event.payload.get("date_string")
    lecturer_id: str = event.payload["lecturer_id"]

    user: User = User.get(User.vk_id == event.peer_id)
    
    if command is Command.CLASSES:
        (schedule, response_error) = get_schedule_by_group_schedule_id(
            schedule_type=ScheduleType.CLASSES,
            user=user,
            another_group_schedule_id=states[event.peer_id].another_group_schedule_id,
            dates=[ date_string ] if date_string is not None else []
        )
    elif command is Command.LECTURERS:
        (schedule, response_error) = get_lecturers_schedule(
            lecturer_id=lecturer_id,
            schedule_type=ScheduleType.CLASSES,
            user=user,
            dates=[ date_string ] if date_string is not None else []
        )
    else:
        (schedule, response_error) = (None, ResponseError.INCORRECT_SCHEDULE_TYPE)
    
    if response_error is not None:
        await event.answer(
            message=response_error.value,
            dont_parse_links=True,
            keyboard=to_menu()
        )
    
    if schedule is not None:
        for day in schedule:
            await event.answer(
                message=remove_markdown(day),
                keyboard=dates_scroller(shown_date_string=date_string, lecturer_id=lecturer_id) if date_string is not None else to_menu()
            )

    states[event.peer_id].drop()
