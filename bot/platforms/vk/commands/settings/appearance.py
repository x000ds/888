from vkwave.bots import SimpleBotEvent
from vkwave.bots import PayloadFilter
from vkwave.bots import PayloadContainsFilter

from bot.platforms.vk import vk_bot

from bot.platforms.vk.commands.settings.utilities.keyboards import appearance_chooser
from bot.platforms.vk.utilities.keyboards import to_menu

from bot.models.user import User
from bot.models.settings import Settings

from bot.utilities.types import Command
from bot.utilities.types import SettingsOption


@vk_bot.message_handler(
    PayloadFilter(payload={ "callback": Command.SETTINGS_APPEARANCE.value }) |
    PayloadContainsFilter(key=Command.SETTINGS_APPEARANCE.value)
)
async def appearance(event: SimpleBotEvent):
    user: User = User.get(User.vk_id == event.peer_id)
    settings: Settings = Settings.get(Settings.user == user)
    
    if event.payload.get(Command.SETTINGS_APPEARANCE.value) == SettingsOption.IS_SCHEDULE_SIZE_FULL.value:
        settings.is_schedule_size_full = not settings.is_schedule_size_full
    
    settings.save()
    
    await event.answer(
        message=(
            "Показаны текущие настройки.\n"
            "Нажми на нужную опцию, чтобы изменить её:"
        ),
        keyboard=appearance_chooser(settings=settings)
    )

@vk_bot.message_handler(PayloadFilter(payload={ "callback": Command.SETTINGS_APPEARANCE_DROP.value }))
async def appearance_drop(event: SimpleBotEvent):
    user: User = User.get(User.vk_id == event.peer_id)
    
    Settings.delete().where(Settings.user == user).execute()
    Settings.insert(user=user).execute()
    
    await appearance_done(event=event)

@vk_bot.message_handler(PayloadFilter(payload={ "callback": Command.SETTINGS_APPEARANCE_DONE.value }))
async def appearance_done(event: SimpleBotEvent):
    await event.answer(
        message="Сохранено!",
        keyboard=to_menu()
    )
