dima = "992863889"
ilya = "899038082"
kris = "2137731767"

# Список id админов. Файлы приходит только первому по списку
admins: list[str] = [ilya, dima]

# Список id валидаторов. Можно вписать либо одного, либо двух - тогда одному будут идти четные, второму нечет
# Им приходят файлы и кнопки, доступны команды валидации
validators: list[str] = [kris]

# admins: list[str] = ["2137731767", "899038082", "992863889"]


# где хранятся данные. тк я не умею в бд, то это просто json
baza_task = 'user_status.json'
baza_info = 'user_info.json'
logs = 'logs.json'
tasks_tsv = 'tasks.tsv'

# каналы сбора
referrals = ('smeight', 'gulnara', 'its_dmitrii', 'Natali', 'TD', 'Marina', 'airplane', 'one_more')

# # игнорить ли сообщения, присланные во время отключения бота
# ignor: bool = False

#
