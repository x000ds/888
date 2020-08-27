from bot.shared.constants import BOT_ADDRESSING


BRS: str = (
    "*БРС*\n"
    "_балльно-рейтинговая система_\n\n"
    
    "Обычно можно получить *50* баллов за семестр и столько же за экзамен. *100* баллов всего.\n\n"
    
    "• 3ка - от *51* до *70*\n"
    "• 4ка - от *71* до *85*\n"
    "• 5ка - от *86* до *100*\n\n"
    
    "Для зачёта достаточно получить *51* балл в сумме.\n\n"
    
    "_варьируется от преподавателя к преподавателю_"
)

HELP: str = (
    "*~$ kbot --help*\n"
    
    "\n*classes & exams*\n"
    "• Для того, чтобы узнать расписание занятий другой группы, введи /classes *[ группа ]*\n"
    "• То же работает с /exams\n"
    
    "\n*notes*\n"
    "• При добавлении новой заметки можно выделить текст \**жирным*\* или \__курсивом_\_, обособив его звёздочками или нижним подчёркиванием.\n"
    
    "\n*settings*\n"
    "• Расписание может отображаться в полном и компактном форматах. В первом режиме доступны время-место, название и тип пары, а также имя преподавателя и кафедра предмета. Во втором — имени преподавателя и кафедры предмета нет, а тип предмета укорочен: *Л* — лекция, *П* — практика, *ЛР* — лабораторная работа, *К* — консультация.\n"
    "• Некоторые пары проводятся только в определённые недели или даты. Такие пары бот отображает только для того дня, когда пара будет. Для того, чтобы отображать эти занятия всегда, нужно переключить пункт *пары по датам* на *все пары*.\n"
    
    "\n*групповые чаты*\n"
    "• Бота можно добавить в групповой чат. Необходимо сделать его админом и не запрещать ему удалять сообщения.\n"
    "• Текстовые сообщения должны начинаться с обращения {bot_addressing} либо быть реплаями, команды — не должны:\n"
    "• /command\n"
    "• {bot_addressing} текст\n"
    "• текст (в случае, если реплай)\n"
    
    "\n*другое*\n"
    "• Внутри бота реализована GUARD-система, не позволяющая захламлять чат. Для того, чтобы второй запрос стал доступен, необходимо завершить или отменить первый.\n"
    "• Бот имеет свой репозиторий на GitHub, добро пожаловать: github.com/airatk/kaishnik-bot\n"
    
    "\n_Бот был написан студентом во время учёбы на 1 курсе с применением исключительно самостоятельно полученных знаний, без какого-либо доступа к каким-либо API сайтов КАИ._\n"
    
    "\nХотелки, жалобы, любые интересующие вопросы — разработчику: @airatk"
).format(bot_addressing=BOT_ADDRESSING[:-1])

DONATE: str = (
    "Если тебе понравился бот, ты можешь добровольно отблагодарить разработчика денежным донатом:\n\n"
    
    "• *Сбербанк*: 2202 2012 3023 9101\n"
    "• *Paypal*: paypal.me/kamairat\n\n"
    
    "Либо стать Патроном и получить стикеры или толстовку в подарок:\n\n"
    
    "• *Patreon*: patreon.com/airatk\n\n"
    
    "Спасибо, что пользуешься ботом! :)"
)

DICE: str = "🏀"
