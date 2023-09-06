# Кому юзер напишет в случае проблем. Встречается только в команде /help
mngr: str = '@its_dmitrii'

# список id админов. валидация приходит только первому по списку
# admins: list[str] = ["992863889"]   # Дима
admins: list[str] = ["2137731767", "899038082", "992863889"]   # Кристина, Илья, Дима
# 2137731767 Лаврук Кристина

# База данных со статусами заданий юзеров. тк я не умею в бд, то это просто json
baza_task = 'user_status.json'
baza_info = 'user_info.json'
logs = 'logs.json'

# каналы сбора
referrals = ('smeight', 'gulnara', 'its_dmitrii', 'Natali', 'TD', 'Marina', 'airplane', 'one_more')

# # игнорить ли сообщения, присланные во время отключения бота
# ignor: bool = False

#
