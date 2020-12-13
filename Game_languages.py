


class Languages():

    def __init__(self, regim_of_sound):
        self.regim_of_sound = regim_of_sound



    def Russian(self):
        self.zapp = 'Запуск произвольного поля'
        self.zapz = 'Запуск загруженного из файла поля'
        self.zapn = 'Рисование рислвания своего поля'
        self.nas = 'Настройки'
        self.v = 'Выход'
        self.naz = 'Назад'
        self.yz = 'Язык'
        self.s = 'Звук'
        self.zast = 'Заставка'
        self.vcp = 'Выбор цвета пикселей'
        self.rus = 'Русский'
        self.eng = 'Английский'
        self.tons = 'Включить звук'
        self.toffs = 'Выключить звук'
        self.red = 'Красный'
        self.blue = 'Синий'
        self.yel = 'Жёлтый'
        self.ora = 'Оранжевый'
        self.wit = 'Белый'
        self.pink = 'Розовый'
        self.green = 'Зелёный'
        self.chlan = 'ВЫБРАН РУССКИЙ ЯЗЫК'
        self.chcol = 'ВЫБРАННЫЙ ЦВЕТ:'
        self.COLF = 'Белый'
        self.COLP = 'Красный'
        self.lang = 'rus'
        if self.regim_of_sound == 1:
            self.sound = 'Звук включён'
        elif self.regim_of_sound == 0:
            self.sound = 'Звук выключён'





    def English(self):
        self.zapp = 'Launch custom field'
        self.zapz = 'Launch an arbitrary field loaded from a file'
        self.zapn = 'Draw a custom field'
        self.nas = 'Settings'
        self.v = 'Exit'
        self.naz = 'Back'
        self.yz = 'Language'
        self.s = 'Sound'
        self.zast = 'Screensaver'
        self.vcp = 'Select pixel color'
        self.rus = 'Russian'
        self.eng = 'English'
        self.tons = 'Turn sound on'
        self.toffs = 'Turn sound off'
        self.red = 'Red'
        self.blue = 'Blue'
        self.yel = 'Yellow'
        self.ora = 'Orange'
        self.wit = 'White'
        self.pink = 'Pink'
        self.green = 'Green'
        self.chlan = 'SELECTED ENGLISH LANGUAGE'
        self.chcol = 'SELECTED COLOUR:'
        self.COLF = 'White'
        self.COLP = 'RED'
        self.lang = 'eng'
        if self.regim_of_sound == 1:
            self.sound = 'Sound on'
        elif self.regim_of_sound == 0:
            self.sound = 'Sound off'



    def Sound(self, i):
        if i == 1 and self.lang == 'rus':
            self.sound = 'Звук включён'
            self.regim_of_sounf = 1
        elif i == 1 and self.lang == 'eng':
            self.sound = 'Sound on'
            self.regim_of_sounf = 1
        elif i == 0 and self.lang == 'rus':
            self.sound = 'Звук выключен'
            self.regim_of_sounf = 0
        elif i == 0 and self.lang == 'eng':
            self.sound = 'Sound off'
            self.regim_of_sounf = 0






