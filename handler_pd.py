import json
from aiogram import Router, Bot, F
from aiogram.filters import Command, CommandStart, StateFilter, CommandObject
from bot_logic import log, FSM
from config import Config, load_config
from settings import baza_info, logs
from lexic import lex
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message


# Инициализация
router: Router = Router()
config: Config = load_config()
TKN: str = config.tg_bot.token
storage: MemoryStorage = MemoryStorage()


# команда /personal - заполнить ПД
@router.message(Command(commands=['personal']))
async def personal_command(msg: Message, state: FSMContext):
    user = str(msg.from_user.id)
    await log(logs, user, msg.text)
    # чтение БД
    with open(baza_info, 'r', encoding='utf-8') as f:
        data_inf = json.load(f)

    # проверить есть ли его ПД в БД
    try:
        data_inf[user]
    except KeyError:
        # создать запись ПД
        await log(logs, user, 'pd created')
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
    except KeyError:
        data_inf[user].setdefault('gender', None)
    if not data_inf[user]['gender']:
        # спросить возраст
        await state.set_state(FSM.age)
        await msg.answer(lex['age'])
        await log(logs, user, 'ask age')

    else:
        await msg.answer(lex['pd_ok'])
        await log(logs, user, 'pd already ok')


# юзер отправляет возраст
@router.message(F.content_type.in_({'text'}), StateFilter(FSM.age))
async def personal_age(msg: Message, state: FSMContext):
    user = str(msg.from_user.id)
    age = msg.text
    await log(logs, user, f'age: {age}')

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
        await log(logs, user, 'ask gender')

    else:
        await msg.reply(text=lex['age_bad'])


# юзер отправляет пол
@router.message(F.content_type.in_({'text'}), StateFilter(FSM.gender))
async def personal_sex(msg: Message, state: FSMContext):
    user = str(msg.from_user.id)
    gender = msg.text.lower()
    await log(logs, user, f'gender: {gender}')

    # проверка правильности ввода
    if gender in ('m', 'f'):
        # чтение БД
        with open(baza_info, 'r', encoding='utf-8') as f:
            data_inf = json.load(f)

        # сохранить пол в БД
        data_inf[user]['gender'] = gender
        with open(baza_info, 'w', encoding='utf-8') as f:
            json.dump(data_inf, f, indent=2, ensure_ascii=False)

        # спросить страну
        await msg.answer(text=lex['country'])
        await log(logs, user, 'gender ok')
        await state.set_state(FSM.country)
    else:
        await msg.reply(text=lex['gender_bad'])


# юзер отправляет страну
@router.message(F.content_type.in_({'text'}), StateFilter(FSM.country))
async def personal_country(msg: Message, state: FSMContext):
    user = str(msg.from_user.id)
    country = msg.text.capitalize()
    await log(logs, user, f'country: {country}')

    # чтение БД
    with open(baza_info, 'r', encoding='utf-8') as f:
        data_inf = json.load(f)

    # сохранить страну в БД
    data_inf[user]['fio'] = country
    with open(baza_info, 'w', encoding='utf-8') as f:
        json.dump(data_inf, f, indent=2, ensure_ascii=False)

    if data_inf[user]['referral']:
        # если асессор из TD, то спросить фио
        if data_inf[user]['referral'].lower() == 'td':
            await state.set_state(FSM.fio)
            await msg.answer(text=lex['fio'])
            await log(logs, user, 'ask fio')

        # если толокер, то дать id
        elif data_inf[user]['referral'].lower() == 'toloka':
            print(user, 'toloka')
            await msg.answer(text=lex['tlk_ok'])
            await msg.answer(text=f'<code>{user}</code>', parse_mode='HTML')
            await log(logs, user, 'tlk ok')
            await state.clear()

        else:
            await msg.answer(text=lex['pd_ok'])
            await log(logs, user, 'country ok')
            await state.clear()
    else:
        await msg.answer(text=lex['pd_ok'])
        await log(logs, user, 'country ok')
        await state.clear()


# юзер отправляет фио
@router.message(F.content_type.in_({'text'}), StateFilter(FSM.fio))
async def personal_fio(msg: Message, state: FSMContext):
    user = str(msg.from_user.id)
    fio = msg.text
    print(user, fio)
    await log(logs, user, f'fio: {fio}')
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
        await log(logs, user, 'fio ok')
        await state.clear()
    else:
        await msg.reply(text=lex['fio_bad'])

