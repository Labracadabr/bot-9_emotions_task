from aiogram import Router, Bot, F, types
from aiogram.filters import Command, CommandStart, StateFilter, CommandObject, or_f
import template_pd
from bot_logic import *
# from config import Config, load_config
import keyboards
from settings import *
import template_pd
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import CallbackQuery, Message, URLInputFile
from config import config

# Инициализация бота
TKN = config.BOT_TOKEN
router: Router = Router()
storage: MemoryStorage = MemoryStorage()
last_group_id = ''

# # чекнуть не в бане ли юзер
# @router.message(Access(book['ban']))
# async def no_access(message: Message):
#     await log(logs, message.from_user.id, 'ban')
#     await message.answer(lexicon['ban'])


# deep-link команда /start
@router.message(CommandStart())
async def start_command(message: Message, command: CommandObject, state: FSMContext, bot: Bot):
    referral = command.args
    user = message.from_user
    msg_time = message.date.strftime("%d/%m/%Y %H:%M")
    user_id = str(user.id)
    print(f'Bot start id{user_id} {user.full_name} @{user.username} from:{referral}')

    # чтение БД
    with open(baza_task, 'r', encoding='utf-8') as f:
        data_tsk = json.load(f)
    with open(baza_info, 'r', encoding='utf-8') as f:
        data_inf = json.load(f)

    # язык
    # если это не первый старт - взять язык из памяти
    language = await get_pers_info(user=user_id, key='lang')
    # если первый - использовать язык приложения
    if not language:
        language = str(message.from_user.language_code).lower()
        print(language)
    lexicon = load_lexicon(language)

    # если юзер без реферала и его раньше не было в БД: не проходит
    if user_id not in data_inf and referral not in referrals:
        # print(user_id, 'new user wrong ref:', referral)
        await bot.send_message(chat_id=user_id, text=lexicon['no_ref'])
        await log(logs, user_id, f'wrong link @{user.username}')
        return

    # создать учетную запись юзера, если её еще нет и реферал есть
    elif user_id not in data_tsk and referral in referrals:
        if user_id not in data_inf:
            print(user_id, 'new user from:', referral)
            data_tsk.setdefault(user_id, create_account(task_amount=total_tasks))
            # data_tsk.setdefault(user_id, lexicon['user_account'])

            # создать запись ПД
            print(user_id, 'pd created')
            info = template_pd.user_pd
            info['referral'] = referral
            info['first_start'] = msg_time
            info['tg_username'] = message.from_user.username
            info['tg_fullname'] = message.from_user.full_name
            info['lang_tg'] = message.from_user.language_code
            info['lang'] = message.from_user.language_code
            print(info)

            # сохранить новые данные
            data_inf.setdefault(user_id, info)
            with open(baza_info, 'w', encoding='utf-8') as f:
                json.dump(data_inf, f, indent=2, ensure_ascii=False)
            data_inf.setdefault(user_id, info)
        else:
            referral = data_inf[user].get('referral', '?')

        with open(baza_task, 'w', encoding='utf-8') as f:
            json.dump(data_tsk, f, indent=2, ensure_ascii=False)

        # приветствие и выдача политики
        match language:
            case 'ru':
                await message.answer(text=lexicon['start'], reply_markup=keyboards.keyboard_privacy_ru, parse_mode='HTML')
            case 'en':
                await message.answer(text=lexicon['start'], reply_markup=keyboards.keyboard_privacy_en, parse_mode='HTML')
        await message.answer(text=lexicon['pol_agree'], reply_markup=keyboards.keyboard_ok)

        # бот переходит в состояние ожидания согласия с политикой
        await state.set_state(FSM.policy)
        # сообщить админу, кто стартанул бота
        alert = f'➕ user {len(data_tsk)} {contact_user(user)} from: {referral}'
        for i in admins:
            await bot.send_message(
                text=alert, chat_id=i, disable_notification=True, parse_mode='HTML')
                # text=f'➕ user {len(data_tsk)} id{user.id} {user.full_name} @{user.username} from: {referral}', chat_id=i, disable_notification=True)

        # логи
        await log(logs, 'logs',
            f'{msg_time}, {user.full_name}, @{user.username}, id {user.id}, {user.language_code}, start={referral}')
        await log(logs, user.id, f'/start={referral}')

    # # если это работник
    # elif user_id in admins+validators:
    #     await message.answer(text=lexicon['start'], reply_markup=keyboards.keyboard_privacy_ru, parse_mode='HTML')
    #     await message.answer(text=lexicon['pol_agree'], reply_markup=keyboards.keyboard_ok)
    #     await state.set_state(FSM.policy)

    # если юзер уже в БД и просто снова нажал старт
    else:
        match language:
            case 'ru':
                await message.answer(text=lexicon['start'], reply_markup=keyboards.keyboard_privacy_ru, parse_mode='HTML')
            case 'en':
                await message.answer(text=lexicon['start'], reply_markup=keyboards.keyboard_privacy_en, parse_mode='HTML')
        await message.answer(text=lexicon['pol_agree'], reply_markup=keyboards.keyboard_ok)
        await state.set_state(FSM.policy)
        # await bot.send_message(text=lexicon[''], chat_id=user_id, reply_markup=keyboards.keyboard_user)
        await log(logs, user.id, f'start_again')


