from bot import bot

from bot.shared.api.student import Student


def parse_creator_request(request: str) -> (str, str):
    request_words: [str] = request.split()
    
    if len(request_words) <= 1: return (None, None)
    
    option: str = request_words[1]  # The 0th index is for a command
    
    if ":" not in option: return (option, None)
    
    option_data = option.split(":")
    return (option_data[0], option_data[1])

async def update_progress_bar(loading_message, current_progress_bar: str, values: [Student], index: int) -> str:
    period: int = 20
    percent: int = int((index + 1)/len(values)*period)
    
    next_progress_bar: str = "`[ {plus}{minus} ]`".format(
        plus="".join([ "+" for _ in range(percent) ]),
        minus="".join([ "-" for _ in range(period - percent) ])
    )
    
    if current_progress_bar == next_progress_bar: return current_progress_bar
    
    await bot.edit_message_text(
        chat_id=loading_message.chat.id,
        message_id=loading_message.message_id,
        text=next_progress_bar
    )
    
    return next_progress_bar