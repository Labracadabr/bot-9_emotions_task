import json

# Кому юзер напишет в случае проблем. Встречается только в команде /help
mngr: str = '@its_dmitrii'

# список id админов
admins: list[str] = ["992863889"]

# Куда сохранятся файлы из ответов. Заранее создать папку
SAVE_DIR: str = r"C:\Users\PC\PycharmProjects\bot-6_data_collector\OUTPUT\W2"
# SAVE_DIR: str = r"C:\Users\PC\PycharmProjects\bot-6_data_collector\OUTPUT\SELFIE"

# статусы юзеров. тк я не умею в sql, то это просто json
baza = 'user_baza.json'
with open(baza, encoding='utf-8') as f:
    book: dict[str, list[str]] = json.load(f)

# # игнорить ли сообщения, присланные во время отключения бота
# ignor: bool = False
