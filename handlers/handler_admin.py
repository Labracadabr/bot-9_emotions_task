from aiogram import Router, Bot, F
from settings import admins, baza_task, baza_info, logs, validators, check_files
from bot_logic import *
import json
import os
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest
from config import config

# Инициализация бота
TKN = config.BOT_TOKEN
router: Router = Router()


# # Забанить юзера по telegram id. Пример сообщения: ban id123456789
# @router.message(Access(admins), lambda msg: str(msg.text).lower().startswith('ban '))
# async def banner(msg: Message):
#     # вытащить id из текста сообщения
#     ban_id = str(msg.text).split()[-1]
#     if ban_id.lower().startswith('id'):
#         ban_id = ban_id[2:]
#
#     await log('user_status.json', 'ban', ban_id)
#     await msg.answer(text=f'id {ban_id} banned')


# admin нажал ✅
@router.callback_query(Access(admins+validators), F.data == 'admin_ok')
async def admin_ok(callback: CallbackQuery, bot: Bot):
    msg = callback.message

    # worker = вытащить id из текста сообщения
    worker = id_from_text(msg.text)
    language = await get_pers_info(user=worker, key='lang')
    lexicon = load_lexicon(language)

    # принять все файлы
    await accept_user(worker)
    await log(logs, worker, 'admin_accept_button')

    # убрать кнопки админа
    await bot.edit_message_text(f'{msg.text}\n✅ Принято', msg.chat.id, msg.message_id, reply_markup=None)
    # Дать юзеру аппрув
    await bot.send_message(chat_id=worker, text=lexicon['all_approved']+f'id{worker}')
    # сохранить ссылки
    path = await get_tsv(TKN, bot, msg, worker)
    # отправить tsv админу
    for i in admins:
        await bot.send_document(chat_id=i, caption='Принято '+worker, document=FSInputFile(path=path))
    os.remove(path)


# admin нажал ❌
@router.callback_query(Access(admins+validators), lambda x: x.data == 'admin_no')
async def admin_no(callback: CallbackQuery, bot: Bot):
    msg = callback.message
    await log(logs, str(msg.from_user.id), 'admin_no')

    # обновить сообщение у админа и убрать кнопки
    await bot.edit_message_text(f'{msg.text}\n\n❌ Отклонено. Напиши причину отказа '
                                f'для каждого файла <b>одним ответом на это сообщение</b>!\n\n'
                                f'Укажи номер задания и через пробел причину. Следующее задание '
                                f'- перенос строки. Например:\n\n<i>05 плохое качество\n51 обрезано лицо</i>',
                                msg.chat.id, msg.message_id, parse_mode='HTML', reply_markup=None)


