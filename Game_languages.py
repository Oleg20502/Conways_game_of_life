"""
Модуль Game_languages

Устанавливает и изменяет язык меню

"""


class Languages():
    """
    Класс Languages используется для хранения и установки языквых пакетов.

    Атрибуты:
    regim_of_sound - переменная, определяющая что будет отображено в кнопке состояния звука

    Методы:
    Russian - задаёт переменным, отвечающим подписи кнопок, слова на русском языке
    English - задаёт переменным, отвечающим подписи кнопок, слова на английском языке
    Sound - Функция меняющая состояние индикатора звука, на вход подаётся i - переменная состояния звука.
    i = 1 - звук включился, i = 0 - выключился

    """
    def __init__(self, lang = 0, sound_regime = 0, grid_regime = 0):
        self.lang = lang
        self.sound_regime = sound_regime
        self.grid_regime = grid_regime
        # Переменная нужна, чтобы можно было полноценно реализовать смену языка, она означает, что по умодлчанию звук включён,
        # т. е. кнопка показывающая состояние звука такая: "Звук включен"

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
        self.chcol = ['ВЫБРАННЫЙ ЦВЕТ: ', 'SELECTED COLOUR: ']
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
        """
        Присваевает переменным, отвечающим за подписи кнопок значения на русском языке

        """
        self.lang = 0

    def English(self):
        """
        Присваевает переменным, отвечающим за подписи кнопок значения на английском языке

        """
        self.lang = 1
        
    def L(self, word):
        return word[self.lang]
    
    def Sound(self, i):
        """
        Функция меняющая состояние индикатора звука. На вход подаётся
        i - переменная состояния звука. i = 1 - звук включился, i = 0 - выключился

        """
        if i == 1 and self.lang == 'rus':
            self.sound = 'Звук включен'
        elif i == 1 and self.lang == 'eng':
            self.sound = 'Sound on'
        elif i == 0 and self.lang == 'rus':
            self.sound = 'Звук выключен'
        elif i == 0 and self.lang == 'eng':
            self.sound = 'Sound off'


if __name__ == "__main__":
    print("This module is not for direct call!")




