"""
Модуль Game_languages

Устанавливает и изменяет язык меню

"""


class Languages():
    """
    Класс Languages используется для хранения и установки языквых пакетов.

    """
    def __init__(self, lang = 0, sound_regime = 0, grid_regime = 0):
        self.lang = lang
        self.sound_regime = sound_regime
        self.grid_regime = grid_regime

        self.zapp = ['Сгенерировать случайное поле', 'Generate random cell field']
        self.zapz = ['Загрузить паттерн из файла', 'Load pattern from file']
        self.zapn = ['Пустое поле', 'Blank cell field']
        self.nastr = ['Настройки', 'Settings']
        self.exit = ['Выход', 'Exit']
        self.naz = ['Назад', 'Back']
        self.yz = ['Язык', 'Language']
        self.zast = ['Выбрать цвет поля', 'Select field color']
        self.vcp = ['Выбрать цвет клеток', 'Select cells color']
        self.rus = ['Русский', 'Russian']
        self.eng = ['Английский', 'English']
        self.sound = ['Звук', 'Sound']
        self.soundon = ['Включить звук', 'Turn sound on']
        self.soundoff = ['Выключить звук', 'Turn sound off']
        self.soundoninfo = ['Звук включен', 'Звук включен']
        self.soundoffinfo = ['Звук выключен', 'Звук выключен']
        self.grid = ['Сетка', 'Grid']
        self.gridon = ['Показывать сетку', 'Show grid']
        self.gridoff = ['Скрыть сетку', 'Hide grid']
        self.gridoninfo = ['Сетка включена', 'Grid on']
        self.gridoffinfo = ['Сетка скрыта', 'Grid off']
        self.red = ['Красный', 'Red']
        self.blue = ['Синий', 'Blue']
        self.yel = ['Жёлтый', 'Yellow']
        self.ora = ['Оранжевый', 'Orange']
        self.wit = ['Белый', 'White']
        self.pink = ['Розовый', 'Pink']
        self.green = ['Зелёный', 'Green']
        self.chlan = ['ВЫБРАН РУССКИЙ ЯЗЫК', 'SELECTED ENGLISH LANGUAGE']
        self.chcol = ['ВЫБРАННЫЙ ЦВЕТ: ', 'SELECTED COLOR: ']
        self.COLF = ['Белый', 'White']
        self.COLP = ['Красный', 'RED']
        self.language = ['rus', 'eng']
        self.COLNAMES = {1: ['Красный', 'RED'], 2: ['Синий', 'BLUE'], 
                         3: ['Зелёный', 'GREEN'], 4: ['Жёлтый', 'YELLOW'], 
                            5: ['Белый', 'WHITE']}
        
        if self.sound_regime == 1:
            self.soundinfo = self.soundoninfo
        elif self.sound_regime == 0:
            self.soundinfo = self.soundoffinfo
        
        if self.grid_regime == 1:
            self.gridinfo = self.gridoninfo
        elif self.grid_regime == 0:
            self.gridinfo = self.gridoffinfo

    def Russian(self):
        self.lang = 0

    def English(self):
        self.lang = 1
        
    def L(self, word):
        """
        Присваевает переменным, отвечающим за подписи кнопок значения на языке,
        соответсвующему self.lang.
        """
        return word[self.lang]


if __name__ == "__main__":
    print("This module is not for direct call!")
