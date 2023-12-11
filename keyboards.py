from aiogram.types import KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from bot_logic import get_pers_info, load_lexicon
from pprint import pprint

# кнопки как опция ответа
# button_start = KeyboardButton(text='/start')
# button_help = KeyboardButton(text='/help')
button_next = KeyboardButton(text='/next')
button_stat = KeyboardButton(text='/status')

# privacy policy
privacy_en: str = "https://drive.google.com/file/d/1RddAFv77L6sL2tvPJBFxA5eI-Zb9Z1AC/view"
privacy_ru: str = "https://docs.google.com/document/d/1s9LkBxFPAuKnFxFWKcSNzXvMUG_2hSq7xehG8gZbKt4/edit"
url_button_ru = InlineKeyboardButton(text='Политика конфиденциальности', url=privacy_ru)
url_button_en = InlineKeyboardButton(text='Privacy policy', url=privacy_en)
privacy_ok = InlineKeyboardButton(text='✅', callback_data='ok_pressed')

# языки
lang_rus: InlineKeyboardButton = InlineKeyboardButton(text='🇷🇺 Русский', callback_data='ru')
lang_eng: InlineKeyboardButton = InlineKeyboardButton(text='🇬🇧 English', callback_data='en')

# этносы
race_euro: InlineKeyboardButton = InlineKeyboardButton(text='European / Европеец', callback_data='euro')
race_asia: InlineKeyboardButton = InlineKeyboardButton(text='Asian / Азиат', callback_data='asia')
race_afro: InlineKeyboardButton = InlineKeyboardButton(text='African / Африканец', callback_data='afro')
race_indi: InlineKeyboardButton = InlineKeyboardButton(text='Indian / Индиец', callback_data='indi')
race_other: InlineKeyboardButton = InlineKeyboardButton(text='Other / Другое', callback_data='other')

# принять или отклонить файл
admin_ok: InlineKeyboardButton = InlineKeyboardButton(text='✅', callback_data='admin_ok')
admin_no: InlineKeyboardButton = InlineKeyboardButton(text='❌', callback_data='admin_no')

# списки кнопок
vars_copy = vars().copy()
race_btn_list = list([vars_copy[i]] for i in vars_copy if i.startswith('race'))
lang_btn_list = list([vars_copy[i]] for i in vars_copy if i.startswith('lang'))

# клавиатуры из таких кнопок
keyboard_privacy_ru = InlineKeyboardMarkup(inline_keyboard=[[url_button_ru]])
keyboard_privacy_en = InlineKeyboardMarkup(inline_keyboard=[[url_button_en]])
keyboard_ok = InlineKeyboardMarkup(inline_keyboard=[[privacy_ok]])
keyboard_admin = InlineKeyboardMarkup(inline_keyboard=[[admin_ok], [admin_no]])
keyboard_user = ReplyKeyboardMarkup(keyboard=[[button_next], [button_stat]], resize_keyboard=True)
keyboard_race = InlineKeyboardMarkup(inline_keyboard=race_btn_list, resize_keyboard=True)
keyboard_lang = InlineKeyboardMarkup(inline_keyboard=lang_btn_list, resize_keyboard=True)
