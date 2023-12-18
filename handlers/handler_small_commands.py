from aiogram import Router, Bot, F
from aiogram.filters import Command, CommandStart, StateFilter, CommandObject
from bot_logic import *
import keyboards
from settings import *
from lexic import ru, en, adm
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import CallbackQuery, Message, URLInputFile


# Инициализация
router: Router = Router()


# команда /help
@router.message(Command(commands=['help']))
async def comm(msg: Message):
    user = str(msg.from_user.id)
    language = await get_pers_info(user=user, key='lang')
    lexicon = load_lexicon(language)
    await log(logs, user, msg.text)

    if user in admins + validators:
        adm_lexicon = __import__('lexic.adm', fromlist=['']).lexicon
        await msg.answer(adm_lexicon['adm_help'].format(len(admins), len(validators)), parse_mode='HTML')
    else:
        await msg.answer(lexicon['help'])


# команда /language
@router.message(Command(commands=['language']))
async def comm(msg: Message):
    user = str(msg.from_user.id)
    await msg.answer('Выберите язык / Choose language', reply_markup=keyboards.keyboard_lang)
    await log(logs, user, msg.text)


# юзер выбрал язык
@router.callback_query(lambda x: x.data in langs)
async def lng(msg: CallbackQuery, bot: Bot):
    user = str(msg.from_user.id)
    language = msg.data

    # сохранить значение
    await set_pers_info(user=user, key='lang', val=language)

    language = await get_pers_info(user=user, key='lang')
    lexicon = load_lexicon(language)

    # уведомить о смене
    await bot.send_message(chat_id=user, text=lexicon["lang_ok"].format(language.upper()))
    await log(logs, user, f'language: {language}')


# команда /instruct
@router.message(Command(commands=['instruct']))
async def comm(msg: Message, bot: Bot):
    user = str(msg.from_user.id)
    await log(logs, user, msg.text)
    language = await get_pers_info(user=user, key='lang')
    lexicon = load_lexicon(language)
    # текст
    # выдать инструкцию и примеры
    msg_to_pin = await bot.send_message(text=lexicon['instruct1'], chat_id=user, parse_mode='HTML')
    await bot.send_message(text=f"{lexicon['instruct2']}\n\n{lexicon['full_hd']}", chat_id=user, parse_mode='HTML',
                           disable_web_page_preview=True, reply_markup=keyboards.keyboard_user)
    url_exmpl = 'https://s3.amazonaws.com/trainingdata-data-collection/dima/Innodata/inod_exmpl.jpg'
    await bot.send_photo(chat_id=user, photo=URLInputFile(url_exmpl), caption=lexicon['example'])
    # закреп
    await bot.pin_chat_message(message_id=msg_to_pin.message_id, chat_id=user, disable_notification=True)


# команда /status - показать юзеру статус его заданий
@router.message(Command(commands=['status']))
async def process_status_command(msg: Message, bot: Bot):
    user = str(msg.from_user.id)
    await log(logs, user, '/status')
    language = await get_pers_info(user=user, key='lang')
    lexicon = load_lexicon(language)
    stat = get_status(user)
    # await msg.answer(f'Ваши задания:\n\n{stat}', parse_mode='HTML')
    await msg.answer(lexicon['status'].format(stat['acc'], stat['rej'], stat['rev'], stat['non'], ), parse_mode='HTML')


# команда /next - дать юзеру след задание
@router.message(Command(commands=['next']), ~StateFilter(FSM.policy))
async def next_cmnd(message: Message, bot: Bot, state: FSMContext):
    user = str(message.from_user.id)
    await log(logs, user, '/next')
    language = await get_pers_info(user=user, key='lang')
    if language not in langs:
        language = 'en'
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
            splited_line = line.split('\t')
            if splited_line[0] == file_num:
                next_task = splited_line
                break

    print(next_task)
    # текст задания
    task_message = get_task_message(next_task)
    # отправка задания юзеру
    await bot.send_message(chat_id=user, text=task_message, parse_mode='HTML')
    await state.set_state(FSM.ready_for_next)


# команда /cancel - отменить отправленный файл
@router.message(Command(commands=['cancel']))
async def cancel_command(msg: Message, bot: Bot, state: FSMContext):
    user = str(msg.from_user.id)
    language = await get_pers_info(user=user, key='lang')
    lexicon = load_lexicon(language)

    await log(logs, user, '/cancel')
    with open(baza_task, 'r') as f:
        data = json.load(f)
    if user in data:
        # проверить, не отправлены ли все файлы уже на проверку
        statuses = set(data[user][i][0] for i in data[user])
        if 'status' in statuses or 'reject' in statuses:
            await bot.send_message(chat_id=user, text=lexicon['cancel'])
            # Бот ожидает номера заданий
            await state.set_state(FSM.cancelation)
        else:
            await bot.send_message(chat_id=user, text=lexicon['cancel_fail'])
    else:
        await bot.send_message(chat_id=user, text=lexicon['cancel_fail'])


# удаление отмененных файлов
@router.message(F.content_type.in_({'text'}), StateFilter(FSM.cancelation))
async def cancel(msg: Message, bot: Bot, state: FSMContext):
    user = str(msg.from_user.id)
    language = await get_pers_info(user=user, key='lang')
    lexicon = load_lexicon(language)

    # обработать номера заданий
    nums_to_cancel = []
    for num in msg.text.split():
        #  проверка правильности ввода
        if num.isnumeric() and len(num) == 2:
            nums_to_cancel.append(num)

        # если номера указаны неверно
        else:
            await msg.reply(lexicon['cancel_wrong_form'])
            await log(logs, user, 'cancel_wrong_form')
            return

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

        # уведомить юзера о результате
        if cancelled:
            await msg.reply(text=lexicon['cancel_ok']+', '.join(cancelled))
        if not_found:
            await msg.answer(text=lexicon['cancel_not_found']+', '.join(not_found))
        await state.clear()
        await log(logs, user, f'cancelled {cancelled}, not found {not_found}')

