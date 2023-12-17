from aiogram.types import KeyboardButton, InlineKeyboardButton as Button, InlineKeyboardMarkup as Markup, ReplyKeyboardMarkup
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
url_button_ru = Button(text='Политика конфиденциальности', url=privacy_ru)
url_button_en = Button(text='Privacy policy', url=privacy_en)
url_button_id = Button(text='Privacy policy', url=privacy_en)
privacy_ok = Button(text='✅', callback_data='ok_pressed')

# языки
lang_rus = Button(text='🇷🇺 Русский', callback_data='ru')
lang_eng = Button(text='🇬🇧 English', callback_data='en')
lang_ind = Button(text='🇮🇩 Indonesia', callback_data='id')

# этносы
race_euro = Button(text='European / Европеец', callback_data='euro')
race_asia = Button(text='Asian / Азиат', callback_data='asia')
race_afro = Button(text='African / Африканец', callback_data='afro')
race_indi = Button(text='Indian / Индиец', callback_data='indi')
race_other = Button(text='Other / Другое', callback_data='other')

# принять или отклонить файл
admin_ok = Button(text='✅', callback_data='admin_ok')
admin_no = Button(text='❌', callback_data='admin_no')

# списки кнопок
vars_copy = vars().copy()
race_btn_list = list([vars_copy[i]] for i in vars_copy if i.startswith('race'))
lang_btn_list = list([vars_copy[i]] for i in vars_copy if i.startswith('lang'))

# клавиатуры из таких кнопок
keyboard_privacy_ru = Markup(inline_keyboard=[[url_button_ru]])
keyboard_privacy_en = Markup(inline_keyboard=[[url_button_en]])
keyboard_privacy_id = Markup(inline_keyboard=[[url_button_id]])
keyboard_ok = Markup(inline_keyboard=[[privacy_ok]])
keyboard_admin = Markup(inline_keyboard=[[admin_ok], [admin_no]])
keyboard_user = ReplyKeyboardMarkup(keyboard=[[button_next], [button_stat]], resize_keyboard=True)
keyboard_race = Markup(inline_keyboard=race_btn_list, resize_keyboard=True)
keyboard_lang = Markup(inline_keyboard=lang_btn_list, resize_keyboard=True)
