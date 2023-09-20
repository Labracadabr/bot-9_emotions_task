dima = "992863889"
ilya = "899038082"
kris = "2137731767"
liza = '677214436'

# Список id админов. Файлы приходят только первому по списку
admins: list[str] = [ilya, dima]

# Список id валидаторов. Можно вписать либо ноль, либо одного, либо двух - тогда одному будут идти четные, второму нечет
# Им приходят файлы и кнопки, доступны команды валидации
validators: list[str] = [liza]


# где хранятся данные. тк я не умею в бд, то это просто json
baza_task = 'user_status.json'
baza_info = 'user_info.json'
logs = 'logs.json'
tasks_tsv = 'tasks.tsv'

# каналы сбора
referrals = ('smeight', 'gulnara', 'its_dmitrii', 'Natali', 'TD', 'Marina', 'schura', 'cat', 'airplane', 'one_more')
# https://t.me/TdTasksBot?start=...

# # игнорить ли сообщения, присланные во время отключения бота
# ignor: bool = False

#
