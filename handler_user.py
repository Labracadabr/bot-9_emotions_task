import json
from aiogram import Router, Bot, F
from aiogram.filters import Command, CommandStart, StateFilter, CommandObject
from bot_logic import log, Access, FSM # dwnld_photo_or_doc
from config import Config, load_config
from keyboards import keyboard_admin, keyboard_user, keyboard_ok, keyboard_privacy
from settings import admins, baza_task, baza_info, referrals, tasks_tsv
from lexic import lex
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import CallbackQuery, Message, URLInputFile


# Инициализация всяких ботских штук
router: Router = Router()
config: Config = load_config()
TKN: str = config.tg_bot.token
storage: MemoryStorage = MemoryStorage()


# команда /help
@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
    print(message.from_user.id, '/help')
    log('logs.json', message.from_user.id, '/help')
    await message.answer(lex['help'])


# # чекнуть не в бане ли юзер
# @router.message(Access(book['ban']))
# async def no_access(message: Message):
#     log('logs.json', message.from_user.id, 'ban')
#     await message.answer(lex['ban'])


# команда /status - показать юзеру статус его заданий
@router.message(Command(commands=['status']))
async def process_status_command(msg: Message, bot: Bot):
    user = str(msg.from_user.id)
    print(user, '/status')
    log('logs.json', user, '/status')
    with open(baza_task, 'r') as f:
        data = json.load(f)

    # дать статус заданий по айди юзера
    async def get_status(user_id):
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
            non = '65'
        return f'✅ Принято - {acc}\n🔁 Надо переделать - {rej}\n⏳ На проверке - <b>{rev}</b>\n💪 Осталось сделать - {non}'

    # если это админ - показать статус всех юзеров
    if user in admins:
        answer_text = ''
        for usr in data:
            usr_stat = await get_status(usr)
            if not usr_stat.endswith('65'):
                answer_text += f'\nid{usr}\n{usr_stat}\n'
        if answer_text:
            await msg.answer('Статусы всех юзеров, кто отправил хотя бы один файл:\n'+answer_text, parse_mode='HTML')
        else:
            await msg.answer('Ещё никто ничего не отправил')

    # простому юзеру показать только его статус
    if user not in admins:
        stat = await get_status(user)
        await msg.answer(f'Ваши задания:\n\n{stat}', parse_mode='HTML')


# deep-link команда /start
@router.message(CommandStart())
async def start_command(message: Message, command: CommandObject, state: FSMContext, bot: Bot):
    referral = command.args
    user = message.from_user
    msg_time = message.date.strftime("%d/%m/%Y %H:%M")
    user_id = str(message.from_user.id)
    print(referral)
    print(f'Bot start id{user.id} {user.full_name} @{user.username} from:{referral}')

    # чтение БД
    with open(baza_task, 'r', encoding='utf-8') as f:
        data_tsk = json.load(f)
    with open(baza_info, 'r', encoding='utf-8') as f:
        data_inf = json.load(f)

    # если юзер без реферала и его раньше не было в БД: не проходит
    if user_id not in data_inf and referral not in referrals:
        print(user_id, 'new user wrong ref:', referral)
        await bot.send_message(chat_id=user_id, text=lex['no_ref'])

    # создать учетную запись юзера, если её еще нет и реферал есть
    elif user_id not in data_inf and referral in referrals:
        print(user_id, 'new user from:', referral)
        data_tsk.setdefault(user_id, lex['user_account'])

        # создать запись ПД
        print(user_id, 'pd created')
        info = lex['user_pd']
        info['referral'] = referral
        info['first_start'] = msg_time
        info['tg_username'] = message.from_user.username
        info['tg_fullname'] = message.from_user.full_name
        print(info)

        data_inf.setdefault(user_id, info)
        with open(baza_info, 'w', encoding='utf-8') as f:
            json.dump(data_inf, f, indent=2, ensure_ascii=False)
        data_inf.setdefault(user_id, info)

        # приветствие и выдача политики
        await message.answer(text=lex['start'], reply_markup=keyboard_privacy, parse_mode='HTML')
        await message.answer(text='С политикой ознакомлен и согласен', reply_markup=keyboard_ok)
        # бот переходит в состояние ожидания согласия с политикой
        await state.set_state(FSM.policy)
        # сообщить админу, кто стартанул бота
        for i in admins:
            await bot.send_message(
                text=f'Bot started by id{user.id} {user.full_name} @{user.username} from: {referral}',
                chat_id=i, disable_notification=True)
        # сохранить новые данные
        with open(baza_task, 'w', encoding='utf-8') as f:
            json.dump(data_tsk, f, indent=2, ensure_ascii=False)
        with open(baza_info, 'w', encoding='utf-8') as f:
            json.dump(data_inf, f, indent=2, ensure_ascii=False)
        # логи
        log('logs.json', 'logs',
            f'{msg_time}, {user.full_name}, @{user.username}, id {user.id}, {user.language_code}, start={referral}')
        log('logs.json', user.id, f'/start={referral}')

    # если юзер уже в БД и просто снова нажал старт
    else:
        await bot.send_message(text=lex['start_again'], chat_id=user_id, reply_markup=keyboard_user)
        log('logs.json', user.id, f'start_again')


