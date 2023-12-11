adm_lexicon: dict[str:str] = {
    # admin
    'adm_review': 'Принять ВСЕ файлы от',
    'msg_to_admin': '📩 Сообщение от',
    'deleted': 'Удалено, вот бекап до удаления',
    'adm_reject': '',
    'wrong_rej_form': 'Неверный формат: каждая новая строка должна начинаться с числа и '
                      'оканчиваться переносом строки.\nНапиши причину отказа снова.',
    'adm_help': 'Команды, доступные админу (123 заменить на нужный айди слитно):'
                '\n\n- Получить файлы юзера (фото и видео), вместо status указать в каком статусе нужны файлы - review, accept или reject:'
                '\n<code>files id123 status</code>'
                '\n\n- Отправить "Сообщение от администратора" юзеру по айди:'
                '\n<i>Ответить на любое сообщение, в котором есть айди (сообщ. от бота, или написать самому <code>id123</code> и ответить на свое сообщение)</i>'
                '\n\n- Принять файлы без кнопок:'
                '\n<code>accept id123</code>'
                '\n\n- Отклонить файлы без кнопок:'
                '\n<code>reject id123</code> (далее ответом написать причины отказа)'
                '\n\n- Получить tsv со ссылками на скачивание всего, что юзер скинул'
                '\n<code>tsv id123</code>'
                '\n\n- Получить базы данных (это 4 разные  команды)'
                '\n<code>send bd / send logs / send info / send all</code>'
                '\n\n- Количество админов: {}, валидаторов: {}',

    # шаблоны
    'user_pd': {
        "referral": None,
        "first_start": None,
        "accept_date": None,
        "tg_username": None,
        "tg_fullname": None,
        "lang_tg": None,
        "lang": None,
        "tasks": None,
        "reject": 0,
        "total_sent": 0,
        "last_sent": None,
        "status": None,
        "fio": None,
        "age": None,
        "gender": None,
        "country": None,
        "race": None,
    },

    'log': 'inn',

}
