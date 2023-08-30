import time
import json
import requests
import os
from aiogram import Router, Bot, F, types
from aiogram.filters import Command, StateFilter, or_f
# from aiogram.types import Message, CallbackQuery
from bot_logic import log, Access, FSM # dwnld_photo_or_doc
from config import Config, load_config
from keyboards import keyboard_admin, keyboard_user, keyboard_ok, keyboard_privacy
from settings import admins, book, project, auto_approve, verification_code, platform_id_example
from lexic import lex
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import CallbackQuery, Message


# Инициализация всяких ботских штук
router: Router = Router()
config: Config = load_config()
TKN: str = config.tg_bot.token
storage: MemoryStorage = MemoryStorage()
user_files: [str, str] = {}

baza = 'user_baza.json'


# команда /help
@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    log('logs.json', message.from_user.id, '/help')
    await message.answer(lex['help'])


# # чекнуть не в бане ли юзер
# @router.message(Access(book['ban']))
# async def no_access(message: Message):
#     await message.answer(lex['ban'])


# команда /start
@router.message(Command(commands=['start']))
async def process_start_command(message: Message, bot: Bot, state: FSMContext):
    worker = message.from_user
    msg_time = message.date.strftime("%d/%m/%Y %H:%M")
    # print(message.json(indent=4, exclude_none=True))

    # логи
    log('logs.json', 'logs',
        f'{msg_time}, {worker.full_name}, @{worker.username}, id {worker.id}, {worker.language_code}')
    log('logs.json', worker.id, '/start')

    # бот переходит в состояние ожидания согласие с политикой
    await state.set_state(FSM.policy)

    # приветствие и выдача политики
    await message.answer(text=lex['start'])
    await message.answer(text='I read and agree', reply_markup=keyboard_ok)

    # сообщить админу, кто нажал старт
    if str(worker.id) not in admins:
        for i in admins:
            await bot.send_message(text=f'Bot started by id{worker.id} {worker.full_name} @{worker.username}',
                                   chat_id=i, disable_notification=True)


# команда /next
@router.message(Command(commands=['next']))
async def process_help_command(message: Message, bot: Bot, state: FSMContext):
    user = str(message.from_user.id)

    log('logs.json', user, '/next')

    with open(baza, 'r') as f:
        data = json.load(f)

    tasks = data[user]
    for i in tasks[0]:
        print(tasks[0][i])
        if tasks[0][i][0] == 'status':
            await bot.send_message(chat_id=user, text=lex['tasks'][i], parse_mode='HTML')
            print(111)
            break
    # бот переходит в состояние ожидания след файла
    await state.set_state(FSM.ready_for_next)


# команда /status
@router.message(Command(commands=['status']))
async def process_help_command(message: Message):
    log('logs.json', message.from_user.id, '/help')
    await message.answer(lex['help'])


# согласен с политикой ✅
@router.callback_query(lambda x: x.data == "ok_pressed", StateFilter(FSM.policy))
async def privacy_ok(callback: CallbackQuery, bot: Bot, state: FSMContext):
    worker = callback.from_user

    # логи
    log('logs.json', worker.id, 'privacy_ok')

    # выдать инструкцию и примеры
    await bot.send_message(text=lex['instruct1'], chat_id=worker.id, parse_mode='HTML')
    # await bot.send_photo(photo=lex['example_link'], caption='Examples', chat_id=worker.id)
    # await bot.send_media_group(media=json.loads(lex['example_json']), chat_id=worker.id)
    time.sleep(2)

    await bot.send_message(text=f"{lex['instruct2']}\n\n{lex['full_hd']}", chat_id=worker.id, parse_mode='HTML')

#
# # если юзер пишет что-то не нажав ✅
# @router.message(StateFilter(FSM.policy))
# async def privacy_missing(msg: Message):
#     log('logs.json', msg.from_user.id, 'privacy_missing')
#     await msg.answer(text=lex['privacy_missing'])


# юзер отправил альбом: не принимается
@router.message(lambda msg: msg.media_group_id)
async def alb(msg: Message):
    worker = msg.from_user
    log('logs.json', worker.id, 'album')
    await msg.reply(lex['album'])


# юзер отправил сжатый файл: не принимается
@router.message(F.content_type.in_({'photo', 'video'}))
async def compressed_pic(msg: Message):
    log('logs.json', msg.from_user.id, '/file')
    await msg.reply(lex['full_hd'], parse_mode='HTML')


# юзер отправил норм файл
@router.message(F.content_type.in_({'document'}))
async def photo1(msg: Message, bot: Bot, state: FSMContext):
    user = str(msg.from_user.id)

    with open(baza, 'r') as f:
        data = json.load(f)

    # вычисляем, какое было прислано задание
    sent_file = ''
    tasks = data[user]
    for i in tasks[0]:
        print(tasks[0][i])
        if tasks[0][i][0] in ('status', 'reject'):
            sent_file = i
            log('logs.json', user, f'SENT_{sent_file}')
            break

    # сохраняем ссылку на файл
    file_id = msg.document.file_id
    file_info = await bot.get_file(file_id)
    file_url = file_info.file_path
    tg_file_link = f'https://api.telegram.org/file/bot{TKN}/{file_url}'

    # меняем статус задания
    data[user][0][sent_file] = ('review', tg_file_link)

    with open(baza, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # если остались еще задания
    if sent_file != "file65":
        # Бот ожидает нажатия /next
        await state.set_state(FSM.done_a_task)
        await msg.reply(f'Принят файл {sent_file}.\nНажмите /next для следующего задания', reply_markup=keyboard_user)

    # если был отправлен последний файл
    if sent_file == "file65":
        log('logs.json', user, 'SENT_ALL_FILES')
        await msg.reply(lex['all_sent'])
        # await state.set_state(FSM.waiting_verif)

        # Отправить файлЫ админу на проверку
        for task in data[user][0] :
            if task[0] == 'review':
                # Отправить каждый файл, у которого статус - review
                await bot.send_photo(chat_id=admins[0], photo=task[1], caption=f'{task} id{user}')
        # сообщения с кнопками (принять или нет)
        await bot.send_message(chat_id=admins[0], text=f'Принять файлы от id{user}?', reply_markup=keyboard_admin)

#
#     # логи
#     # if str(worker.id) not in admins:
#     log('logs.json', worker.id, 'SENT_FILE_2')
#     log('user_baza.json', lex['log'], str(worker.id))
#     book.setdefault(lex['log'], []).append(str(worker.id))
#
#     print(worker.full_name, 'sent all files')
#     print()