# команда /next - дать юзеру след задание
@router.message(Command(commands=['next']))
async def next_cmnd(message: Message, bot: Bot, state: FSMContext):
    user = str(message.from_user.id)
    print(user, '/next')
    log('logs.json', user, '/next')

    # считать статусы заданий юзера
    with open(baza_task, 'r', encoding='utf-8') as f:
        data = json.load(f)
    tasks = data[user]

    # найти первое доступное задание, т.е. без статуса accept или review, и отправить юзеру
    more_tasks = False
    for file in tasks:
        if tasks[file][0] in ('status', 'reject'):
            more_tasks = True
            with open(tasks_tsv, 'r', encoding='utf-8') as f:
                next_task = []
                for line in f.readlines():
                    splited_line = line.split('\t')
                    if splited_line[0] == file:
                        next_task = splited_line
                        break
            # print(next_task)

            name = next_task[1]+' '+next_task[3]
            link = next_task[2]
            instruct = next_task[4]
            task_message = f'<a href="{link}">{name}</a>\n{instruct}'

            await bot.send_message(chat_id=user, text=task_message, parse_mode='HTML')
            # бот переходит в состояние ожидания след файла
            await state.set_state(FSM.ready_for_next)
            break

    # если задания кончились
    if not more_tasks:
        await bot.send_message(chat_id=user, text=lex['no_more'], parse_mode='HTML')


# юзер согласен с политикой ✅
@router.callback_query(lambda x: x.data == "ok_pressed", StateFilter(FSM.policy))
async def privacy_ok(callback: CallbackQuery, bot: Bot, state: FSMContext):
    worker = callback.from_user
    print(worker.id, 'privacy_ok')
    log('logs.json', worker.id, 'privacy_ok')

    # выдать инструкцию и примеры
    msg_to_pin = await bot.send_message(text=lex['instruct1'], chat_id=worker.id, parse_mode='HTML')
    await bot.send_message(text=f"{lex['instruct2']}\n\n{lex['full_hd']}", chat_id=worker.id, parse_mode='HTML',
                           disable_web_page_preview=True, reply_markup=keyboard_user)
    await bot.pin_chat_message(message_id=msg_to_pin.message_id, chat_id=worker.id, disable_notification=True)

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
    log('logs.json', msg.from_user.id, 'compressed_file')
    await msg.reply(lex['full_hd'], parse_mode='HTML')


