from settings import mngr

# RU: dict[str, dict[str, str]] = {}
lex: dict = {

        'help': f'Если что-то не работает, нажмите /start или напишите {mngr}',
        'start': 'Привет!\n\n'
                 'Мы собираем фото и видео для обучения нейросети распознавать эмоции, жесты и прочие действия. '
                 'Your picture and personal data will not be published anywhere, '
                 'our purpose is training neural networks to distinguish parts of faces.'
                 'We will check your file and give you the verification code.\n\n'
                 'Прежде чем продолжить, пожалуйста, ознакомьтесь с нашей политикой конфиденциальности и нажмите'
                 ' кнопку ✅.',

        'ban': 'Вам заблокирован доступ к заданиям.',
        'privacy_missing': 'Нажмите галочку, чтобы согласиться с политикой конфиденциальности.',

        'full_hd': 'Нужно отправить файл <b>без сжатия</b>. Если не знаете как, то'
                   ' <a href="https://www.youtube.com/embed/qOOMNJ0gIss">посмотрите пример</a> (9 сек).',


        'instruct1': 'Спасибо! Теперь ознакомьтесь с требованиями к отправляемым файлам:\n'
                     '- Убедитесь, что объектив вашей камеры чист\n'
                     '- Лицо должно быть хорошо видно, на свету, не обрезано\n'
                     '- Видео обязательно должны быть <b>горизонтальные</b> (как в примерах)\n'
                     '- Выполняйте задания точь в точь, как в примере (Если в примере человек поворачивает голову'
                     ' сначала налево, а потом направо - вы делаете также)\n'
                     '- Если в примере требуется поменять задний фон и одежду, то вам требуется сделать то же самое',
        'instruct2': 'Можете приступать к выполнению. Далее вам будет показано первое задание. Как только отправите '
                     'файл - нажмите команда /next для получения следующего задания. Когда вы выполните все 65 заданий - ваши файлы '
                     'будут отправлены на проверку.',
        'log': 'so-dev',
        'album': 'Отправляйте файлы по одному, не группой',
        'all_sent': 'Спасибо! Вы отправили все нужные файлы. Ожидайте проверки вашей работы.',

        # Behavior:
        'user_account': {
                        "file01": [],
                        "file02": [],
                        "file03": [],
                        "file04": [],
                        "file05": [],
                        "file06": [],
                        "file07": [],
                        "file08": [],
                        "file09": [],
                        "file10": [],
                        "file11": [],
                        "file12": [],
                        "file13": [],
                        "file14": [],
                        "file15": [],
                        "file16": [],
                        "file17": [],
                        "file18": [],
                        "file19": [],
                        "file20": [],
                        "file21": [],
                        "file22": [],
                        "file23": [],
                        "file24": [],
                        "file25": [],
                        "file26": [],
                        "file27": [],
                        "file28": [],
                        "file29": [],
                        "file30": [],
                        "file31": [],
                        "file32": [],
                        "file33": [],
                        "file34": [],
                        "file35": [],
                        "file36": [],
                        "file37": [],
                        "file38": [],
                        "file39": [],
                        "file40": [],
                        "file41": [],
                        "file42": [],
                        "file43": [],
                        "file44": [],
                        "file45": [],
                        "file46": [],
                        "file47": [],
                        "file48": [],
                        "file49": [],
                        "file50": [],
                        "file51": [],
                        "file52": [],
                        "file53": [],
                        "file54": [],
                        "file55": [],
                        "file56": [],
                        "file57": [],
                        "file58": [],
                        "file59": [],
                        "file60": [],
                        "file61": [],
                        "file62": [],
                        "file63": [],
                        "file64": [],
                        "file65": []
                      },
        'tasks': {
            'file01': '<a href="https://drive.google.com/file/d/14bYM2Y_N4SFLIXsyJ6fpLPWX1MSh7Zqd/view?usp=drive_link">file01</a> Drink\n(Для записи видео потребуется бутылка воды)\nСнимите как вы пьете воду из бутылки',
            'file02': '<a href="https://drive.google.com/file/d/19L-ac1bbe6kh7cgxiDyUO8MET7VX6Jpk/view?usp=drive_link">file02</a> Eat-food\n(Требуется что-то из еды, по типу снэка без упаковки)\nСнимите как вы едите что-то, например, любой снэк',
            'file03': '<a href="https://drive.google.com/file/d/1D9XJL0fS9nZ4OqQ-D_Csgr6dnk5Kf-ol/view?usp=drive_link">file03</a> Play-phone\n(Для записи видео потребуется второй телефон)\nСнимите как вы печатаете на телефоне',
            'file04': '<a href="https://drive.google.com/file/d/1mtSy2ShtvrTmAtOpEINJeTdYhLDlgdz9/view?usp=drive_link">file04</a> Turn-pen\n(Для записи видео потребуется письменная ручка)\nСнимите как вы крутите ручку в левой руке',
            # Body Pose
            'file05': '<a href="https://drive.google.com/file/d/1VZI4pQF6gd3szi1xmoDrwO5Sr80vgyB5/view?usp=drive_link">file05</a> Body-forth-back\nСнимите как вы наклоняйтесь вперед-назад два раза',
            'file06': '<a href="https://drive.google.com/file/d/1lmgJm0muj2fJZ1YaVpxBsgAx801Kxiae/view?usp=drive_link">file06</a> Body-left-right\nСнимите как вы наклоняйте тело влево-вправо',
            'file07': '<a href="https://drive.google.com/file/d/1tpcY-LKjf5EMOw6Aao5iuSEZxQNMPBaB/view?usp=drive_link">file07</a> Body-rotate\nСнимите как вы поворачивайте тело вместе с головой влево-вправо',
            'file08': '<a href="https://drive.google.com/file/d/14gxs3K9uiUr2CWIJ_QTzuoINpcahAhWA/view?usp=drive_link">file08</a> Fold-arm\nСнимите как вы складываете руки',
            'file09': '<a href="https://drive.google.com/file/d/1DhUO-2aq-VD3-RI8zYHdicbQBBHF5qmw/view?usp=drive_link">file09</a> Shrug-shoulder\nСнимите как вы пожимайте плечами',
            'file10': '<a href="https://drive.google.com/file/d/10bRmPqkIOGUlmMlCag3mu9olMVzrNJJj/view?usp=drive_link">file10</a> Strech-arm\nСнимите как вы тянитесь',
            'file11': '<a href="https://drive.google.com/file/d/1nfVGka8x-LnMxLXDKqnVA2szfO8_htB7/view?usp=drive_link">file11</a> Up-down\nСнимите как вы встаете и сдитесь',
            # Expression:
            'file12': '<a href="https://drive.google.com/file/d/1D9Shqnc-GT4pRvIn7YtCh_JD1or2tn9u/view?usp=drive_link">file12</a> Amazed\nВ этом видео важна эмоция\nСнимите ваше удивление',
            'file13': '<a href="https://drive.google.com/file/d/1Asg0zzVXKCTvBGi49qg8t51HWKTnrVi3/view?usp=drive_link">file13</a> Anger\nВ этом видео важна эмоция\nСнимите как вы злитесь',
            'file14': '<a href="https://drive.google.com/file/d/1FtHT22RWF8QYwLfRTAT_PXYhVUPuGygO/view?usp=drive_link">file14</a> Disgusted\nВ этом видео важна эмоция\nСнимите вашу эмоцию отвращения',
            'file15': '<a href="https://drive.google.com/file/d/1zjPBk8CD8hyO7iOsS6FPgh6OATp5AtIT/view?usp=drive_link">file15</a> Happy\nВ этом видео важна эмоция\nСнимите эмоцию счастья',
            'file16': '<a href="https://drive.google.com/file/d/1rfjchs4I_EAROFdOSeRvhovlZFpAJN6i/view?usp=drive_link">file16</a> Normal\nВ этом видео важна эмоция\nСнимите ваше обычное лицо',
            'file17': '<a href="https://drive.google.com/file/d/1aIlIanjEzkIBA0TyeOv7aHr1OxToBlEq/view?usp=drive_link">file17</a> Sad\nВ этом видео важна эмоция\nСнимите эмоцию грусти',
            'file18': '<a href="https://drive.google.com/file/d/1EZqQZCf1Qeq8dHgLOJYJLGUUHazJLLep/view?usp=drive_link">file18</a> Scared\nВ этом видео важна эмоция\nСнимите ваш испуг',
            # Face Pose vid:
            'file19': '<a href="https://drive.google.com/file/d/1IZtDmoNUsYL0N4PF3Ob-c9kjASEQnr8F/view?usp=drive_link">file19</a> Deep-breath\nСнимите ваш глубокий вдох и выдох',
            'file20': '<a href="https://drive.google.com/file/d/1BC4hbSFc5_ijQjhpX_3f1y8E0KOXSRNU/view?usp=drive_link">file20</a> Eye-closed\nСнимите как вы зажмуриваетесь',
            'file21': '<a href="https://drive.google.com/file/d/17mOicp3XE2VU8dioQiwPGzSpkBClKQTN/view?usp=drive_link">file21</a> Eye-roll\nПовторите движение зрачков в этом видео',
            'file22': '<a href="https://drive.google.com/file/d/161g32put2RKzyqRvTL1CMj5YdKy2uuVZ/view?usp=drive_link">file22</a> Eye-stare\nПоднимите брови и откройте глаза',
            'file23': '<a href="https://drive.google.com/file/d/141HNzEVt3ACcu48bIWUHALD7GNfcFMU2/view?usp=drive_link">file23</a> Mouth-open\nОткройте широко рот ',
            'file24': '<a href="https://drive.google.com/file/d/1yA-FAUAFVaAHOxhh0DSSvt5Fvw8yirb5/view?usp=drive_link">file24</a> Mouth-pout\nСделайте губы трубочкой ',
            'file25': '<a href="https://drive.google.com/file/d/1laBs74n9RdwIwFksIYYdiv80uubIBBmB/view?usp=drive_link">file25</a> Mouth-pucker\nВтяните губы, как на видео',
            'file26': '<a href="https://drive.google.com/file/d/1yXJrhYzs6UH8FnEEBpYmvbNrOYT6I9xs/view?usp=drive_link">file26</a> Put-tongue\nОткройте рот и покажите язык',
            'file27': '<a href="https://drive.google.com/file/d/1Q-E8HOdpRsHnjRlhUkN6N9UNvz_Ed1Zt/view?usp=drive_link">file27</a> Touch-chin\nПотрогайте подбородок',
            'file28': '<a href="https://drive.google.com/file/d/13i8iOrT4nAqAape_g2LvpC8INX7_L9kB/view?usp=drive_link">file28</a> Touch-ear\nПотрогайте ухо',
            'file29': '<a href="https://drive.google.com/file/d/1Amq1N1O_vZQC1fR5qfE_1_VoQLuZFkZs/view?usp=drive_link">file29</a> Touch-eye\nПотрогайте глаза',
            'file30': '<a href="https://drive.google.com/file/d/1xEoSgXtJOsmAlDipk-0hGJPd6jfLN3O8/view?usp=drive_link">file30</a> Touch-face\nПотрогайте щеки',
            'file31': '<a href="https://drive.google.com/file/d/1vphpWl3O2K0J8lzIlTAWsv3rcJqGNi7Z/view?usp=drive_link">file31</a> Touch-forehead\nПотрогайте лоб',
            'file32': '<a href="https://drive.google.com/file/d/1OZ5x6HF3Crf-FADWkKt19HRGSg1CrAEj/view?usp=drive_link">file32</a> Touch-glasses\n(Для записи потребуются очки) Поправьте очки',
            'file33': '<a href="https://drive.google.com/file/d/1TLxipCoi29ZnM_PsSSvrBCRKXuszXeOq/view?usp=drive_link">file33</a> Touch-head\nПотрогайте голову',
            'file34': '<a href="https://drive.google.com/file/d/1YORFJWOuAMRz8LAXJKvvTU3SUXniYPsD/view?usp=drive_link">file34</a> Touch-mouth\nПотрогайте рот',
            'file35': '<a href="https://drive.google.com/file/d/1G3WLi-A38mqZSD16QICrRYinGQBLlU4n/view?usp=drive_link">file35</a> Touch-nose\nПотрогайте нос',
            # Face Pose photo:
            'file36': '<a href="https://drive.google.com/file/d/1ai02BmUv9tb1zrGLrkxqNje5A4b8kpG2/view?usp=drive_link">file36</a> Glasses-headset\nФото в очках и больших наушниках',
            'file37': '<a href="https://drive.google.com/file/d/109Ckvdc2e6gTvHZpxw3WO64t88FOX5zr/view?usp=drive_link">file37</a> Mask\nФото в медицинской маске',
            'file38': '<a href="https://drive.google.com/file/d/1VFdRjy6vbubYczeqmbX1bDGWQvo3uniO/view?usp=drive_link">file38</a> Normal\nФото без эмоций, обычное лицо',
            'file39': '<a href="https://drive.google.com/file/d/1g33g1DQ6JlDz7ppiuIO6FwnorTO1mVbD/view?usp=drive_link">file39</a> Sunglasses\nФото в темных очках',
            # Hand Pose vid:
            'file40': '<a href="https://drive.google.com/file/d/1VXa_7KkyDBsvnifDuhBsZCyMeSW6C4WH/view?usp=drive_link">file40</a> Clapping\nСнимите как вы хлопаете в ладошки',
            'file41': '<a href="https://drive.google.com/file/d/1orqIiF4y7bfZRnHU9V52F00CIhkOgD-k/view?usp=drive_link">file41</a> Greeting\nСнимите как вы приветствуете кого-то',
            # Hand Pose photo:
            'file42': '<a href="https://drive.google.com/file/d/1j95rtx32sR-k635qCVq4pl_un10VpJ4b/view?usp=drive_link">file42</a> Disike\nФото: палец вниз',
            'file43': '<a href="https://drive.google.com/file/d/1R7fUaB8DevIl52yiJprWosayjMLKzdIa/view?usp=drive_link">file43</a> Like\nФото: палец вверх',
            'file44': '<a href="https://drive.google.com/file/d/1Of1Joar-DqEjHNZ58-Q_5DE6-NHzm_fI/view?usp=drive_link">file44</a> Make-a-fist\nФото: показать кулак',
            'file45': '<a href="https://drive.google.com/file/d/1M6CCnERhE_02D07M3dd8B4sTWGf9HkHq/view?usp=drive_link">file45</a> Number-1\nФото: Показать пальцем цифру 1 (как в примере)',
            'file46': '<a href="https://drive.google.com/file/d/1k1BSpQb45BfMfjuTBHYhIioh62UZsZow/view?usp=drive_link">file46</a> Number-2\nФото: Показать пальцами цифру 2 (как в примере)',
            'file47': '<a href="https://drive.google.com/file/d/1M_RVhMujraY08OYDglM0lr5w-oclzszc/view?usp=drive_link">file47</a> Number-3\nФото: Показать пальцами цифру 3 (как в примере)',
            'file48': '<a href="https://drive.google.com/file/d/1lH8-zwAKICOfvGIhAOtzVKSQFYg8FHd_/view?usp=drive_link">file48</a> Number-4\nФото: Показать пальцами цифру 4 (как в примере)',
            'file49': '<a href="https://drive.google.com/file/d/17mBYlZjIE1fXIbJCdqjpymTv5EwJG4Sd/view?usp=drive_link">file49</a> Number-5\nФото: Показать пальцами цифру 5 (как в примере)',
            'file50': '<a href="https://drive.google.com/file/d/1HZviA2W_4RKgdzi3UQaFizUYFpHwAfvK/view?usp=drive_link">file50</a> Number-6\nФото: Показать пальцами цифру 6 (как в примере)',
            'file51': '<a href="https://drive.google.com/file/d/1OElR2QqqC1iEqv5K5gNw8T48J5akRE-9/view?usp=drive_link">file51</a> Number-8\nФото: Показать пальцами цифру 8 (как в примере)',
            'file52': '<a href="https://drive.google.com/file/d/1fOKd-2pZPpuyIGanZf5Vwfbx1pjmCP-4/view?usp=drive_link">file52</a> OK\nФото: жест "ok"',
            'file53': '<a href="https://drive.google.com/file/d/1l7N6QVmwVOVBGpdk2YOsF5VUSZHg7wVD/view?usp=drive_link">file53</a> Point-finger\nФото: показать указательный палец',
            'file54': '<a href="https://drive.google.com/file/d/1sk1V_jj_0IHV4KBxLl5iboznhTauXKZ8/view?usp=drive_link">file54</a> Put-palms-together\nФото: 🙏 Сложить ладони',
            'file55': '<a href="https://drive.google.com/file/d/1kKNAvIcxeX3yVCj92akhDNVQtB0A8DO4/view?usp=drive_link">file55</a> Show-hand\nФото: повторите жест из примера',
            'file56': '<a href="https://drive.google.com/file/d/1YA3V-TigMn-CsXcHBSJlouIGLiz57UXi/view?usp=drive_link">file56</a> Show-hand2\nФото: повторите жест из примера',
            'file57': '<a href="https://drive.google.com/file/d/1-HN39MozLHHBqrvOxMnjmNqsLbpbOxV2/view?usp=drive_link">file57</a> Show-hand3\nФото: повторите жест из примера',
            'file58': '<a href="https://drive.google.com/file/d/1E_ipDr0KLPgB-Dv6nFgGGoXdDxp6KNiR/view?usp=drive_link">file58</a> Single-hand-heart\n Фото: 🫰🏻"Тиктокерское сердце"',
            'file59': '<a href="https://drive.google.com/file/d/1S-xpUXldA0pHzvHeAwDQx21nscQXk_hK/view?usp=drive_link">file59</a> Two-hand-heart\n Фото: Сердце двумя руками',
            # Head Pose new background
            'file60': '<a href="https://drive.google.com/file/d/12vf2QVnhxs_gElqLkFPxKSw6xgiyCYgh/view?usp=drive_link">file60</a> GlassesPitch\n (Для записи потребуются очки) Снимите как вы отклоняете голову назад и наклоняете её вперед',
            'file61': '<a href="https://drive.google.com/file/d/1c7cppQhpx74guNZZx9jxG54BTJPZUWNP/view?usp=drive_link">file61</a> GlassesRoll\n(Для записи потребуются очки) Снимите как вы наклоняете голову влево-вправо',
            'file62': '<a href="https://drive.google.com/file/d/11rjkofMR33oVXHzFGa7gTpJviCX5FX3h/view?usp=drive_link">file62</a> GlassesYaw\n(Для записи потребуются очки) ',
            'file63': '<a href="https://drive.google.com/file/d/1D_JvBisheWLNipYnzuR-zkXH7X9XEXee/view?usp=drive_link">file63</a> NoGlassesPitch\nСнимите как вы отклоняете голову назад и наклоняете её вперед',
            'file64': '<a href="https://drive.google.com/file/d/1PphVEamh4_hYfC1aTMWDIMjJM2UOIloF/view?usp=drive_link">file64</a> NoGlassesRoll\nСнимите как вы наклоняете голову влево-вправо',
            'file65': '<a href="https://drive.google.com/file/d/1uKVAxlC1Fhnmtnz8o-KR1Eh3djjAQLvV/view?usp=drive_link">file65</a> NoGlassesYaw\nСнимите как вы поворачиваете голову влево-вправо',
            }


}
