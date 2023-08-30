from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from settings import admins, book, baza
from bot_logic import Access, log
from lexic import lex
import json

# Инициализация
router: Router = Router()


# Забанить юзера по telegram id. Пример сообщения: ban id123456789
@router.message(Access(admins), lambda msg: str(msg.text).lower().startswith('ban '))
async def banner(msg: Message):
    # вытащить id из текста сообщения
    ban_id = str(msg.text).split()[-1]
    if ban_id.lower().startswith('id'):
        ban_id = ban_id[2:]

    # ведение учета
    log('user_baza.json', 'ban', ban_id)
    book.setdefault('ban', []).append(ban_id)

    await msg.answer(text=f'id {ban_id} banned')


# admin нажал ✅
@router.callback_query(Access(admins), lambda x: x.data == 'admin_ok')
async def admin_ok(callback: CallbackQuery, bot:Bot):
    msg = callback.message

    # вытащить id из текста сообщения
    worker = ''
    for i in str(msg.text).split():
        if i.lower().startswith('id'):
            worker = i[2:-1]
            break

    # проставить accept во всех файлах
    with open(baza, 'r') as f:
        data = json.load(f)
    tasks = data[worker]
    for file in tasks:
        tasks[file][0] = 'accept'

    # убрать кнопки админа
    await bot.edit_message_text(f'{msg.text}\n✅ Принято', msg.chat.id, msg.message_id, reply_markup=None)
    # Дать юзеру аппрув
    await bot.send_message(chat_id=worker, text=lex['all_approved']+f'\nid{worker}')


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
    for line in verdict:
        rejected_files.append(line.split()[0])

    # проставить reject в нужных файлах
    with open(baza, 'r') as f:
        data = json.load(f)
    tasks = data[worker]
    for file in rejected_files:
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
    await bot.send_message(chat_id=worker, text=f'Your file has been rejected. Reason:\n\n<i>{verdict}</i>',
                           parse_mode='HTML')



