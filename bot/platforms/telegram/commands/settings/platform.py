from aiogram.types import CallbackQuery
from aiogram.types import ParseMode

from bot.platforms.telegram import dispatcher
from bot.platforms.telegram import guards

from bot.platforms.telegram.utilities.helpers import top_notification

from bot.models.user import User

from bot.utilities.constants import PLATFORM_CODE_INFO
from bot.utilities.helpers import generate_platform_code
from bot.utilities.types import Command


@dispatcher.callback_query_handler(
    lambda callback:
        guards[callback.message.chat.id].text == Command.SETTINGS.value and
        callback.data == Command.SETTINGS_PLATFORM_CODE.value
)
@top_notification
async def appearance_done(callback: CallbackQuery):
    user_id: int = User.get(User.telegram_id == callback.message.chat.id).user_id
    platform_code: str = generate_platform_code(user_id=user_id)
    
    await callback.message.edit_text(
        text=PLATFORM_CODE_INFO.format(platform_code=platform_code),
        parse_mode=ParseMode.MARKDOWN
    )
    
    guards[callback.message.chat.id].drop()
