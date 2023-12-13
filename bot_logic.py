import json
from pprint import pprint

from aiogram.filters import BaseFilter
from aiogram.filters.state import State, StatesGroup
import os
from settings import *
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram import Bot
from config import Config, load_config
from datetime import datetime


# Инициализация
config: Config = load_config()
TKN: str = config.tg_bot.token
bot_func: Bot = Bot(TKN)


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
    all_accepted = State()      # все принято юзер, ждет оплаты
    password = State()          # бот просит пароль
    delete = State()            # Админ стирает чью-то учетную запись
    age = State()               # Заполнение перс данных
    gender = State()            # Заполнение перс данных
    fio = State()               # Заполнение перс данных
    country = State()           # Заполнение перс данных
    race = State()              # Заполнение перс данных
    polling = State()           # тест для юзера


# выбор языка. на входе языковой код (по дефолту en), на выходе словарь с лексикой этого языка
def load_lexicon(language: str = 'en') -> dict:
    if language not in langs:
        language = 'en'
    try:
        lexicon_module = __import__(f'lexic.{language}', fromlist=[''])
        return lexicon_module.lexicon
    except ImportError:
        return None


# Запись данных item в указанный csv file по ключу key
async def log(file, key, item):
    key = str(key)
    t = str(datetime.now()).split('.')[0]
    # сохранить в csv
    try:
        with open(file, 'a', encoding='utf-8') as f:
            print('\t'.join((t, str(key), repr(item))), file=f)
        # with open(file, encoding='utf-8') as f:  # старая версия с json
        #     data = json.load(f)
        # data.setdefault(str(key), []).append(item)
        # with open(file, 'w', encoding='utf-8') as f:
        #     json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        item += f'\n🔴Ошибка записи:\n{e}'

    # дублировать логи в консоль
    log_text = str(key)+' '+str(item)
    print(t.split()[-1], log_text)
    # дублировать логи в тг-канал
    if item != '/next':
        try:
            await bot_func.send_message(chat_id=log_channel_id, text=log_text) if log_channel_id else None
        except Exception as e:
            print('channel error', e)


# дать статус заданий по айди юзера
async def get_status(user_id) -> dict:
    with open(baza_task, 'r') as f:
        data = json.load(f)
    non = rev = rej = acc = 0
    try:
        info = data[user_id]
        for task in info:
            # print(task)
            if info[task][0] == 'status':
                non += 1
            elif info[task][0] == 'review':
                rev += 1
            elif info[task][0] == 'reject':
                rej += 1
            elif info[task][0] == 'accept':
                acc += 1
    except KeyError:
        non = total_tasks
    output = {
        'non': non,
        'rev': rev,
        'rej': rej,
        'acc': acc,
    }
    # return f'✅ Принято - {acc}\n🔁 Надо переделать - {rej}\n⏳ На проверке - {rev}\n💪 Осталось сделать - {non}'
    return output


# айди из текста
def id_from_text(text: str) -> str:
    user_id = ''
    for word in text.split():
        if word.lower().startswith('id'):
            for symbol in word:
                if symbol.isnumeric():
                    user_id += symbol
            break
    return user_id


# создать учетную запись заданий
def create_account(task_amount: int) -> dict:
    # пример = {"file01": ['status', 'file'], }
    account = {f'file{num:0>2}': ['status', 'file'] for num in range(1, task_amount+1)}
    return account


# найти первое доступное задание и выдать номер этого задания, напр file04
def find_next_task(user: str):
    # считать статусы заданий юзера
    with open(baza_task, 'r', encoding='utf-8') as f:
        data = json.load(f)
    try:
        tasks = data[user]
    except KeyError:
        return None
    for file_num in tasks:
        if tasks[file_num][0] in ('status', 'reject'):
            # задание найдено
            return file_num
    # если доступных заданий нет:
    return None


