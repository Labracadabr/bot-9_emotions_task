import json
from aiogram import Router, Bot, F
from aiogram.filters import Command, StateFilter
import template_pd
from bot_logic import log, FSM, get_pers_info, load_lexicon
# from config import Config, load_config
from settings import baza_info, logs, verification
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, CallbackQuery
from keyboards import keyboard_race
from config import config

# Инициализация бота
TKN = config.BOT_TOKEN
router: Router = Router()
storage: MemoryStorage = MemoryStorage()


# команда /personal - заполнить ПД
@router.message(Command(commands=['personal']))
async def personal_command(msg: Message, state: FSMContext):
    user = str(msg.from_user.id)
    language = await get_pers_info(user=user, key='lang')
    lexicon = load_lexicon(language)
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
        info = template_pd.user_pd
        info['first_start'] = msg.date.strftime("%d/%m/%Y %H:%M")
        info['tg_username'] = msg.from_user.username
        info['tg_fullname'] = msg.from_user.full_name

        data_inf.setdefault(user, info)
        with open(baza_info, 'w', encoding='utf-8') as f:
            json.dump(data_inf, f, indent=2, ensure_ascii=False)

    # проверить заполнены ли уже перс данные
    try:
        data_inf[user]['race']
    except KeyError:
        data_inf[user].setdefault('race', None)
    if not data_inf[user]['race']:
        # спросить возраст
        await state.set_state(FSM.age)
        await msg.answer(lexicon['age'])

    else:
        await msg.answer(lexicon['pd_ok'])
        await log(logs, user, 'pd already ok')


# юзер отправляет возраст > спросить пол
@router.message(F.content_type.in_({'text'}), StateFilter(FSM.age))
async def personal_age(msg: Message, state: FSMContext):
    user = str(msg.from_user.id)
    language = await get_pers_info(user=user, key='lang')
    lexicon = load_lexicon(language)
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
        await msg.answer(text=lexicon['gender'])

    else:
        await msg.reply(text=lexicon['age_bad'])


# юзер отправляет пол > спросить расу
@router.message(F.content_type.in_({'text'}), StateFilter(FSM.gender))
async def personal_sex(msg: Message, state: FSMContext):
    user = str(msg.from_user.id)
    language = await get_pers_info(user=user, key='lang')
    lexicon = load_lexicon(language)

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

        # спросить race
        await msg.answer(text=lexicon['race'], reply_markup=keyboard_race)
        await state.set_state(FSM.race)
    else:
        await msg.reply(text=lexicon['gender_bad'])


# юзер отправляет расу > спросить страну
@router.callback_query(StateFilter(FSM.race))
async def personal_sex(msg: CallbackQuery, state: FSMContext, bot: Bot):
    user = str(msg.from_user.id)
    language = await get_pers_info(user=user, key='lang')
    lexicon = load_lexicon(language)

    race = msg.data
    await log(logs, user, f'race: {race}')

    # чтение БД
    with open(baza_info, 'r', encoding='utf-8') as f:
        data_inf = json.load(f)

    # сохранить race в БД
    data_inf[user]['race'] = race
    with open(baza_info, 'w', encoding='utf-8') as f:
        json.dump(data_inf, f, indent=2, ensure_ascii=False)

    # спросить страну
    await bot.send_message(chat_id=user, text=lexicon['country'])
    await state.set_state(FSM.country)


# юзер отправляет страну > спросить фио если ТД, выдать код если толокер
@router.message(F.content_type.in_({'text'}), StateFilter(FSM.country))
async def personal_country(msg: Message, state: FSMContext):
    user = str(msg.from_user.id)
    language = await get_pers_info(user=user, key='lang')
    lexicon = load_lexicon(language)

    country = msg.text.capitalize()
    await log(logs, user, f'country: {country}')

    # чтение БД
    with open(baza_info, 'r', encoding='utf-8') as f:
        data_inf = json.load(f)

    # сохранить страну в БД
    data_inf[user]['country'] = country
    with open(baza_info, 'w', encoding='utf-8') as f:
        json.dump(data_inf, f, indent=2, ensure_ascii=False)

    if data_inf[user]['referral']:
        # если асессор из TD, то спросить фио
        if data_inf[user]['referral'].lower() == 'td':
            await state.set_state(FSM.fio)
            await msg.answer(text=lexicon['fio'])
            await log(logs, user, 'ask fio')

        # если толокер, то дать id
        elif data_inf[user]['referral'].lower() == 'toloka':
            await msg.answer(text=lexicon['tlk_ok'].format(verification, user), parse_mode='HTML')
            # await msg.answer(text=f'<code>{user}</code>', parse_mode='HTML')
            await log(logs, user, 'toloka ok')
            await state.clear()

        else:
            await msg.answer(text=lexicon['pd_ok'])
            await state.clear()
    else:
        await msg.answer(text=lexicon['pd_ok'])
        await state.clear()


# юзер отправляет фио > конец
@router.message(F.content_type.in_({'text'}), StateFilter(FSM.fio))
async def personal_fio(msg: Message, state: FSMContext):
    user = str(msg.from_user.id)
    language = await get_pers_info(user=user, key='lang')
    lexicon = load_lexicon(language)

    fio = msg.text
    print(user, fio)
    await log(logs, user, f'fio: {fio}')
    slov = len(fio.split())

    # проверка правильности ввода
    if slov == 3 or slov == 2 and all(item.isalpha() for item in fio):
        # чтение БД
        with open(baza_info, 'r', encoding='utf-8') as f:
            data_inf = json.load(f)

        # сохранить фио в БД
        data_inf[user]['fio'] = fio
        with open(baza_info, 'w', encoding='utf-8') as f:
            json.dump(data_inf, f, indent=2, ensure_ascii=False)

        await msg.answer(text=lexicon['pd_ok'])
        await log(logs, user, 'fio ok')
        await state.clear()
    else:
        await msg.reply(text=lexicon['fio_bad'])

