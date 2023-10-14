import json
from aiogram.filters import BaseFilter
from aiogram.filters.state import State, StatesGroup
import os
from settings import baza_task, baza_info, tasks_tsv, logs
from lexic import lex
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, CallbackQuery, FSInputFile


# Запись данных item в указанный json file по ключу key
def log(file, key, item):
    with open(file, encoding='utf-8') as f:
        data = json.load(f)

    data.setdefault(str(key), []).append(item)

    with open(file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# айди из текста
def id_from_text(text):
    user_id = ''
    for word in text.split():
        if word.lower().startswith('id'):
            for symbol in word:
                if symbol.isnumeric():
                    user_id += symbol
            break
    return user_id


# найти первое доступное задание и выдать номер этого задания, напр file04
def find_next_task(user: str):
    # считать статусы заданий юзера
    with open(baza_task, 'r', encoding='utf-8') as f:
        data = json.load(f)
    tasks = data[user]
    for file_num in tasks:
        if tasks[file_num][0] in ('status', 'reject'):
            # задание найдено
            return file_num
    # если доступных заданий нет:
    return None


# на входе строка из тсв с заданиями, на выходе task_message
def get_task_message(next_task):
    task_name = next_task[1] + ' ' + next_task[3]
    link = next_task[2]
    instruct = next_task[4]
    task_message = f'<a href="{link}">{task_name}</a>\n{instruct}'
    return task_message


# Фильтр, проверяющий доступ юзера
class Access(BaseFilter):
    def __init__(self, access: list[str]) -> None:
        # В качестве параметра фильтр принимает список со строками
        self.access = access

    async def __call__(self, message: Message) -> bool:
        user_id_str = str(message.from_user.id)
        return user_id_str in self.access


# Состояния FSM
class FSM(StatesGroup):
    # Состояния, в которых будет находиться бот в разные моменты взаимодействия с юзером
    policy = State()            # Состояние ожидания соглашения с policy
    cancelation = State()       # Отмена отправки
    ready_for_next = State()    #
    done_a_task = State()       #
    all_accepted = State()      # Юзер всё скинул и ждет оплаты
    password = State()          # бот просит пароль
    delete = State()            # Админ стирает чью-то учетную запись
    age = State()               # Заполнение перс данных
    gender = State()            # Заполнение перс данных
    fio = State()               # Заполнение перс данных
    polling = State()               # тест для юзера


async def get_tsv(TKN, bot, msg, worker):
    #  чтение БД
    with open(baza_task, 'r') as f:
        data = json.load(f)

    urls = {}
    tasks = data[worker]
    for file_num in tasks:
        # добыть ссылку по file_id
        try:
            file_info = await bot.get_file(tasks[file_num][1])
            file_url = file_info.file_path
            url = f'https://api.telegram.org/file/bot{TKN}/{file_url}'
            print(file_num, url)
        except TelegramBadRequest:
            url = 'unavailable'
            print(file_num, 'file unavailable')

        urls.setdefault(file_num, url)

    folder = 'sent_files'
    if not os.path.exists(folder):
        os.makedirs(folder)
    path = f'{folder}/sent_{worker}.tsv'
    with open(path, 'w', encoding='UTF-8') as file:
        # tasks_dict = lex['tasks']
        #  создание слоавря {код задания: название}
        with open(tasks_tsv, 'r', encoding='UTF-8') as f:
            tasks_dict = {i.split('\t')[0]: i.split('\t')[3] for i in f.readlines()}
        print(tasks_dict)

        # первая строка таблицы
        row = ['create_time:', f'{str(msg.date.date())}', f'{msg.date.time()}']
        print('\t'.join(row), file=file)

        #  остальные строки
        for i, file_num in enumerate(tasks_dict):
            # print(tasks_dict[file_num])
            try:
                row = (file_num, tasks_dict[file_num], urls[file_num])
            except IndexError:
                break
            print('\t'.join(map(str, row)), file=file)
            # print(row)
    # вернуть путь к тсв
    return path


async def accept_user(worker):
    # проставить accept во всех файлах
    with open(baza_task, 'r', encoding='utf-8') as f:
        data = json.load(f)
    tasks = data[worker]

    # изменить статусы
    for file in tasks:
        tasks[file][0] = 'accept'
        print(tasks[file][0])

    # сохранить статусы заданий
    data.setdefault(worker, tasks)
    with open(baza_task, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


async def send_files(worker, status):
    #  логи
    log(logs, worker, f'{status} files requested')
    #  правильность ввода
    if status not in ('reject', 'accept', 'review'):
        print('wrong adm request')
        return

    # чтение бд
    with open(baza_task, 'r', encoding='utf-8') as f:
        data = json.load(f)
    tasks = data[worker]

    # чтение инстр заданий для подписи к файлам
    all_tasks_text = []
    with open(tasks_tsv, 'r', encoding='utf-8') as f:
        next_task = []
        for line in f.readlines():
            all_tasks_text.append(line.split('\t'))

    # Отправить файлЫ на проверку
    output = []
    for task in tasks:
        if tasks[task][0] == status:
            # Отправить каждый файл, у которого статус == review
            file_id = tasks[task][1]
            for tasks_text in all_tasks_text:
                if tasks_text[0] == task:
                    next_task = tasks_text
            task_message = get_task_message(next_task)
            # print(task_message)
            # text = lex['tasks'][task].split('\n')[0]
            print('adm', task)
            output.append((file_id, task_message,))

    return output