# админ ответил на сообщение или написал отказ
@router.message(Access(admins+validators), F.reply_to_message)
async def reply_to_msg(msg: Message, bot: Bot):
    admin = str(msg.from_user.id)
    # ответ админа
    admin_response = str(msg.text)
    # сообщение, на которое отвечает админ
    orig = msg.reply_to_message

    # worker = вытащить id из текста сообщения
    worker = id_from_text(orig.text)
    language = await get_pers_info(user=worker, key='lang')
    user_lexicon = load_lexicon(language)
    adm_lexicon = __import__('lexic.adm', fromlist=['']).lexicon

    txt_for_worker = '\n\n'

    # если админ тупит
    if not worker:
        await bot.send_message(orig.chat.id, 'На это сообщение не надо отвечать')
        await log(logs, admin, 'response_fail')
        return

    # если админ написал причину отказа❌
    elif adm_lexicon["adm_review"] in orig.text or orig.text.lower().startswith('reject id'):
        print('adm reject')

        # если отказ начинается на * - отклонить всё
        reject_all = True if admin_response.startswith('*') else False
        if reject_all:
            rejected_files = [str(i) for i in range(1, total_tasks+1)]
            txt_for_worker = admin_response.replace('*', '')

        # иначе - записать номера отклоненных файлов
        else:
            rejected_files = []
            txt_for_worker = '\n\n'
            for line in admin_response.split('\n'):
                print(line)
                file_num = line.split()[0]
                # убедиться, что каждая строка начинается с номера задания
                if not file_num.isnumeric():
                    await bot.send_message(orig.chat.id, adm_lexicon['wrong_rej_form'])
                    await log(logs, worker, 'reject_fail')
                    return
                if int(file_num) > total_tasks:
                    await bot.send_message(orig.chat.id, text=f'Нет задания под номером {file_num}\nНапиши причину отказа снова.')
                    await log(logs, worker, 'reject_fail')
                    return

                rejected_files.append(line.split()[0])  # внести номер задания, напр 02
                txt_for_worker += line + '\n'

        # прочитать данные юзера из пд
        with open(baza_info, 'r', encoding='utf-8') as f:
            data_inf = json.load(f)

        if worker in data_inf:
            # if isinstance(data_inf[worker], list):  # из старой версии
            #     data_inf[worker] = data_inf[worker][0]
            ref = data_inf[worker].get('referral', None)
            username = data_inf[worker].get('tg_username', None)
            fullname = data_inf[worker].get('tg_fullname', None)
        else:
            ref = username = fullname = '?'

        rej_info_text = f'❌ Отклонено {len(rejected_files)} заданий.\nid{worker} {fullname} @{username} ref: {ref}\nПричина:\n{admin_response}'

        # если слишком длинный текст
        if len(rej_info_text) > 4096:
            dlina = len(rej_info_text)
            await msg.answer(
                text=f'Сообщение выйдет длиной в {dlina} символов. Максимальный лимит - 4096. Сократи на {dlina - 4096} и отправь заново')
            print('reject_too_long')
            await log(logs, worker, 'reject_too_long')
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
            reject_alert = user_lexicon['reject_all'] if reject_all else user_lexicon['reject']
            await bot.send_message(chat_id=worker, text=reject_alert, parse_mode='HTML')
            msg_to_pin = await bot.send_message(chat_id=worker, text=txt_for_worker, parse_mode='HTML')
            await bot.pin_chat_message(message_id=msg_to_pin.message_id, chat_id=worker, disable_notification=True)
            await log(logs, worker, 'rejected_delivered')
        except TelegramForbiddenError:
            await msg.answer(text=f'Юзер id{worker} заблокировал бота')
        except TelegramBadRequest:
            await msg.answer(text=f'Чат id{worker} не найден')
        except Exception as e:
            await msg.answer(text=f'Сообщение для id{worker} не доставлено\n{e}')

        # чтение бд
        with open(baza_task, 'r', encoding='utf-8') as f:
            data = json.load(f)
        tasks = data[worker]

        # проставить reject в отклоненных файлах
        count = 0
        for file in rejected_files:
            print('file', file, 'rejected')
            tasks[f'file{file.zfill(2)}'][0] = 'reject'
            count += 1
        await log(logs, worker, f'{count} rejected')

        # проставить accept в файлах, которые остались в статусе review
        count = 0
        for file in tasks:
            if tasks[file][0] == 'review':
                tasks[file][0] = 'accept'
                print(file, 'accepted')
                count += 1
        await log(logs, worker, f'{count} accepted')

        # сохранить статусы заданий
        data.setdefault(worker, tasks)
        with open(baza_task, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            print(worker, 'status saved')
        await log(logs, worker, 'status saved, admin '+admin)

        # плюсануть кол-во отказов
        try:
            data_inf[worker].setdefault('reject', data_inf[worker].get('reject') + 1)
        except Exception as e:
            await log(logs, worker, f'small_error: {e}')

    # если админ отвечает на сообщение юзера
    elif worker:
        await log(logs, worker, f'adm_reply: {admin_response}')
        # отпр ответ юзеру и всем админам
        for i in [worker]+admins:
            await bot.send_message(chat_id=i, text=user_lexicon['msg_from_admin']+txt_for_worker+admin_response)


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
        await msg.answer(text='Введи, что стереть, например id12345')
        await state.set_state(FSM.delete)
    else:
        await msg.answer(text='Неверный пароль')


# админ обнуляет юзера
@router.message(Access(admins), StateFilter(FSM.delete))
async def adm_deleted(msg: Message, bot: Bot, state: FSMContext):
    txt = msg.text.lower()

    # удаление всего (вообще все акки юзеров)
    if txt == 'drop database':
        with open(baza_task, 'r', encoding='utf-8') as f:
            count = len(json.load(f))

        await msg.answer(f'Удалены аккаунты {count} юзеров, вот бекап до удаления')
        # прислать бекап
        await bot.send_document(chat_id=msg.from_user.id, document=FSInputFile(path=baza_task))
        await bot.send_document(chat_id=msg.from_user.id, document=FSInputFile(path=baza_info))
        await bot.send_document(chat_id=msg.from_user.id, document=FSInputFile(path=logs))
        # удалить все
        os.remove(logs)
        os.remove(baza_task)
        os.remove(baza_info)
        # создать все
        check_files()
        await log(logs, str(msg.from_user.id), f'drop database {count} users')
        await state.clear()
        return

    # worker = вытащить id из текста сообщения
    worker = id_from_text(txt)
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
        await log(logs, worker, 'tasks deleted')
        print(worker, 'tasks deleted')
    try:
        del data_inf[worker]
    except KeyError as e:
        print('error', e)
    else:
        await log(logs, worker, 'info deleted')
        print(worker, 'info deleted')

    # сохранить изменения
    with open(baza_task, 'w', encoding='utf-8') as f1, open(baza_info, 'w', encoding='utf-8') as f2:
        json.dump(data_tsk, f1, indent=2, ensure_ascii=False)
        json.dump(data_inf, f2, indent=2, ensure_ascii=False)

    await msg.answer('Удалено, вот бекап до удаления')
    await state.clear()


# админ что-то пишет
@router.message(Access(admins+validators), F.content_type.in_({'text'}))
async def adm_msg(msg: Message, bot: Bot):
    admin = str(msg.from_user.id)
    txt = msg.text
    adm_lexicon = __import__('lexic.adm', fromlist=['']).lexicon

    if txt.startswith(TKN[:4]):
        # рассылка всем юзерам
        await log(logs, admin, 'rassylka')
        with open(baza_task, 'r', encoding='utf-8') as f1:
            users = json.load(f1)
        await bot.send_message(chat_id=admin, text='Запущена рассылка')
        msg_sent = not_found = 0
        for user in users:
            try:
                await bot.send_message(chat_id=user, text=txt[4:], parse_mode='HTML')
                print('msg_sent', user)
                msg_sent += 1
            except:
                print('not_found', user)
                not_found += 1
        await bot.send_message(chat_id=admin, text=f'Доставлено до {msg_sent} из {len(users)} юзеров')

    # админ запрашивает файл
    elif txt.lower().startswith('send'):
        file = txt.lower().split()[-1]
        if file in ('bd', 'info', 'logs', 'all'):
            await send_json(user=admin, file=file)
        else:
            await msg.answer('Команда не распознана')
            await log(logs, admin, f'wrong_command: \n{txt}')

    # админ запрашивает перс данные
    elif txt.lower().startswith('pd'):
        worker = id_from_text(txt)
        # чтение бд
        with open(baza_info, 'r', encoding='utf-8') as f:
            data_inf = json.load(f)
        user_data = data_inf[worker]
        # создать json
        path = f'person_{worker}.json'
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(user_data, f, indent=2, ensure_ascii=False)
        # отправить и удалить
        await bot.send_document(chat_id=admin, document=FSInputFile(path))
        os.remove(path)
        await msg.answer(str(user_data))
        await log(logs, admin, 'admin_request_pd_'+worker)

    # показать существующие реф ссылки
    elif txt.lower().startswith('ref'):
        send_msg = 'Сохраненные реферальные ссылки:\n'
        # url бота
        bot_info = await bot.get_me()
        bot_link = f"https://t.me/{bot_info.username}?start="
        # слепить ссылки
        for ref in referrals:
            send_msg += bot_link+ref+'\n'
        # отправить
        await bot.send_message(chat_id=admin, text=send_msg)

    # принять все файлы по айди юзера
    elif txt.lower().startswith('accept id'):
        # worker = вытащить id из текста сообщения
        worker = id_from_text(txt)
        language = await get_pers_info(user=worker, key='lang')
        lexicon = load_lexicon(language)

        # принять все файлы
        await accept_user(worker)
        await log(logs, worker, 'admin_accept_command')
        # Дать юзеру аппрув
        await bot.send_message(chat_id=worker, text=lexicon['all_approved'] + f'id{worker}')
        #  сообщить админам
        for i in admins:
            await bot.send_message(
                text=f'✅ Приняты файлы от id{worker}', chat_id=i, disable_notification=True)

    # отпр тсв со всем что юзер скинул на данный момент
    elif txt.lower().startswith('tsv id'):
        # worker = вытащить id из текста сообщения
        worker = id_from_text(txt)
        await log(logs, worker, 'adm_ask_tsv')

        # отправить tsv админу
        path = await get_tsv(TKN, bot, msg, worker)
        await bot.send_document(chat_id=msg.from_user.id, document=FSInputFile(path=path))
        await log(logs, worker, 'adm_get_tsv')
        os.remove(path)

    # отпр файлы юзера, прим сообщения: files id12345 review
    elif txt.lower().startswith('files id'):
        # worker = вытащить id из текста сообщения
        worker = id_from_text(msg.text)
        status = txt.lower().split()[-1]
        output = await send_files(worker, status)
        await msg.answer(text=f'Отправляю файлы юзера id{worker} в статаусе {status}')
        for i in output:
            file_id, task_message = i
            await bot.send_document(chat_id=admin, document=file_id, caption=task_message, parse_mode='HTML', disable_notification=True)
        await log(logs, worker, f'{status} files received by adm')
        await log(logs, admin, f'{status} files received from {worker}')

    # создать два задания для отладки
    elif txt.lower() == 'adm start':
        # чтение БД
        with open(baza_task, 'r', encoding='utf-8') as f:
            users = json.load(f)

        print('adm start')
        await bot.send_message(text=f'Ты админ. Доступно 2 задания для отладки /next', chat_id=admin)
        users[admin] = create_account(task_amount=2)
        # сохранить новые данные
        with open(baza_task, 'w', encoding='utf-8') as f:
            json.dump(users, f, indent=2, ensure_ascii=False)

    elif id_from_text(txt):
        if adm_lexicon["adm_review"] in txt or txt.lower().startswith('reject id'):
            await msg.answer('Можешь написать отказ ответом на свое сообщение')
        # else:
        #     await msg.answer(f'Ответь на свое сообщение, и я покажу его юзеру id{id_from_text(txt)}')
    else:
        await msg.answer('Команда не распознана')
        await log(logs, admin, f'wrong_command: \n{txt}')