# команда /next - дать юзеру след задание
@router.message(Command(commands=['next']), ~StateFilter(FSM.policy))
async def next_cmnd(message: Message, bot: Bot, state: FSMContext):
    user = str(message.from_user.id)
    await log(logs, user, '/next')
    language = await get_pers_info(user=user, key='lang')
    lexicon = load_lexicon(language)

    # Найти первое доступное задание, т.е. без статуса accept или review, и отправить юзеру
    file_num = find_next_task(user)
    # если задания кончились или не начались
    if not file_num:
        await bot.send_message(chat_id=user, text=lexicon['no_more'], parse_mode='HTML')
        return

    # если нашлись
    with open(tasks_tsv.format(language), 'r', encoding='utf-8') as f:
        next_task = []
        for line in f.readlines():
            split_line = line.split('\t')
            if split_line[0] == file_num:
                next_task = split_line
                break

    print(next_task)
    # текст задания
    task_message = get_task_message(next_task)
    # отправка задания юзеру
    m = await bot.send_message(chat_id=user, text=task_message, parse_mode='HTML')
    await state.set_state(FSM.ready_for_next)


# юзер согласен с политикой ✅
@router.callback_query(F.data == "ok_pressed", StateFilter(FSM.policy))
async def privacy_ok(callback: CallbackQuery, bot: Bot, state: FSMContext):
    user = callback.from_user
    await log(logs, user.id, 'privacy_ok')
    language = await get_pers_info(user=str(user.id), key='lang')
    lexicon = load_lexicon(language)

    # выдать инструкцию и примеры
    msg_to_pin = await bot.send_message(text=lexicon['instruct1'], chat_id=user.id, parse_mode='HTML')
    await bot.send_message(text=f"{lexicon['instruct2']}\n\n{lexicon['full_hd']}", chat_id=user.id, parse_mode='HTML',
                           disable_web_page_preview=True, reply_markup=keyboards.keyboard_user)
    # хороший пример
    url = 'https://s3.amazonaws.com/trainingdata-data-collection/dima/Innodata/inod_exmpl.jpg'
    await bot.send_photo(chat_id=user.id, photo=URLInputFile(url), caption=lexicon['example'])

    # плохой пример
    # url = 'https://s3.amazonaws.com/trainingdata-data-collection/dima/Innodata/inod_exmpl.jpg'
    # await bot.send_photo(chat_id=user.id, photo=URLInputFile(url_exmpl), caption=lexicon['example'])

    # закреп
    await bot.pin_chat_message(message_id=msg_to_pin.message_id, chat_id=user.id, disable_notification=True)
    await state.clear()


# если юзер пишет что-то не нажав ✅
@router.message(StateFilter(FSM.policy))
async def privacy_missing(msg: Message):
    language = await get_pers_info(user=str(msg.from_user.id), key='lang')
    lexicon = load_lexicon(language)
    await log(logs, msg.from_user.id, 'privacy_missing')
    await msg.answer(text=lexicon['privacy_missing'])


# юзер отправил альбом: не принимается
@router.message(F.media_group_id)
async def alb(msg: Message):
    # чтобы не отвечать на каждое фото из одного альбома
    global last_group_id
    if msg.media_group_id == last_group_id:
        return
    else:
        last_group_id = msg.media_group_id

    user = str(msg.from_user.id)
    language = await get_pers_info(user=user, key='lang')
    lexicon = load_lexicon(language)
    await log(logs, user, 'album')
    await msg.reply(lexicon['album'])


# юзер отправил сжатый файл: не принимается
@router.message(F.content_type.in_({'photo', 'video'}))
async def compressed_pic(msg: Message):
    language = await get_pers_info(user=str(msg.from_user.id), key='lang')
    lexicon = load_lexicon(language)
    await log(logs, msg.from_user.id, 'compressed_file')
    await msg.reply(lexicon['full_hd'], parse_mode='HTML')


