import json
from aiogram import Router, Bot, F
from aiogram.filters import Command, StateFilter, or_f
from bot_logic import log, Access, FSM # dwnld_photo_or_doc
from config import Config, load_config
from keyboards import keyboard_admin, keyboard_user, keyboard_ok, keyboard_privacy
from settings import admins, baza
from lexic import lex
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import CallbackQuery, Message


# Инициализация всяких ботских штук
router: Router = Router()
config: Config = load_config()
TKN: str = config.tg_bot.token
storage: MemoryStorage = MemoryStorage()


# команда /help
@router.message(Command(commands=['help']))
async def process_help_command(message: Message):
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
    log('logs.json', user, '/status')
    with open(baza, 'r') as f:
        data = json.load(f)

    async def get_status(user_id):
        non = rev = rej = acc = 0

        try:
            info = data[user_id]
            for task in info:
                print(task)
                if info[task][0] == 'status':
                    non += 1
                if info[task][0] == 'review':
                    rev += 1
                if info[task][0] == 'reject':
                    rej += 1
                if info[task][0] == 'accept':
                    acc += 1
        except KeyError:
            non = '65'
        return f'✅ Принято - {acc}\n🔁 Надо переделать - {rej}\n⏳ На проверке - {rev}\n💪 Осталось сделать - {non}'

    if user in admins:
        answer_text = ''
        for usr in data:
            usr_stat = await get_status(usr)
            if not usr_stat.endswith('65'):
                answer_text += f'\nid{usr}\n{usr_stat}\n'
        if answer_text:
            await msg.answer('Статусы всех юзеров, кто отправил хотя бы один файл:\n'+answer_text)
        else:
            await msg.answer('Ещё никто ничего не отправил')

    if user not in admins:
        stat = await get_status(user)
        await msg.answer(f'Ваши задания:\n\n{stat}')


# команда /start
@router.message(Command(commands=['start']))
async def process_start_command(message: Message, bot: Bot, state: FSMContext):
    user = message.from_user
    msg_time = message.date.strftime("%d/%m/%Y %H:%M")
    # print(message.json(indent=4, exclude_none=True))
    print(f'Bot started by id{user.id} {user.full_name} @{user.username}')

    # логи
    log('logs.json', 'logs',
        f'{msg_time}, {user.full_name}, @{user.username}, id {user.id}, {user.language_code}')
    log('logs.json', user.id, '/start')

    # приветствие и выдача политики
    await message.answer(text=lex['start'], reply_markup=keyboard_privacy, parse_mode='HTML')
    await message.answer(text='С политикой ознакомлен и согласен', reply_markup=keyboard_ok)
    # бот переходит в состояние ожидания согласие с политикой
    await state.set_state(FSM.policy)

    # сообщить админу, кто стартанул бота
    if str(user.id) not in admins:
        for i in admins:
            await bot.send_message(text=f'Bot started by id{user.id} {user.full_name} @{user.username}',
                                   chat_id=i, disable_notification=True)

    # создать учетную запись юзера, если её еще нет
    with open(baza, 'r') as f:
        data = json.load(f)
    if str(user.id) not in data:
        data.setdefault(str(user.id), lex['user_account'])
        with open(baza, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


# команда /next - дать юзеру след задание
@router.message(Command(commands=['next']))
async def next_cmnd(message: Message, bot: Bot, state: FSMContext):
    user = str(message.from_user.id)
    log('logs.json', user, '/next')

    # считать статусы заданий юзера
    with open(baza, 'r') as f:
        data = json.load(f)
    tasks = data[user]

    # найти первое доступное задание, т.е. без статуса accept или review, и отправить юзеру
    for i in tasks:
        if tasks[i][0] in ('status', 'reject'):
            await bot.send_message(chat_id=user, text=lex['tasks'][i], parse_mode='HTML')
            break

    # бот переходит в состояние ожидания след файла
    await state.set_state(FSM.ready_for_next)


# юзер согласен с политикой ✅
@router.callback_query(lambda x: x.data == "ok_pressed", StateFilter(FSM.policy))
async def privacy_ok(callback: CallbackQuery, bot: Bot, state: FSMContext):
    worker = callback.from_user
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

    # сохраняем ссылку на файл
    file_id = msg.document.file_id

    with open(baza, 'r') as f:
        data = json.load(f)

    # вычисляем, какое было прислано задание
    sent_file = ''
    tasks = data[user]
    for i in tasks:
        print(tasks[i])
        if tasks[i][0] in ('status', 'reject'):
            sent_file = i
            log('logs.json', user, f'SENT_{sent_file}')
            break

    # меняем статус задания и сохраняем
    data[user][sent_file] = ('review', file_id)
    tasks = data[user]
    with open(baza, 'w', encoding='utf-8') as f:
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
        # await msg.reply(f'Получен файл для задания {sent_file[-2:]}.\nНажмите /next для следующего задания', reply_markup=keyboard_user)
        await msg.reply(text=lex['receive'].format(sent_file[-2:]), reply_markup=keyboard_user)

    # если был отправлен последний файл
    if not more_tasks:
        # уведомить юзера чтоб ожидал проверку
        await msg.reply(lex['all_sent'])
        # Отправить файлЫ админу на проверку
        for task in tasks:
            print('adm', task)
            if tasks[task][0] == 'review':
                # Отправить каждый файл, у которого статус == review
                file_id = tasks[task][1]
                text = lex['tasks'][task].split('\n')[0]

                await bot.send_document(chat_id=admins[0], document=file_id, caption=text, parse_mode='HTML')

        # сообщение с кнопками (✅принять или нет❌)
        await bot.send_message(chat_id=admins[0], text=f'Принять ВСЕ файлы от id{user}?'
                                                       f'\n{msg.from_user.full_name} @{msg.from_user.username}', reply_markup=keyboard_admin)

        log('logs.json', user, 'SENT_ALL_FILES')


