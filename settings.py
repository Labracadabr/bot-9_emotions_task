# Кому юзер напишет в случае проблем. Встречается только в команде /help
mngr: str = '@its_dmitrii'

# список id админов. валидация приходит только первому по списку
# admins: list[str] = ["992863889"]   # Дима
admins: list[str] = ["899038082", "992863889"]   # Илья, Дима

# База данных со статусами заданий юзеров. тк я не умею в бд, то это просто json
baza_task = 'user_status.json'
baza_info = 'user_info.json'

# каналы сбора
referrals = ('smeight', 'gulnara', 'its_dmitrii', 'Natali', 'TD', 'Marina')

# # игнорить ли сообщения, присланные во время отключения бота
# ignor: bool = False

#
