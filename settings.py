import os

# список языков
langs = ('ru', 'en')

# tg id работников
dima = "992863889"
ilya = "899038082"
kris = "2137731767"
liza = '677214436'
anya = '639770334'
kate = '1110667509'
sasha = '5488256829'

# Список id админов. Файлы приходят автоматически только первому по списку
# admins: list[str] = [anya]
admins: list[str] = [dima]

# Список id валидаторов. Можно вписать либо ничего, либо одного, либо двух - тогда одному будут идти четные, второму нечет
# Им приходят файлы и кнопки, доступны команды валидации
validators: list[str] = []

# сколько в боте заданий
total_tasks: int = 15

# где хранятся данные. тк я не умею в sql, то это просто json
baza_task = 'user_status.json'
baza_info = 'user_info.json'
logs = 'logs.tsv'
tasks_tsv = 'lexic/tasks_{}.tsv'

# каналы сбора
referrals = ('smeight', 'gulnara', 'its_dmitrii', 'Natali', 'TD', 'Marina', 'schura', 'hanna', 'toloka', 'cat', 'airplane', 'one_more', 'good')
# https://t.me/PhotoTasksBot?start={}...

# tg канал для логов
# log_channel_id = ''
log_channel_id = '-1002105757977'

# проверочный код
verification = 'B54U83'


# проверить все ли на месте
def check_files():
    file_list = [baza_task, baza_info, logs]+[tasks_tsv.format(i) for i in langs]
    for file in file_list:
        if not os.path.isfile(file):
            if file.endswith('json'):
                with open(file, 'w', encoding='utf-8') as f:
                    print('Отсутствующий файл создан:', file)
                    print('{}', file=f)
            elif file.endswith('sv'):
                with open(file, 'w', encoding='utf-8') as f:
                    print('Отсутствующий файл создан:', file)
                    print('\t'.join(('Time', 'User', 'Action')), file=f)

            elif 'tasks' in file:
                print("Ошибка! Отсутствует файл с заданиями", file)
                exit()

    # with open(tasks_tsv, 'r', encoding='utf-8') as f:
    #     task_list = f.readlines()
    #     if not len(task_list) == total_tasks:
    #         print('Ошибка! Не совпадает число заданий')
    #         exit()
    print('OK')


check_files()
