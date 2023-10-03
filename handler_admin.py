from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from settings import admins, baza_task, baza_info, logs, validators
from bot_logic import Access, log, id_from_text, FSM, get_tsv, accept_user, send_files
from lexic import lex
import json
import os
from config import Config, load_config
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest

# import pygsheets
# import googleapiclient.errors


# Инициализация
router: Router = Router()
config: Config = load_config()
TKN: str = config.tg_bot.token


# # Забанить юзера по telegram id. Пример сообщения: ban id123456789
# @router.message(Access(admins), lambda msg: str(msg.text).lower().startswith('ban '))
# async def banner(msg: Message):
#     # вытащить id из текста сообщения
#     ban_id = str(msg.text).split()[-1]
#     if ban_id.lower().startswith('id'):
#         ban_id = ban_id[2:]
#
#     log('user_status.json', 'ban', ban_id)
#     await msg.answer(text=f'id {ban_id} banned')


# reject fix
@router.message(Access(["992863889"]), lambda msg: msg.text.startswith('❌ Отклонено'))
async def reject_fix(msg: Message, bot: Bot):
    user = str(msg.from_user.id)
    print('adm reject fix')

    # worker = вытащить id из текста сообщения
    worker = id_from_text(msg.text)
    txt_for_worker = '\n\n'
    # ответ админа
    admin_response = msg.text.split('\n')[3:]
    admin_response = '\n'.join(admin_response)

    # записать номера отклоненных файлов
    rejected_files = []
    correct_format = True
    for line in admin_response.split('\n'):
        print(line)
        file_num = line.split()[0]
        # убедиться, что каждая строка начинается с номера задания
        if not file_num.isnumeric():
            correct_format = False
            await bot.send_message(msg.chat.id, lex['wrong_rej_form'])
            print(admin_response.split('\n'))
            break
        rejected_files.append(line.split()[0])
        txt_for_worker += line+'\n'

    if correct_format:
        # прочитать данные юзера из пд
        with open(baza_info, 'r', encoding='utf-8') as f:
            data_inf = json.load(f)
        # if worker not in data_inf:
        #     print(worker, 'new user from:', None)
            # data_tsk.setdefault(worker, lex['user_account'])
            #
            # # создать запись ПД
            # print(user_id, 'pd created')
            # info = lex['user_pd']
            # info['referral'] = None
            # info['first_start'] = None
            # info['tg_username'] = message.from_user.username
            # info['tg_fullname'] = message.from_user.full_name
            # print(info)
            # data_inf.setdefault(worker, info)

        if worker in data_inf:
            if isinstance(data_inf[worker], list):
                data_inf[worker] = data_inf[worker][0]
            ref = data_inf[worker].get('referral', None)
            username = data_inf[worker].get('tg_username', None)
            fullname = data_inf[worker].get('tg_fullname', None)
        else:
            ref = username = fullname = '?'

        rej_info_text=f'❌ Отклонено {len(rejected_files)} заданий.\nid{worker} {fullname} @{username} ref: {ref}\nПричина:\n{admin_response}'
        if len(rej_info_text) > 4096:
            dlina = len(rej_info_text)
            await msg.answer(
                text=f'Сообщение выйдет длиной в {dlina} символов. Максимальный лимит - 4096. Сократи на {dlina - 4096} и отправь заново')
            print('reject_too_long')
            log(logs, user, 'reject_too_long')
            return

        # продублировать всем админам
        for i in admins:
            await bot.send_message(chat_id=i, text=rej_info_text)

        # сообщить юзеру об отказе
        try:
            await bot.send_message(chat_id=worker, text=lex['reject'], parse_mode='HTML')
            msg_to_pin = await bot.send_message(chat_id=worker, text=txt_for_worker, parse_mode='HTML')
            await bot.pin_chat_message(message_id=msg_to_pin.message_id, chat_id=worker, disable_notification=True)
            log(logs, worker, 'rejected_delivered')
        except TelegramForbiddenError:
            await msg.answer(text=f'Юзер id{worker} заблокировал бота')
        except TelegramBadRequest:
            await msg.answer(text=f'Чат id{worker} не найден')
        except Exception as e:
            await msg.answer(text=f'Сообщение для id{worker} не доставлено\n{e}')

        # проставить reject в отклоненных файлах
        with open(baza_task, 'r', encoding='utf-8') as f:
            data = json.load(f)
        tasks = data[worker]
        for file in rejected_files:
            print('file', file, 'rejected')
            tasks[f'file{file}'][0] = 'reject'

        # проставить accept в остальных файлах
        for file in tasks:
            if tasks[file][0] == 'review':
                tasks[file][0] = 'accept'
                print(file, 'accepted')

        # сохранить статусы заданий
        data.setdefault(worker, tasks)
        with open(baza_task, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            print(worker, 'status saved')
        log(logs, worker, 'adm_rejected')


# admin нажал ✅
@router.callback_query(Access(admins+validators), F.data == 'admin_ok')
async def admin_ok(callback: CallbackQuery, bot:Bot):
    msg = callback.message

    # worker = вытащить id из текста сообщения
    worker = id_from_text(msg.text)

    # принять все файлы
    await accept_user(worker)
    log(logs, worker, 'admin_accept')

    # убрать кнопки админа
    await bot.edit_message_text(f'{msg.text}\n✅ Принято', msg.chat.id, msg.message_id, reply_markup=None)
    # Дать юзеру аппрув
    await bot.send_message(chat_id=worker, text=lex['all_approved']+f'id{worker}')
    log(logs, worker, 'admin_accept')
    # # сохранить ссылки
    # gc = pygsheets.authorize(service_file='token.json')
    # sheet_url = 'https://docs.google.com/spreadsheets/d/1dlZdboea3OAzNpivRxgDiQ6SaW14RjHdfFD-77HwGiQ/edit#gid=0'
    # spreadsheet = gc.open_by_url(sheet_url)
    # try:
    #     spreadsheet.add_worksheet(title=worker)
    # except googleapiclient.errors.HttpError:
    #     pass

    # сохранить ссылки в g_sheet, в отдельный tsv и print в консоль

    path = await get_tsv(TKN, bot, msg, worker)
    # отправить tsv админу
    for i in admins:
        await bot.send_document(chat_id=i, document=FSInputFile(path=path))


# admin нажал ❌
@router.callback_query(Access(admins+validators), lambda x: x.data == 'admin_no')
async def admin_no(callback: CallbackQuery, bot: Bot):
    msg = callback.message
    log(logs, str(msg.from_user.id), 'admin_no')

    # обновить сообщение у админа и убрать кнопки
    await bot.edit_message_text(f'{msg.text}\n\n❌ Отклонено. Напиши причину отказа '
                                f'для каждого файла <b>одним ответом на это сообщение</b>!\n\n'
                                f'Укажи номер задания и через пробел причину. Следующее задание '
                                f'- перенос строки. Например:\n'
                                f'\n<i>05 плохое качество'
                                f'\n51 обрезано лицо</i>',
                                msg.chat.id, msg.message_id, parse_mode='HTML', reply_markup=None)


# админ ответил на сообщение
@router.message(Access(admins+validators), F.reply_to_message)
async def reply_to_msg(msg: Message, bot: Bot):
    # ответ админа
    admin_response = str(msg.text)
    # сообщение, на которое отвечает админ
    orig = msg.reply_to_message

    # worker = вытащить id из текста сообщения
    worker = id_from_text(orig.text)
    txt_for_worker = '\n\n'

    # если админ тупит
    if not worker:
        await bot.send_message(orig.chat.id, 'На это сообщение не надо отвечать')

    # если админ написал причину отказа❌
    elif lex["adm_review"] in orig.text or orig.text.startswith('reject id'):
        print('adm reject')
        # записать номера отклоненных файлов
        # записать номера отклоненных файлов
        rejected_files = []
        correct_format = True
        for line in admin_response.split('\n'):
            print(line)
            file_num = line.split()[0]
            # убедиться, что каждая строка начинается с номера задания
            if not file_num.isnumeric():
                correct_format = False
                await bot.send_message(orig.chat.id, lex['wrong_rej_form'])
                break
            rejected_files.append(line.split()[0])
            txt_for_worker += line + '\n'

        if correct_format:
            # прочитать данные юзера из пд
            with open(baza_info, 'r', encoding='utf-8') as f:
                data_inf = json.load(f)
            # if worker not in data_inf:
            #     print(worker, 'new user from:', None)
            # data_tsk.setdefault(worker, lex['user_account'])
            #
            # # создать запись ПД
            # print(user_id, 'pd created')
            # info = lex['user_pd']
            # info['referral'] = None
            # info['first_start'] = None
            # info['tg_username'] = message.from_user.username
            # info['tg_fullname'] = message.from_user.full_name
            # print(info)
            # data_inf.setdefault(worker, info)

            if worker in data_inf:
                if isinstance(data_inf[worker], list):
                    data_inf[worker] = data_inf[worker][0]
                ref = data_inf[worker].get('referral', None)
                username = data_inf[worker].get('tg_username', None)
                fullname = data_inf[worker].get('tg_fullname', None)
            else:
                ref = username = fullname = '?'

            rej_info_text = f'❌ Отклонено {len(rejected_files)} заданий.\nid{worker} {fullname} @{username} ref: {ref}\nПричина:\n{admin_response}'
            if len(rej_info_text) > 4096:
                dlina = len(rej_info_text)
                await msg.answer(
                    text=f'Сообщение выйдет длиной в {dlina} символов. Максимальный лимит - 4096. Сократи на {dlina - 4096} и отправь заново')
                print('reject_too_long')
                log(logs, worker, 'reject_too_long')
                return

            # обновить сообщение у админа и дописать причину отказа
            if orig.from_user.is_bot:
                await bot.edit_message_text(f'❌ Отклонено. Причина:\n{admin_response}', orig.chat.id, orig.message_id,
                                            reply_markup=None)

            # продублировать всем админам
            for i in admins:
                await bot.send_message(chat_id=i, text=rej_info_text)

            # сообщить юзеру об отказе
            try:
                await bot.send_message(chat_id=worker, text=lex['reject'], parse_mode='HTML')
                msg_to_pin = await bot.send_message(chat_id=worker, text=txt_for_worker, parse_mode='HTML')
                await bot.pin_chat_message(message_id=msg_to_pin.message_id, chat_id=worker, disable_notification=True)
                log(logs, worker, 'rejected_delivered')
            except TelegramForbiddenError:
                await msg.answer(text=f'Юзер id{worker} заблокировал бота')
            except TelegramBadRequest:
                await msg.answer(text=f'Чат id{worker} не найден')
            except Exception as e:
                await msg.answer(text=f'Сообщение для id{worker} не доставлено\n{e}')

            # проставить reject в отклоненных файлах
            with open(baza_task, 'r', encoding='utf-8') as f:
                data = json.load(f)
            tasks = data[worker]
            for file in rejected_files:
                print('file', file, 'rejected')
                tasks[f'file{file}'][0] = 'reject'

            # проставить accept в остальных файлах
            for file in tasks:
                if tasks[file][0] == 'review':
                    tasks[file][0] = 'accept'
                    print(file, 'accepted')

            # сохранить статусы заданий
            data.setdefault(worker, tasks)
            with open(baza_task, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                print(worker, 'status saved')
            log(logs, worker, 'adm_rejected')

    # если админ отвечает на сообщение юзера
    elif worker:
        print('adm reply')
        # отпр ответ юзеру и всем админам
        for i in [worker]+admins:
            await bot.send_message(chat_id=i, text=lex['msg_from_admin']+txt_for_worker+admin_response)


# админ просит обнулить юзера
@router.message(Access(admins), F.text, F.text.lower() == 'del')
async def adm_del(msg: Message, state: FSMContext):
    await msg.answer(text='Введи пароль')
    await state.set_state(FSM.password)


# бот спрашивает пароль
@router.message(Access(admins), StateFilter(FSM.password))
async def adm_passw(msg: Message, state: FSMContext):
    if msg.text == TKN[:4]:
        await msg.delete()
        await msg.answer(text='Введи id, который нужно стереть, например id12345')
        await state.set_state(FSM.delete)
    else:
        await msg.answer(text='Неверный пароль')


# админ обнуляет юзера
@router.message(Access(admins), StateFilter(FSM.delete))
async def adm_deleted(msg: Message, bot: Bot, state: FSMContext):
    # worker = вытащить id из текста сообщения
    worker = id_from_text(msg.text.lower())
    if not worker:
        await msg.answer(text='Введи например id12345')
        return

    # чтение бд
    with open(baza_task, 'r', encoding='utf-8') as f1, open(baza_info, 'r', encoding='utf-8') as f2:
        data_tsk = json.load(f1)
        data_inf = json.load(f2)

    # скинуть бекап и удалить данные
    await bot.send_document(chat_id=msg.from_user.id, document=FSInputFile(path=baza_task))
    await bot.send_document(chat_id=msg.from_user.id, document=FSInputFile(path=baza_info))
    try:
        del data_tsk[worker]
    except KeyError as e:
        print('error', e)
    else:
        log(logs, worker, 'tasks deleted')
        print(worker, 'tasks deleted')
    try:
        del data_inf[worker]
    except KeyError as e:
        print('error', e)
    else:
        log(logs, worker, 'info deleted')
        print(worker, 'info deleted')

    # сохранить изменения
    with open(baza_task, 'w', encoding='utf-8') as f1, open(baza_info, 'w', encoding='utf-8') as f2:
        json.dump(data_tsk, f1, indent=2, ensure_ascii=False)
        json.dump(data_inf, f2, indent=2, ensure_ascii=False)

    await msg.answer(lex['deleted'])
    await state.clear()


# админ что-то пишет
@router.message(Access(admins+validators), F.content_type.in_({'text'}))
async def adm_msg(msg: Message, bot: Bot):
    user = str(msg.from_user.id)
    txt = msg.text

    if txt.startswith(TKN[:4]):
        # рассылка всем юзерам
        log(logs, user, 'rassylka')
        with open(baza_task, 'r', encoding='utf-8') as f1:
            data_tsk = json.load(f1)
        await bot.send_message(chat_id=user, text='Запущена рассылка')
        msg_sent = not_found = 0
        for i in data_tsk:
            try:
                await bot.send_message(chat_id=i, text=txt[4:], parse_mode='HTML')
                print('msg_sent', i)
                msg_sent += 1
            except:
                print('not_found', i)
                not_found += 1
        await bot.send_message(chat_id=user, text=f'Доставлено до {msg_sent} из {msg_sent + not_found} юзеров')

    # админ запрашивает файл
    elif txt.lower() == 'send bd':
        await bot.send_document(chat_id=user, document=FSInputFile(path=baza_task))
    elif txt.lower() == 'send info':
        await bot.send_document(chat_id=user, document=FSInputFile(path=baza_info))
    elif txt.lower() == 'send logs':
        await bot.send_document(chat_id=user, document=FSInputFile(path=logs))
    elif txt.lower() == 'send all':
        await bot.send_document(chat_id=user, document=FSInputFile(path=baza_task))
        await bot.send_document(chat_id=user, document=FSInputFile(path=baza_info))
        await bot.send_document(chat_id=user, document=FSInputFile(path=logs))

    # принять все файлы по айди юзера
    elif txt.lower().startswith('accept id'):
        # worker = вытащить id из текста сообщения
        worker = id_from_text(txt)

        # принять все файлы
        await accept_user(worker)
        log(logs, worker, 'admin_accept')
        #  сообщить админам
        for i in admins:
            await bot.send_message(
                text=f'✅ Приняты файлы от id{worker}', chat_id=i, disable_notification=True)

    # отпр тсв со всем что юзер скинул на данный момент
    elif txt.lower().startswith('tsv id'):
        # worker = вытащить id из текста сообщения
        worker = id_from_text(txt)
        log(logs, worker, 'admin_tsv')

        # отправить tsv админу
        path = await get_tsv(TKN, bot, msg, worker)
        await bot.send_document(chat_id=msg.from_user.id, document=FSInputFile(path=path))
        log(logs, worker, 'adm get_tsv')

    # отпр файлы юзера, прим сообщения: files id12345 review
    elif txt.lower().startswith('files id'):
        # worker = вытащить id из текста сообщения
        worker = id_from_text(msg.text)
        status = txt.lower().split()[-1]
        output = await send_files(worker, status)
        await msg.answer(text=f'Отправляю файлы юзера id{worker} в статаусе {status}')
        for i in output:
            file_id, task_message = i
            await bot.send_document(chat_id=user, document=file_id, caption=task_message, parse_mode='HTML', disable_notification=True)
        log(logs, worker, f'{status} files received by adm')
        log(logs, user, f'{status} files received from {worker}')

    # создать два задания для отладки
    elif txt.lower() == 'adm start':
        # чтение БД
        with open(baza_task, 'r', encoding='utf-8') as f:
            data_tsk = json.load(f)

        print('adm start')
        await bot.send_message(text=f'Ты админ. Доступно 2 задания для отладки /next', chat_id=user)
        data_tsk[user] = {"file01": ['status', 'file'], "file02": ['status', 'file']}
        # сохранить новые данные
        with open(baza_task, 'w', encoding='utf-8') as f:
            json.dump(data_tsk, f, indent=2, ensure_ascii=False)

    elif id_from_text(txt):
        if lex["adm_review"] in txt or txt.lower().startswith('reject id'):
            await msg.answer('Можешь написать отказ ответом на свое сообщение')
        # else:
        #     await msg.answer(f'Ответь на свое сообщение, и я покажу его юзеру id{id_from_text(txt)}')
    else:
        await msg.answer('Команда не распознана')
        log(logs, user, 'adm_tupit')