# на входе строка из тсв с заданиями, на выходе task_message
def get_task_message(next_task) -> str:
    task_name = next_task[1] + '\n' + next_task[3]
    link = next_task[2]
    instruct = next_task[4].replace('*', ' \n')
    if link:
        task_message = f'<a href="{link}">{task_name}</a>\n{instruct}'
    else:
        task_message = f'{task_name}\n{instruct}'
    return task_message


# отправить json
async def send_json(user: str, file: str):
    files = {
        'bd': baza_task,
        'info': baza_info,
        'logs': logs,
    }
    output = list(files.values()) if file == 'all' else [files[file]]
    for i in output:
        await bot_func.send_document(chat_id=user, document=FSInputFile(path=i))
    await log(logs, user, f'adm file request: {file}')


# создать tsv с названиями файлов и ссылками на их скачивания, return путь к файлу
async def get_tsv(TKN, bot, msg, worker) -> str:
    #  чтение БД
    with open(baza_task, 'r') as f:
        data = json.load(f)

    urls = {}
    tasks = data[worker]
    for file_num in tasks:
        # добыть ссылку по file_id
        try:
            file_id = tasks[file_num][1]
            file_info = await bot.get_file(file_id)
            file_url = file_info.file_path
            url = f'https://api.telegram.org/file/bot{TKN}/{file_url}'
            print(file_num, url)
        except TelegramBadRequest:
            url = 'unavailable'
            print(file_num, 'file unavailable')

        urls.setdefault(file_num, url)

    path = f'sent_{worker}.tsv'
    with open(path, 'w', encoding='UTF-8') as file:
        # tasks_dict = lex['tasks']
        #  создание словаря {код задания: название}
        with open(tasks_tsv.format('ru'), 'r', encoding='UTF-8') as f:
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
                print('\t'.join(map(str, row)), file=file)
                # print(row)
            except IndexError or KeyError:
                break
    # вернуть путь к тсв
    return path


# проставить accept во всех файлах
async def accept_user(worker) -> None:
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

    # with open(baza_task, 'r', encoding='utf-8') as f:
    #     info = json.load(f)
    #
    # info['accept_date'] = msg_time
    #
    # # сохранить новые данные
    # info.setdefault(worker, info)
    # with open(baza_info, 'w', encoding='utf-8') as f:
    #     json.dump(info, f, indent=2, ensure_ascii=False)


# отправить в чат файлы юзера в указанном статусе
async def send_files(worker, status) -> list | None:
    #  логи
    await log(logs, worker, f'{status} files requested')
    #  правильность ввода
    if status not in ('reject', 'accept', 'review'):
        print('wrong adm request')
        return

    # чтение бд
    with open(baza_task, 'r', encoding='utf-8') as f:
        data = json.load(f)
    tasks = data[worker]

    # язык будет тот же, что у исполнителя
    language = await get_pers_info(user=worker, key='lang')
    if language not in langs:
        language = 'en'

    # чтение инстр заданий для подписи к файлам
    all_tasks_text = []
    with open(tasks_tsv.format(language), 'r', encoding='utf-8') as f:
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


# получить значение
async def get_pers_info(user: str, key: str):
    with open(baza_info, 'r', encoding='utf-8') as f:
        data: dict = json.load(f)
    user_data: dict = data.get(user)
    if not user_data:
        await log(logs, user, f'user not found')
        return None
    value = user_data.get(key)
    return value


# задать значение
async def set_pers_info(user: str, key: str, val):
    # прочитать бд
    with open(baza_info, 'r', encoding='utf-8') as f:
        data: dict = json.load(f)
    user_data: dict = data.get(user)
    if not user_data:
        await log(logs, user, f'user not found')
        return None
    old_val = user_data.get(key)

    # сохр изменение
    user_data[key] = val
    data.setdefault(user, user_data)
    with open(baza_info, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(user, f'{key}: {old_val} => {val}')
    # await log(logs, user, f'{key}: {old_val} => {val}')