# юзер отправил норм файл
@router.message(F.content_type.in_({'document'}), StateFilter(FSM.ready_for_next))
async def file_ok(msg: Message, bot: Bot, state: FSMContext):
    user = str(msg.from_user.id)

    with open(baza_task, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # вычисляем, какое было прислано задание
    sent_file = ''
    tasks = data[user]
    for i in tasks:
        # print(tasks[i])
        if tasks[i][0] in ('status', 'reject'):
            sent_file = i
            log('logs.json', user, f'SENT_{sent_file}')
            break
    print(user, 'sent', sent_file)

    # меняем статус задания и сохраняем file_id
    data[user][sent_file] = ('review', msg.document.file_id)
    tasks = data[user]
    with open(baza_task, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    # проверить остались ли доступные задания
    more_tasks = False
    for i in tasks:
        if tasks[i][0] in ('status', 'reject'):
            more_tasks = True
            break

    # если остались еще задания
    if more_tasks:
        # Бот ожидает нажатия /next
        await state.set_state(FSM.done_a_task)
        await msg.reply(text=lex['receive'].format(sent_file[-2:]), reply_markup=keyboard_user)

    # если был отправлен последний файл
    if not more_tasks:
        # прочитать реферал из бд
        with open(baza_info, 'r', encoding='utf-8') as f:
            data_inf = json.load(f)
        ref = data_inf[user]['referral']

        # уведомить юзера, админов, внести в логи и в консоль
        await msg.reply(lex['all_sent'])
        log('logs.json', user, 'SENT_ALL_FILES')
        print(user, 'SENT_ALL_FILES')
        for i in admins:
            await bot.send_message(chat_id=i, text=f'Юзер отправил все файлы - id{user}'
                                                   f'\n{msg.from_user.full_name} @{msg.from_user.username} ref: {ref}')
        # Отправить файлЫ админу на проверку
        for task in tasks:
            print('adm', task)
            if tasks[task][0] == 'review':
                # Отправить каждый файл, у которого статус == review
                file_id = tasks[task][1]
                text = lex['tasks'][task].split('\n')[0]

                await bot.send_document(chat_id=admins[0], document=file_id, caption=text, parse_mode='HTML')  # Крис
                await bot.send_document(chat_id=admins[1], document=file_id, caption=text, parse_mode='HTML')  # Илья

        with open(baza_info, 'r', encoding='utf-8') as f:
            data_inf = json.load(f)

        ref = data_inf[user]['referral']
        # сообщение с кнопками (✅принять или нет❌)
        await bot.send_message(chat_id=admins[0], text=f'{lex["adm_review"]} id{user}?'
                                                       f'\n{msg.from_user.full_name} @{msg.from_user.username} ref: {ref}',
                               reply_markup=keyboard_admin)


# команда /cancel - отменить отправленный файл
@router.message(Command(commands=['cancel']))
async def cancel_command(msg: Message, bot: Bot, state: FSMContext):
    user = str(msg.from_user.id)
    print(user, '/cancel')
    log('logs.json', user, '/cancel')
    with open(baza_task, 'r') as f:
        data = json.load(f)
    if user in data:
        # проверить, не отправлены ли все файлы уже на проверку
        statuses = set(data[user][i][0] for i in data[user])
        if 'status' in statuses or 'reject' in statuses:
            await bot.send_message(chat_id=user, text=lex['cancel'])
            # Бот ожидает номера заданий
            await state.set_state(FSM.cancelation)
        else:
            await bot.send_message(chat_id=user, text=lex['cancel_fail'])
    else:
        await bot.send_message(chat_id=user, text=lex['cancel_fail'])


# удаление отмененных файлов
@router.message(F.content_type.in_({'text'}), StateFilter(FSM.cancelation))
async def cancel(msg: Message, bot: Bot, state: FSMContext):
    user = str(msg.from_user.id)

    # обработать номера заданий
    nums_to_cancel = []
    for num in msg.text.split():
        if num.isnumeric() and len(num) == 2:
            nums_to_cancel.append(num)
        else:
            await msg.reply(lex['cancel_wrong_form'])
            break

    # если все номера указаны верно
    if len(msg.text.split()) == len(nums_to_cancel):
        # прочитать данные из БД
        with open(baza_task, 'r', encoding='utf-8') as f:
            data = json.load(f)
        tasks = data[user]

        # если это задание на проверке, то обнулить
        cancelled, not_found = [], []
        for num in nums_to_cancel:
            try:
                if tasks[f'file{num}'][0] == 'review':
                    tasks[f'file{num}'] = ["status", "file"]
                    cancelled.append(num)
                else:
                    not_found.append(num)
            except KeyError:
                not_found.append(num)

        # сохранить статусы заданий
        data.setdefault(user, tasks)
        with open(baza_task, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(user, 'files cancelled', cancelled)

        # уведомить юзера о результате
        await msg.reply(text=lex['cancel_ok']+', '.join(cancelled))
        await state.clear()
        if not_found:
            await msg.answer(text=lex['cancel_not_found']+', '.join(not_found))


# юзер что-то пишет
@router.message(~Access(admins), F.content_type.in_({'text'}))
async def usr_txt2(msg: Message, bot: Bot):
    log('logs.json', msg.from_user.id, msg.text)

    # показать админам
    for i in admins:
        await bot.send_message(chat_id=i, text=f'{lex["msg_to_admin"]} @{msg.from_user.username} {msg.from_user.full_name}'
                                               f' id{msg.from_user.id}: \n\n{msg.text}')