# юзер отправил норм файл
@router.message(or_f(F.text == '#', F.content_type.in_({'document'})), StateFilter(FSM.ready_for_next))
async def file_ok(msg: Message, bot: Bot, state: FSMContext):
    user = str(msg.from_user.id)
    language = await get_pers_info(user=str(msg.from_user.id), key='lang')
    lexicon = load_lexicon(language)

    if msg.document:
        file_id = msg.document.file_id
        # отклонить если файл тяжелее 50 мб
        size = msg.document.file_size
        if size > 50_000_000:
            await log(logs, user, f'size {size}')
            await msg.answer(text=lexicon['big_file'])
            return

        # отклонить если файл меньше 2 мб
        if size < 2_000_000:
            megabyte = round(size/1_000_000, 2)
            await log(logs, user, f'size {size}')
            await msg.answer(text=lexicon['small_file'].format(megabyte))
            return

        # отклонить если горизонтальная съемка (если у файла есть thumbnail, то можно посчитать его размеры)
        if msg.document.thumbnail:
            width = msg.document.thumbnail.width
            height = msg.document.thumbnail.height
            if width >= height:
                await log(logs, user, f'wrong orient')
                # print('wrong orient', f'width: {width}, height: {height}')
                await msg.answer(text=lexicon['vert'])
                return
    else:
        # болванка для тестирования
        # file_id = 'BQACAgUAAxkBAAIKk2V4SQEHNsyv6Y0g4vDic0vjMUckAAKSDAACVu3AV-SnwgzXyLaBMwQ'
        file_id = 'test'

    # чтение БД
    with open(baza_task, 'r', encoding='utf-8') as f:
        data = json.load(f)
    with open(baza_info, 'r', encoding='utf-8') as f:
        data_inf = json.load(f)

    # плюсануть кол-во отправленных
    x = await get_pers_info(user=user, key='total_sent')
    await set_pers_info(user=user, key='total_sent', val=x+1)

    # вычисляем, какое было прислано задание
    sent_file = find_next_task(user)
    await log(logs, user, f'SENT_{sent_file}')

    # меняем статус задания на 'review' и сохраняем file_id
    data[user][sent_file] = ('review', file_id)
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
        await msg.reply(text=lexicon['receive'].format(sent_file[-2:]), reply_markup=keyboards.keyboard_user)

    # если был отправлен последний файл, то они идут на проверку
    else:
        # кто будет валидировать
        validator = None
        if validators:
            if len(validators) == 2:
                # если два валидатора, то проверка назначается одному из них в зависимости от последней цифры id юзера
                index = int(user[-1]) % 2  # проверка четности
                validator = validators[index]
            else:
                validator = validators[0]

        # прочитать перс данные из бд
        with open(baza_info, 'r', encoding='utf-8') as f:
            data_inf = json.load(f)
        # if isinstance(data_inf[user], list):  # из старой версии
        #     data_inf[user] = data_inf[user][0]
        if data_inf.get(user, None):
            ref = data_inf[user].get('referral', None)
        else:
            ref = None

        # список [('тг-айди файла', 'текст задания'), (...]
        output = await send_files(user, 'review')

        # уведомить юзера, админов, внести в логи и в консоль
        alert = f'🆕 Юзер отправил {len(output)} файлов - {contact_user(msg.from_user)} ref: {ref}'
        await msg.reply(lexicon['all_sent'])
        await log(logs, user, f'SENT_ALL_FILES: {len(output)}')
        for i in admins + [validator]:
            if i:
                print('to', i)
                await bot.send_message(chat_id=i, text=alert, parse_mode='HTML')

        # # Отправить файлЫ на проверку одному валидатору если он есть, иначе - первому админу
        # send_to = validator if validator else admins[0]
        # adm_lexicon = __import__('lexic.adm', fromlist=['']).lexicon
        # for i in output:
        #     file_id, task_message = i
        #     if file_id == 'test':
        #         await bot.send_message(chat_id=send_to, text=file_id+'\n'+task_message, parse_mode='HTML', disable_notification=True)
        #     else:
        #         await bot.send_document(chat_id=send_to, document=file_id, caption=task_message, parse_mode='HTML', disable_notification=True)
        #
        # # сообщение с кнопками (✅принять или нет❌) - если нет валидатора, то кнопки получит админ
        # await bot.send_message(chat_id=send_to, text=f'{adm_lexicon["adm_review"]} id{user}?\n{msg.from_user.full_name}'
        #                        f' @{msg.from_user.username} ref: {ref}', reply_markup=keyboards.keyboard_admin)
        # await log(logs, user, 'review files received')


# юзер что-то пишет
@router.message(~Access(admins+validators), F.content_type.in_({'text'}))
async def usr_txt2(msg: Message, bot: Bot):
    await log(logs, msg.from_user.id, f'msg_to_admin: {msg.text}')
    adm_lexicon = __import__('lexic.adm', fromlist=['']).lexicon

    # показать админам
    for i in admins:
        await bot.send_message(chat_id=i, text=f'{adm_lexicon["msg_to_admin"]} {contact_user(msg.from_user)}: \n\n{msg.text}', parse_mode='HTML')
