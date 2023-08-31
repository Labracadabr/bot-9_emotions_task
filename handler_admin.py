from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from settings import admins, baza
from bot_logic import Access, log
from lexic import lex
import json
import os
from config import Config, load_config
# import pygsheets
# import googleapiclient.errors
import time


# Инициализация
router: Router = Router()
config: Config = load_config()
TKN: str = config.tg_bot.token


# Забанить юзера по telegram id. Пример сообщения: ban id123456789
@router.message(Access(admins), lambda msg: str(msg.text).lower().startswith('ban '))
async def banner(msg: Message):
    # вытащить id из текста сообщения
    ban_id = str(msg.text).split()[-1]
    if ban_id.lower().startswith('id'):
        ban_id = ban_id[2:]

    log('user_baza.json', 'ban', ban_id)
    await msg.answer(text=f'id {ban_id} banned')


# admin нажал ✅
@router.callback_query(Access(admins), lambda x: x.data == 'admin_ok')
async def admin_ok(callback: CallbackQuery, bot:Bot):
    msg = callback.message

    # вытащить id из текста сообщения
    worker: str = ''
    for i in str(msg.text).split():
        if i.lower().startswith('id'):
            worker = i[2:-1]
            break

    # проставить accept во всех файлах и записать ссылки для скачивания
    with open(baza, 'r') as f:
        data = json.load(f)
    urls = []
    tasks = data[worker]
    for file in tasks:
        tasks[file][0] = 'accept'
        print(tasks[file][0])

        # добыть ссылку по file_id
        file_info = await bot.get_file(tasks[file][1])
        file_url = file_info.file_path
        url = f'https://api.telegram.org/file/bot{TKN}/{file_url}'
        urls.append(url)

    # сохранить статусы заданий
    data.setdefault(worker, tasks)
    with open(baza, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # убрать кнопки админа
    await bot.edit_message_text(f'{msg.text}\n✅ Принято', msg.chat.id, msg.message_id, reply_markup=None)
    # Дать юзеру аппрув
    await bot.send_message(chat_id=worker, text=lex['all_approved']+f'id{worker}')

    # # сохранить ссылки
    # gc = pygsheets.authorize(service_file='token.json')
    # sheet_url = 'https://docs.google.com/spreadsheets/d/1dlZdboea3OAzNpivRxgDiQ6SaW14RjHdfFD-77HwGiQ/edit#gid=0'
    # spreadsheet = gc.open_by_url(sheet_url)
    # try:
    #     spreadsheet.add_worksheet(title=worker)
    # except googleapiclient.errors.HttpError:
    #     pass

    # сохранить ссылки в g_sheet, в отдельный tsv и print в консоль
    folder = 'accepted_files'
    if not os.path.exists(folder):
        os.makedirs(folder)
    path = f'{folder}/accepted_{worker}.tsv'
    with open(path, 'w', encoding='UTF-8') as file:
        tasks_dict = lex['tasks']

        # первая строка таблицы
        row = ['accept_time:', f'{str(msg.date.date())}', f'{msg.date.time()}']
        print('\t'.join(row), file=file)
        # spreadsheet.worksheet_by_title(title=worker).append_table(values=row)

        #  остальные строки
        for i, file_num in enumerate(tasks_dict):
            try:
                row = [file_num, tasks_dict[file_num].split()[3], urls[i]]
            except IndexError:
                break
            print('\t'.join(tuple(map(str, row))), file=file)
            print(row)
            # spreadsheet.worksheet_by_title(worker).append_table(values=row)

    # отправить tsv админу
    await bot.send_document(chat_id=admins[0], document=FSInputFile(path=path))


# admin нажал ❌
@router.callback_query(Access(admins), lambda x: x.data == 'admin_no')
async def admin_no(callback: CallbackQuery, bot: Bot):
    msg = callback.message

    # обновить сообщение у админа и убрать кнопки
    await bot.edit_message_text(f'{msg.text}\n\n❌ Отклонено. Напиши причину отказа '
                                f'для каждого файла <b>одним ответом на это сообщение</b>!\n\n'
                                f'Укажи номер задания и через пробел причину. Следующее задание '
                                f'- перенос строки. Например:\n'
                                f'\n<i>05 плохое качество'
                                f'\n51 обрезано лицо</i>',
                                msg.chat.id, msg.message_id, parse_mode='HTML', reply_markup=None)


# Причина отказа
@router.message(Access(admins), lambda msg: msg.reply_to_message)
async def reply_decline_reason(msg: Message, bot: Bot):
    # причина отказа
    verdict = str(msg.text)
    # сообщение, на которое отвечаем
    orig = msg.reply_to_message

    # worker = вытащить id из текста сообщения
    txt = str(msg.reply_to_message.text).split()
    for i in txt:
        if i.lower().startswith('id'):
            worker = i[2:-1]
            break

    # записать номера отклоненных файлов
    rejected_files = []
    txt_for_worker = '\n\n'
    for line in verdict.split('\n'):
        print(line)
        rejected_files.append(line.split()[0])
        txt_for_worker += 'Задание '+line+'\n'

    # проставить reject в нужных файлах
    with open(baza, 'r') as f:
        data = json.load(f)
    tasks = data[worker]
    for file in rejected_files:
        print(file)
        tasks[f'file{file}'][0] = 'reject'

    # проставить accept в остальных файлах
    for file in tasks:
        if tasks[file][0] == 'review':
            tasks[file][0] = 'accept'

    # сохранить статусы заданий
    data.setdefault(worker, tasks)
    with open(baza, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # обновить сообщение у админа и дописать причину отказа
    await bot.edit_message_text(f'❌ Отклонено. Причина:\n{verdict}', orig.chat.id, orig.message_id,
                                reply_markup=None)
    # сообщить юзеру об отказе
    msg_to_pin = await bot.send_message(chat_id=worker, text=lex['reject']+f'<i>{txt_for_worker}</i>', parse_mode='HTML')
    await bot.pin_chat_message(message_id=msg_to_pin.message_id, chat_id=worker, disable_notification=True)




