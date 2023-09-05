from settings import mngr

# RU: dict[str, dict[str, str]] = {}
lex: dict = {
        # admin
        'adm_review': 'Принять ВСЕ файлы от',
        'msg_to_admin': 'Сообщение от',
        'msg_from_admin': 'Сообщение от администратора',
        # users
        'help': f'Если что-то не работает, нажмите /start или напишите {mngr}',

        'cancel': 'Укажите через пробел номера заданий, для которых вы хотите отменить отправку файла. '
                  'Можно указать только те задания, которые сейчас на проверке. Пример сообщения:'
                  '\n\n01 02 16',
        'cancel_ok': 'Ок. Удалены ваши файлы из заданий: ',
        'cancel_not_found': 'Задания под следующими номерами либо уже нами приняты, либо вы их не присылали: ',
        'cancel_wrong_form': 'Неверный формат. Я ожидаю номера заданий через пробел.',

        'no_ref': 'Ссылка недействительна. Спросите ссылку у того, кто привел вас к нам.',
        'start': 'Привет!\n\n'
                 'Мы собираем фото и видео для <b>обучения нейросети</b> распознавать эмоции, жесты и прочие действия.\n\n'
                 'Вам предстоит выполнить 65 заданий. В каждом будет дан пример в виде ссылки на файл из Гугл-диска и краткое описание, '
                 'что нужно заснять (<a href="https://drive.google.com/drive/folders/1izl1XW_behpwcF3TQs8yTRTcok9Og_WT">тут папка</a> со всеми заданиями, '
                 'далее вы будете получать по порядку, по одному). '
                 'Когда вы выполните все 65 заданий - ваши файлы будут отправлены нам <b>на проверку</b>.\n\n'
                 'Если задание будет выполнено не правильно - мы его отклоним и оно будет вам доступно для повторного выполнения. '
                 'Когда все 65 заданий будут успешно приняты - вы получите уведомление, которое нужно показать тому, кто привел вас к боту. После этого вы получите <b>оплату</b>.\n'
                 '\nМожете нажать:'
                 '\n/next для выдачи следующего задания'
                 '\n/status для просмотра статуса ваших заданий'
                 '\n/help чтобы сообщить о проблемах с ботом.'
                 '\n\nДля выполнения задания приготовьте: Большие наушники (либо головной убор), две пары очков (с прозрачными линзами и солнцезащитные), '
                 'два телефона, бутылка воды, еда, письменная ручка, медицинская маска.'
                 '\n\nПрежде чем продолжить, пожалуйста, ознакомьтесь с нашей <b>политикой конфиденциальности</b> и нажмите кнопку ✅.',

        'start_again': 'Вы уже числитесь в базе данных, можете продолжать задания: /next',
        'ban': 'Вам заблокирован доступ к заданиям.',
        'privacy_missing': 'Нажмите галочку, чтобы согласиться с политикой конфиденциальности.',
        'fio': 'Укажите ваше ФИО',
        'age': 'Укажите ваш возраст',
        'gender': 'Укажите ваш пол',

        'instruct1': 'Спасибо! Теперь ознакомьтесь с <b>требованиями</b> к отправляемым файлам:\n\n'
                     '- Убедитесь, что объектив вашей камеры чист\n'
                     '- Нельзя снимать видео, <b>держа телефон в руке</b>. Поставьте его ровно на что-нибудь, чтобы избежать тряски\n'
                     '- Каждое видео должно длиться от 5 секунд\n'
                     '- Нельзя прикрывать никакую часть лица, даже своими пальцами (если иное не показано в примере)\n'
                     '- Лицо должно быть хорошо видно, на свету, не обрезано\n'
                     '- Все видео и фото обязательно должны быть <b>ГОРИЗОНТАЛЬНЫЕ</b> (как в примерах)\n'
                     '- Выполняйте задания точь в точь, как в примере (Если в примере человек поворачивает голову '
                     'в свое лево, то вы поворачиваете также в <b>свое лево</b>)\n'
                     '- Если в примере меняется задний фон и одежда, то вам требуется сделать то же самое\n',
        'full_hd': 'Нужно отправить файл <b>без сжатия</b>. Если не знаете как, то'
                   ' <a href="https://www.youtube.com/embed/qOOMNJ0gIss">посмотрите пример</a> (9 сек).',
        'instruct2': 'Можете приступать к выполнению - нажмите команду /next для получения следующего задания. ',

        'album': 'Отправляйте файлы по одному, не группой',
        'receive': 'Получен файл для задания {}.\nНажмите /next для следующего задания',

        'all_sent': 'Спасибо! Вы отправили все нужные файлы. Ожидайте проверки вашей работы.',
        'no_more': 'Нет доступных заданий',
        'reject': 'Мы проверили вашу работу. К сожалению, часть файлов не прошла проверку. Ознакомьтесь с нашими '
                  'комментариями и нажмите команду /next для получения задания.',
        'all_approved': 'Ура! Все ваши файлы приняты, благодарим за сотрудничество. '
                        'Для получения оплаты просто перешлите это сообщение тому, кто привел вас к нам. Ваш айди: ',

        'user_account': {
                        "file01": ['status', 'file'],
            "file02": ['status', 'file'],
            "file03": ['status', 'file'],
            "file04": ['status', 'file'],
            "file05": ['status', 'file'],
            "file06": ['status', 'file'],
            "file07": ['status', 'file'],
            "file08": ['status', 'file'],
            "file09": ['status', 'file'],
            "file10": ['status', 'file'],
            "file11": ['status', 'file'],
            "file12": ['status', 'file'],
            "file13": ['status', 'file'],
            "file14": ['status', 'file'],
            "file15": ['status', 'file'],
            "file16": ['status', 'file'],
            "file17": ['status', 'file'],
            "file18": ['status', 'file'],
            "file19": ['status', 'file'],
            "file20": ['status', 'file'],
            "file21": ['status', 'file'],
            "file22": ['status', 'file'],
            "file23": ['status', 'file'],
            "file24": ['status', 'file'],
            "file25": ['status', 'file'],
            "file26": ['status', 'file'],
            "file27": ['status', 'file'],
            "file28": ['status', 'file'],
            "file29": ['status', 'file'],
            "file30": ['status', 'file'],
            "file31": ['status', 'file'],
            "file32": ['status', 'file'],
            "file33": ['status', 'file'],
            "file34": ['status', 'file'],
            "file35": ['status', 'file'],
            "file36": ['status', 'file'],
            "file37": ['status', 'file'],
            "file38": ['status', 'file'],
            "file39": ['status', 'file'],
            "file40": ['status', 'file'],
            "file41": ['status', 'file'],
            "file42": ['status', 'file'],
            "file43": ['status', 'file'],
            "file44": ['status', 'file'],
            "file45": ['status', 'file'],
            "file46": ['status', 'file'],
            "file47": ['status', 'file'],
            "file48": ['status', 'file'],
            "file49": ['status', 'file'],
            "file50": ['status', 'file'],
            "file51": ['status', 'file'],
            "file52": ['status', 'file'],
            "file53": ['status', 'file'],
            "file54": ['status', 'file'],
            "file55": ['status', 'file'],
            "file56": ['status', 'file'],
            "file57": ['status', 'file'],
            "file58": ['status', 'file'],
            "file59": ['status', 'file'],
            "file60": ['status', 'file'],
            "file61": ['status', 'file'],
            "file62": ['status', 'file'],
            "file63": ['status', 'file'],
            "file64": ['status', 'file'],
            "file65": ['status', 'file']
                      },
        'tasks': {
            # Behavior:
            'file01': '<a href="https://drive.google.com/file/d/14bYM2Y_N4SFLIXsyJ6fpLPWX1MSh7Zqd/view?usp=drive_link">Задание 01:</a> Drink\n(Для записи видео потребуется бутылка воды)\nСнимите как вы пьете воду из бутылки',
            'file02': '<a href="https://drive.google.com/file/d/19L-ac1bbe6kh7cgxiDyUO8MET7VX6Jpk/view?usp=drive_link">Задание 02:</a> Eat-food\n(Требуется что-то из еды, по типу снэка без упаковки)\nСнимите как вы едите что-то, например, любой снэк',
            'file03': '<a href="https://drive.google.com/file/d/1D9XJL0fS9nZ4OqQ-D_Csgr6dnk5Kf-ol/view?usp=drive_link">Задание 03:</a> Play-phone\n(Для записи видео потребуется второй телефон)\nСнимите как вы печатаете на телефоне. При этом должны быть видны пальцы.',
            'file04': '<a href="https://drive.google.com/file/d/1mtSy2ShtvrTmAtOpEINJeTdYhLDlgdz9/view?usp=drive_link">Задание 04:</a> Turn-pen\n(Для записи видео потребуется письменная ручка)\nСнимите как вы крутите ручку в левой руке',
            # Body Pose
            'file05': '<a href="https://drive.google.com/file/d/1VZI4pQF6gd3szi1xmoDrwO5Sr80vgyB5/view?usp=drive_link">Задание 05:</a> Body-forth-back\nСнимите как вы наклоняйтесь вперед-назад два раза',
            'file06': '<a href="https://drive.google.com/file/d/1lmgJm0muj2fJZ1YaVpxBsgAx801Kxiae/view?usp=drive_link">Задание 06:</a> Body-left-right\nСнимите как вы наклоняйте тело влево-вправо',
            'file07': '<a href="https://drive.google.com/file/d/1tpcY-LKjf5EMOw6Aao5iuSEZxQNMPBaB/view?usp=drive_link">Задание 07:</a> Body-rotate\nСнимите как вы поворачивайте тело вместе с головой влево-вправо',
            'file08': '<a href="https://drive.google.com/file/d/14gxs3K9uiUr2CWIJ_QTzuoINpcahAhWA/view?usp=drive_link">Задание 08:</a> Fold-arm\nСнимите как вы складываете руки',
            'file09': '<a href="https://drive.google.com/file/d/1DhUO-2aq-VD3-RI8zYHdicbQBBHF5qmw/view?usp=drive_link">Задание 09:</a> Shrug-shoulder\nСнимите как вы пожимайте плечами',
            'file10': '<a href="https://drive.google.com/file/d/10bRmPqkIOGUlmMlCag3mu9olMVzrNJJj/view?usp=drive_link">Задание 10:</a> Strech-arm\nСнимите как вы тянитесь',
            'file11': '<a href="https://drive.google.com/file/d/1nfVGka8x-LnMxLXDKqnVA2szfO8_htB7/view?usp=drive_link">Задание 11:</a> Up-down\nСнимите как вы встаете и садитесь',
            # Expression:
            'file12': '<a href="https://drive.google.com/file/d/1D9Shqnc-GT4pRvIn7YtCh_JD1or2tn9u/view?usp=drive_link">Задание 12:</a> Amazed\nВ этом видео важна эмоция\nСнимите ваше удивление',
            'file13': '<a href="https://drive.google.com/file/d/1Asg0zzVXKCTvBGi49qg8t51HWKTnrVi3/view?usp=drive_link">Задание 13:</a> Anger\nВ этом видео важна эмоция\nСнимите как вы злитесь',
            'file14': '<a href="https://drive.google.com/file/d/1FtHT22RWF8QYwLfRTAT_PXYhVUPuGygO/view?usp=drive_link">Задание 14:</a> Disgusted\nВ этом видео важна эмоция\nСнимите вашу эмоцию отвращения',
            'file15': '<a href="https://drive.google.com/file/d/1zjPBk8CD8hyO7iOsS6FPgh6OATp5AtIT/view?usp=drive_link">Задание 15:</a> Happy\nВ этом видео важна эмоция\nСнимите эмоцию счастья',
            'file16': '<a href="https://drive.google.com/file/d/1rfjchs4I_EAROFdOSeRvhovlZFpAJN6i/view?usp=drive_link">Задание 16:</a> Normal\nВ этом видео важна эмоция\nСнимите ваше обычное лицо',
            'file17': '<a href="https://drive.google.com/file/d/1aIlIanjEzkIBA0TyeOv7aHr1OxToBlEq/view?usp=drive_link">Задание 17:</a> Sad\nВ этом видео важна эмоция\nСнимите эмоцию грусти',
            'file18': '<a href="https://drive.google.com/file/d/1EZqQZCf1Qeq8dHgLOJYJLGUUHazJLLep/view?usp=drive_link">Задание 18:</a> Scared\nВ этом видео важна эмоция\nСнимите ваш испуг',
            # Face Pose vid:
            'file19': '<a href="https://drive.google.com/file/d/1IZtDmoNUsYL0N4PF3Ob-c9kjASEQnr8F/view?usp=drive_link">Задание 19:</a> Deep-breath\nСнимите ваш глубокий вдох и выдох',
            'file20': '<a href="https://drive.google.com/file/d/1BC4hbSFc5_ijQjhpX_3f1y8E0KOXSRNU/view?usp=drive_link">Задание 20:</a> Eye-closed\nСнимите как вы зажмуриваетесь',
            'file21': '<a href="https://drive.google.com/file/d/17mOicp3XE2VU8dioQiwPGzSpkBClKQTN/view?usp=drive_link">Задание 21:</a> Eye-roll\nПовторите движение зрачков в этом видео',
            'file22': '<a href="https://drive.google.com/file/d/161g32put2RKzyqRvTL1CMj5YdKy2uuVZ/view?usp=drive_link">Задание 22:</a> Eye-stare\nПоднимите брови и откройте глаза',
            'file23': '<a href="https://drive.google.com/file/d/141HNzEVt3ACcu48bIWUHALD7GNfcFMU2/view?usp=drive_link">Задание 23:</a> Mouth-open\nОткройте широко рот ',
            'file24': '<a href="https://drive.google.com/file/d/1yA-FAUAFVaAHOxhh0DSSvt5Fvw8yirb5/view?usp=drive_link">Задание 24:</a> Mouth-pout\nСделайте губы трубочкой ',
            'file25': '<a href="https://drive.google.com/file/d/1laBs74n9RdwIwFksIYYdiv80uubIBBmB/view?usp=drive_link">Задание 25:</a> Mouth-pucker\nВтяните губы, как на видео',
            'file26': '<a href="https://drive.google.com/file/d/1yXJrhYzs6UH8FnEEBpYmvbNrOYT6I9xs/view?usp=drive_link">Задание 26:</a> Put-tongue\nОткройте рот и покажите язык',
            'file27': '<a href="https://drive.google.com/file/d/1Q-E8HOdpRsHnjRlhUkN6N9UNvz_Ed1Zt/view?usp=drive_link">Задание 27:</a> Touch-chin\nПотрогайте подбородок',
            'file28': '<a href="https://drive.google.com/file/d/13i8iOrT4nAqAape_g2LvpC8INX7_L9kB/view?usp=drive_link">Задание 28:</a> Touch-ear\nПотрогайте ухо',
            'file29': '<a href="https://drive.google.com/file/d/1Amq1N1O_vZQC1fR5qfE_1_VoQLuZFkZs/view?usp=drive_link">Задание 29:</a> Touch-eye\nПотрогайте глаза',
            'file30': '<a href="https://drive.google.com/file/d/1xEoSgXtJOsmAlDipk-0hGJPd6jfLN3O8/view?usp=drive_link">Задание 30:</a> Touch-face\nПотрогайте щеки',
            'file31': '<a href="https://drive.google.com/file/d/1vphpWl3O2K0J8lzIlTAWsv3rcJqGNi7Z/view?usp=drive_link">Задание 31:</a> Touch-forehead\nПотрогайте лоб',
            'file32': '<a href="https://drive.google.com/file/d/1OZ5x6HF3Crf-FADWkKt19HRGSg1CrAEj/view?usp=drive_link">Задание 32:</a> Touch-glasses\n(Для записи потребуются очки) Поправьте очки',
            'file33': '<a href="https://drive.google.com/file/d/1TLxipCoi29ZnM_PsSSvrBCRKXuszXeOq/view?usp=drive_link">Задание 33:</a> Touch-head\nПотрогайте голову',
            'file34': '<a href="https://drive.google.com/file/d/1YORFJWOuAMRz8LAXJKvvTU3SUXniYPsD/view?usp=drive_link">Задание 34:</a> Touch-mouth\nПотрогайте рот',
            'file35': '<a href="https://drive.google.com/file/d/1G3WLi-A38mqZSD16QICrRYinGQBLlU4n/view?usp=drive_link">Задание 35:</a> Touch-nose\nПотрогайте нос',
            # Face Pose photo:
            'file36': '<a href="https://drive.google.com/file/d/1ai02BmUv9tb1zrGLrkxqNje5A4b8kpG2/view?usp=drive_link">Задание 36:</a> Glasses-headset\nФото в прозрачных очках и больших наушниках.\nВ очках не должно быть бликов. Вместо наушников допускается головной убор.',
            'file37': '<a href="https://drive.google.com/file/d/109Ckvdc2e6gTvHZpxw3WO64t88FOX5zr/view?usp=drive_link">Задание 37:</a> Mask\nФото в медицинской маске',
            'file38': '<a href="https://drive.google.com/file/d/1VFdRjy6vbubYczeqmbX1bDGWQvo3uniO/view?usp=drive_link">Задание 38:</a> Normal\nФото без эмоций, обычное лицо',
            'file39': '<a href="https://drive.google.com/file/d/1g33g1DQ6JlDz7ppiuIO6FwnorTO1mVbD/view?usp=drive_link">Задание 39:</a> Sunglasses\nФото в темных очках',
            # Hand Pose vid:
            'file40': '<a href="https://drive.google.com/file/d/1VXa_7KkyDBsvnifDuhBsZCyMeSW6C4WH/view?usp=drive_link">Задание 40:</a> Clapping\nСнимите как вы хлопаете в ладошки',
            'file41': '<a href="https://drive.google.com/file/d/1orqIiF4y7bfZRnHU9V52F00CIhkOgD-k/view?usp=drive_link">Задание 41:</a> Greeting\nСнимите как вы приветствуете кого-то',
            # Hand Pose photo:
            'file42': '<a href="https://drive.google.com/file/d/1j95rtx32sR-k635qCVq4pl_un10VpJ4b/view?usp=drive_link">Задание 42:</a> Disike\nФото: палец вниз',
            'file43': '<a href="https://drive.google.com/file/d/1R7fUaB8DevIl52yiJprWosayjMLKzdIa/view?usp=drive_link">Задание 43:</a> Like\nФото: палец вверх',
            'file44': '<a href="https://drive.google.com/file/d/1Of1Joar-DqEjHNZ58-Q_5DE6-NHzm_fI/view?usp=drive_link">Задание 44:</a> Make-a-fist\nФото: показать кулак',
            'file45': '<a href="https://drive.google.com/file/d/1M6CCnERhE_02D07M3dd8B4sTWGf9HkHq/view?usp=drive_link">Задание 45:</a> Number-1\nФото: Показать пальцем цифру 1 (как в примере)',
            'file46': '<a href="https://drive.google.com/file/d/1k1BSpQb45BfMfjuTBHYhIioh62UZsZow/view?usp=drive_link">Задание 46:</a> Number-2\nФото: Показать пальцами цифру 2 (как в примере)',
            'file47': '<a href="https://drive.google.com/file/d/1M_RVhMujraY08OYDglM0lr5w-oclzszc/view?usp=drive_link">Задание 47:</a> Number-3\nФото: Показать пальцами цифру 3 (как в примере)',
            'file48': '<a href="https://drive.google.com/file/d/1lH8-zwAKICOfvGIhAOtzVKSQFYg8FHd_/view?usp=drive_link">Задание 48:</a> Number-4\nФото: Показать пальцами цифру 4 (как в примере)',
            'file49': '<a href="https://drive.google.com/file/d/17mBYlZjIE1fXIbJCdqjpymTv5EwJG4Sd/view?usp=drive_link">Задание 49:</a> Number-5\nФото: Показать пальцами цифру 5 (как в примере)',
            'file50': '<a href="https://drive.google.com/file/d/1HZviA2W_4RKgdzi3UQaFizUYFpHwAfvK/view?usp=drive_link">Задание 50:</a> Number-6\nФото: Показать пальцами цифру 6 (как в примере)',
            'file51': '<a href="https://drive.google.com/file/d/1OElR2QqqC1iEqv5K5gNw8T48J5akRE-9/view?usp=drive_link">Задание 51:</a> Number-8\nФото: Показать пальцами цифру 8 (как в примере)',
            'file52': '<a href="https://drive.google.com/file/d/1fOKd-2pZPpuyIGanZf5Vwfbx1pjmCP-4/view?usp=drive_link">Задание 52:</a> OK\nФото: жест "ok"',
            'file53': '<a href="https://drive.google.com/file/d/1l7N6QVmwVOVBGpdk2YOsF5VUSZHg7wVD/view?usp=drive_link">Задание 53:</a> Point-finger\nФото: показать указательный палец',
            'file54': '<a href="https://drive.google.com/file/d/1sk1V_jj_0IHV4KBxLl5iboznhTauXKZ8/view?usp=drive_link">Задание 54:</a> Put-palms-together\nФото: 🙏 Сложить ладони',
            'file55': '<a href="https://drive.google.com/file/d/1kKNAvIcxeX3yVCj92akhDNVQtB0A8DO4/view?usp=drive_link">Задание 55:</a> Show-hand\nФото: повторите жест из примера',
            'file56': '<a href="https://drive.google.com/file/d/1YA3V-TigMn-CsXcHBSJlouIGLiz57UXi/view?usp=drive_link">Задание 56:</a> Show-hand2\nФото: повторите жест из примера',
            'file57': '<a href="https://drive.google.com/file/d/1-HN39MozLHHBqrvOxMnjmNqsLbpbOxV2/view?usp=drive_link">Задание 57:</a> Show-hand3\nФото: повторите жест из примера',
            'file58': '<a href="https://drive.google.com/file/d/1E_ipDr0KLPgB-Dv6nFgGGoXdDxp6KNiR/view?usp=drive_link">Задание 58:</a> Single-hand-heart\n Фото: 🫰🏻"Тиктокерское сердце"',
            'file59': '<a href="https://drive.google.com/file/d/1S-xpUXldA0pHzvHeAwDQx21nscQXk_hK/view?usp=drive_link">Задание 59:</a> Two-hand-heart\n Фото: Сердце двумя руками',
            # Head Pose new background
            'file60': '<a href="https://drive.google.com/file/d/12vf2QVnhxs_gElqLkFPxKSw6xgiyCYgh/view?usp=drive_link">Задание 60:</a> GlassesPitch\n (Для записи потребуются очки) Снимите как вы отклоняете голову назад и наклоняете её вперед',
            'file61': '<a href="https://drive.google.com/file/d/1c7cppQhpx74guNZZx9jxG54BTJPZUWNP/view?usp=drive_link">Задание 61:</a> GlassesRoll\n(Для записи потребуются очки) Снимите как вы наклоняете голову влево-вправо',
            'file62': '<a href="https://drive.google.com/file/d/11rjkofMR33oVXHzFGa7gTpJviCX5FX3h/view?usp=drive_link">Задание 62:</a> GlassesYaw\n(Для записи потребуются очки) ',
            'file63': '<a href="https://drive.google.com/file/d/1D_JvBisheWLNipYnzuR-zkXH7X9XEXee/view?usp=drive_link">Задание 63:</a> NoGlassesPitch\nСнимите как вы отклоняете голову назад и наклоняете её вперед',
            'file64': '<a href="https://drive.google.com/file/d/1PphVEamh4_hYfC1aTMWDIMjJM2UOIloF/view?usp=drive_link">Задание 64:</a> NoGlassesRoll\nСнимите как вы наклоняете голову влево-вправо',
            'file65': '<a href="https://drive.google.com/file/d/1uKVAxlC1Fhnmtnz8o-KR1Eh3djjAQLvV/view?usp=drive_link">Задание 65:</a> NoGlassesYaw\nСнимите как вы поворачиваете голову влево-вправо',
            },
        'log': 'so-dev',

}
