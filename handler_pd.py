import json
from aiogram import Router, Bot, F
from aiogram.filters import Command, CommandStart, StateFilter, CommandObject
from bot_logic import log, Access, FSM # dwnld_photo_or_doc
from config import Config, load_config
from settings import admins, baza_task, baza_info, referrals, logs
from lexic import lex
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import CallbackQuery, Message


# Инициализация всяких ботских штук
router: Router = Router()
config: Config = load_config()
TKN: str = config.tg_bot.token
storage: MemoryStorage = MemoryStorage()


# команда /personal - заполнить ПД
@router.message(Command(commands=['personal']))
async def cancel_command(msg: Message, state: FSMContext):
    user = str(msg.from_user.id)
    print(user, msg.text)
    log(logs, user, msg.text)
    # чтение БД
    with open(baza_info, 'r', encoding='utf-8') as f:
        data_inf = json.load(f)

    # проверить есть ли его ПД в БД
    try:
        data_inf[user]
    except KeyError:
        # создать запись ПД
        print(user, 'pd created')
        log(logs, user, 'pd created')
        info = lex['user_pd']
        info['first_start'] = msg.date.strftime("%d/%m/%Y %H:%M")
        info['tg_username'] = msg.from_user.username
        info['tg_fullname'] = msg.from_user.full_name

        data_inf.setdefault(user, info)
        with open(baza_info, 'w', encoding='utf-8') as f:
            json.dump(data_inf, f, indent=2, ensure_ascii=False)

    # проверить заполнены ли уже перс данные
    try:
        data_inf[user]['gender']
        log(logs, user, 'try')
        print('try')
    except KeyError:
        data_inf[user].setdefault('gender', None)
        log(logs, user, 'exc')
        print('exc')
    if not data_inf[user]['gender']:
        # спросить возраст
        await state.set_state(FSM.age)
        await msg.answer(lex['age'])
        print(user, 'ask age')
        log('logs.json', user, 'ask age')

    else:
        await msg.answer(lex['pd_ok'])
        log('logs.json', user, 'pd ok')


# юзер отправляет возраст
@router.message(F.content_type.in_({'text'}), StateFilter(FSM.age))
async def cancel(msg: Message, bot: Bot, state: FSMContext):
    user = str(msg.from_user.id)
    age = msg.text
    print(user, age)
    log('logs.json', user, age)

    # проверка правильного ввода
    if age.isnumeric() and len(age) == 2:
        # чтение БД
        with open(baza_info, 'r', encoding='utf-8') as f:
            data_inf = json.load(f)

        # сохранить возраст в БД
        data_inf[user]['age'] = age
        with open(baza_info, 'w', encoding='utf-8') as f:
            json.dump(data_inf, f, indent=2, ensure_ascii=False)
        # спросить пол
        await state.set_state(FSM.gender)
        await msg.answer(text=lex['gender'])
        print(user, 'ask gender')
        log('logs.json', user, 'ask gender')

    else:
        await msg.reply(text=lex['age_bad'])


# юзер отправляет пол
@router.message(F.content_type.in_({'text'}), StateFilter(FSM.gender))
async def cancel(msg: Message, state: FSMContext):
    user = str(msg.from_user.id)
    gender = msg.text.lower()
    print(user, gender)
    log('logs.json', user, gender)

    # проверка правильности ввода
    if gender == 'm' or gender == 'f':
        # чтение БД
        with open(baza_info, 'r', encoding='utf-8') as f:
            data_inf = json.load(f)

        # сохранить пол в БД
        data_inf[user]['gender'] = gender
        with open(baza_info, 'w', encoding='utf-8') as f:
            json.dump(data_inf, f, indent=2, ensure_ascii=False)

        if data_inf[user]['referral']:
            # если асессор из TD, то спросить фио

            if data_inf[user]['referral'].lower() == 'td':
                await state.set_state(FSM.fio)
                await msg.answer(text=lex['fio'])
                log('logs.json', user, 'ask gender')
                print(user, 'fio')

            # если толокер, то дать id
            elif data_inf[user]['referral'].lower() == 'toloka':
                print(user, 'toloka')
                await msg.answer(text=lex['tlk_ok'])
                await msg.answer(text=f'<code>{user}</code>', parse_mode='HTML')
                log('logs.json', user, 'tlk ok')
                await state.clear()

            else:
                await msg.answer(text=lex['pd_ok'])
                log('logs.json', user, 'gender ok')
                await state.clear()
        else:
            await msg.answer(text=lex['pd_ok'])
            log('logs.json', user, 'gender ok')
            await state.clear()
    else:
        await msg.reply(text=lex['gender_bad'])


# юзер отправляет ФИО
@router.message(F.content_type.in_({'text'}), StateFilter(FSM.fio))
async def cancel(msg: Message, state: FSMContext):
    user = str(msg.from_user.id)
    fio = msg.text
    print(user, fio)
    log('logs.json', user, fio)
    slov = len(fio.split())

    # проверка правильности ввода
    if slov == 3 or slov == 2 and all(isinstance(item, str) for item in fio):
        # чтение БД
        with open(baza_info, 'r', encoding='utf-8') as f:
            data_inf = json.load(f)

        # сохранить фио в БД
        data_inf[user]['fio'] = fio
        with open(baza_info, 'w', encoding='utf-8') as f:
            json.dump(data_inf, f, indent=2, ensure_ascii=False)

        await msg.answer(text=lex['pd_ok'])
        log('logs.json', user, 'fio ok')
        await state.clear()
    else:
        await msg.reply(text=lex['fio_bad'])

