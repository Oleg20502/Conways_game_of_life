"""
Модуль Menu_of_game

Отвечает за отрисовку меню и выполнение действий кнопок меню

"""

import pygame as pg
from pygame.draw import rect

from Game_languages import Languages

WHITE = (255, 255, 255)
RED = (225, 0, 50)
BLACK = (0, 0, 0)
lightBLACK = (3, 3, 3)
lightGREEN = (0, 255, 0)
BLUE = (0, 0, 255, 20)
GRAY = (125, 125, 125)
lightBLUE = (64, 128, 255)
GREEN = (0, 200, 64, 20)
YELLOW = (225, 225, 0, 2)
PINK = (230, 50, 230, 0)
ORANGE = (255, 165, 0)

L = Languages(1)
# Создаём экземпляр класса Languages, 1 означает, что по умолчанию звук включен
L.Russian()
# Включаем русский язык по умолчанию

def print_text(txt, x0, y0, screen, font_color=(255, 255, 255), font_type='text.ttf', font_size=35):
    """
    Рисуем текст чёрного цвета, размера 35, с координатами x, y
     txt: текст
     x: координата левого верхнего конца по x
     y: оордината левого верхнего конца по y
     screen: экран
     font_color: цвет текста
     font_type: тип шрифта
     font_size: размер текста

    """
    font_type = pg.font.Font(font_type, font_size)
    text = font_type.render(txt, True, font_color)
    screen.blit(text, (x0, y0))


class Button():
    def __init__(self, coor, size, regime, screen):
        self.x0 = coor[0]
        self.y0 = coor[1]
        self.width = size[0]
        self.height = size[1]
        self.regime = regime
        self.screen = screen
        
        self.clicked = 0
        
    def draw(self, x = None, y = None, text = None, color = (0, 0, 0, 0)):
        #rect(self.screen, color, (self.x0, self.y0, self.width, self.height))
        if x != None and y != None:
            if self.x0 < x < self.x0 + self.width and self.y0 < y  < self.y0 + self.height:
                rect(self.screen, (30, 150, 100), (self.x0, self.y0, self.width, self.height))
        print_text(text, self.x0 + 8, self.y0 + 8, self.screen)
        
    def get_clicked(self, x, y):
        if self.x0 < x < self.x0 + self.width and self.y0 < y  < self.y0 + self.height:
            self.clicked = 1
        return self.clicked


class Menu():
    # Класс меню. Класс отвечающий за отрисовку и работу меню. на вход размеры окна дисплея - X и Y, а также сам дисплей.
    """
        Класс Menu отвечает за отрисовку и работу меню

        Атрибуты:
        X - ширина экрана
        Y - высота экрана
        screen - экран

        Методы:
        main_menu - Отрисовка главного окна меню и создание активных кнопок
        Settings - Отрисовка меню настроек и создание активных кнопок
        Language - Отрисовка меню выбора языка и создание активных кнопок
        Volume - Отрисовка меню настройки громкости и создание активных кнопок
        Colour_of_fon - Отрисовка меню выбора цвета фона и создание активных кнопок
        Colour_of_pixels - Отрисовка меню выбора цвета пикселей и создание активных кнопок

    """
    def __init__(self, X, Y, screen):
        self.clock = pg.time.Clock()
        self.X = X
        self.Y =Y
        self.FPS = 90
        self.screen = screen
        self.menu = 0 # Глобальная переменная в классе, может принемать значение 0 и 1, по умолчанию 0, при нажатии на одну из кнопок, запускающих игру - 1.
        self.fon = pg.image.load('fonn.jpeg') # Загрузка фона
        self.col = lightGREEN # Цвет писелей по умолчанию
        self.col_fon_game = BLACK # Цвет фона по умолчанию
        self.colors = {1: RED, 2: BLUE, 3: GREEN, 4: YELLOW, 5: WHITE} # Цвета, которые присваиваются фону или пикселям
        # Названия цветов на русском и английском для отображения их в состоянии
        self.COLNAMESRUS = {1: 'Красный', 2: 'Синий', 3: 'Зелёный', 4: 'Жёлтый', 5: 'Белый'}
        self.COLNAMESENG = {1: 'RED', 2: 'BLUE', 3: 'GREEN', 4: 'YELLOW', 5: 'WHITE'}

    def main_menu(self):
        """
        Отрисовка главного окна меню

        """
        window = 'm'
        x_cor, y_cor = self.X / 8, self.Y / 4
        but_size = (580, 50)
        b1 = Button((x_cor, y_cor), but_size, 1, self.screen)               # Кнопка запуска произвольного поля
        b2 = Button((x_cor, y_cor + 50), but_size, 2, self.screen)        # Кнопка запуска загруженного из файла
        b3 = Button((x_cor, y_cor + 100), but_size, 3, self.screen)       # Кнопка запуска режима рисования своего поля
        b4 = Button((x_cor, y_cor + 150), but_size, 4, self.screen)      # Кнопка настроек
        b5 = Button((x_cor, y_cor + 200), but_size, 5, self.screen)       # Кнопка выхода
        buttons = [b1, b2, b3, b4, b5]
        Run = True
        while Run:
            self.clock.tick(self.FPS)
            pg.display.update()
            pg.event.get()
            self.screen.blit(self.fon, (0, 0))
            x, y = pg.mouse.get_pos()
            b1.draw(x, y, L.zapp)
            b2.draw(x, y, L.zapz)
            b3.draw(x, y, L.zapn)
            b4.draw(x, y, L.nastr)
            b5.draw(x, y, L.exit)
            print_text('Game of live', self.X / 4, self.Y / 10, self.screen)
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    window = 'exit'
                elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    for b in buttons:
                        if b.get_clicked(x, y) == 1:
                            b.clicked = 0
                            if b.regime in [1, 2, 3]:
                                self.menu = b.regime
                                window = 'life'
                            elif b.regime == 4:
                                window = self.Settings()
                            elif b.regime == 5:
                                window = 'exit'
            if window in ['exit', 'life']:
                Run = False
        return window

    def Settings(self):
        """
        Отрисовка меню настроек

        """
        window = 's'
        x_cor, y_cor = self.X / 8, self.Y / 4
        but_size = (400, 50)
        b1 = Button((x_cor, y_cor), but_size, 1, self.screen)
        b2 = Button((x_cor, y_cor + 50), but_size, 2, self.screen)
        b3 = Button((x_cor, y_cor + 100), but_size, 3, self.screen)
        b4 = Button((x_cor, y_cor + 150), but_size, 4, self.screen)
        b5 = Button((x_cor, y_cor + 200), but_size, 5, self.screen)
        buttons = [b1, b2, b3, b4, b5]
        Run = True
        while Run:
            self.clock.tick(self.FPS)
            pg.display.update()
            pg.event.get()
            self.screen.blit(self.fon, (0, 0))
            x, y = pg.mouse.get_pos()
            b1.draw(x, y, L.naz)
            b2.draw(x, y, L.yz)
            b3.draw(x, y, L.s)
            b4.draw(x, y, L.zast)
            b5.draw(x, y, L.vcp)
            print_text('Game of live', self.X / 4, self.Y / 10, self.screen)
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    window = 'exit'
                elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    for b in buttons:
                        if b.get_clicked(x, y) == 1:
                            b.clicked = 0
                            if b.regime == 1:
                                window = 'menu'
                            elif b.regime == 2:
                                window = self.Language()
                            elif b.regime == 3:
                                window = self.Volume()
                            elif b.regime == 4:
                                window = self.Colour_of_fon()
                            elif b.regime == 5:
                                window = self.Colour_of_pixels()
            if window in ['exit', 'menu']:
                Run = False
        return window

    def Language(self):
        """
        Отрисовка меню выбора языка

        """
        window = 'l'
        x_cor, y_cor = self.X / 8, self.Y / 4
        but_size = (200, 50)
        b1 = Button((x_cor, y_cor), but_size, 1, self.screen)
        b2 = Button((x_cor, y_cor + 50), but_size, 2, self.screen)
        b3 = Button((x_cor, y_cor + 100), but_size, 3, self.screen)
        b4 = Button((x_cor, self.Y - 100), but_size, 4, self.screen)
        buttons = [b1, b2, b3]
        Run = True
        while Run:
            self.clock.tick(self.FPS)
            pg.display.update()
            pg.event.get()
            self.screen.blit(self.fon, (0, 0))
            x, y = pg.mouse.get_pos()
            b1.draw(x, y, L.naz)
            b2.draw(x, y, L.rus)
            b3.draw(x, y, L.eng)
            b4.draw(None, None, L.chlan)
            print_text('Game of live', self.X / 4, self.Y / 10, self.screen)
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    window = 'exit'
                elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    for b in buttons:
                        if b.get_clicked(x, y) == 1:
                            b.clicked = 0
                            if b.regime == 1:
                                window = 'settings'
                            elif b.regime == 2:
                                #self.clock.tick(7)
                                L.Russian()
                            elif b.regime == 3:
                                L.English()
            if window in ['exit', 'settings']:
                Run = False
        return window

    def Volume(self):
        """
        Отрисовка меню громкости

        """
        window = 'v'
        x_cor, y_cor = self.X / 8, self.Y / 4
        but_size = (280, 50)
        b1 = Button((x_cor, y_cor), but_size, 1, self.screen)
        b2 = Button((x_cor, y_cor + 50), but_size, 2, self.screen)
        b3 = Button((x_cor, y_cor + 100), but_size, 3, self.screen)
        b4 = Button((x_cor, self.Y - 100), but_size, 4, self.screen)
        buttons = [b1, b2, b3]
        Run = True
        while Run:
            self.clock.tick(self.FPS)
            pg.display.update()
            pg.event.get()
            self.screen.blit(self.fon, (0, 0))
            x, y = pg.mouse.get_pos()
            b1.draw(x, y, L.naz)
            b2.draw(x, y, L.tons)
            b3.draw(x, y, L.toffs)
            b4.draw(None, None, L.sound)
            print_text('Game of live', self.X / 4, self.Y / 10, self.screen)
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    window = 'exit'
                elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    for b in buttons:
                        if b.get_clicked(x, y) == 1:
                            b.clicked = 0
                            if b.regime == 1:
                                window = 'settings'
                            elif b.regime == 2:
                                L.Sound(1)
                                L.regim_of_sound = 1
                                pg.mixer.music.play(-1)
                            elif b.regime == 3:
                                L.Sound(0)
                                L.regim_of_sound = 0
                                pg.mixer.music.pause()
            if window in ['exit', 'settings']:
                Run = False
        return window
    
    def Colour_of_fon(self):
        """
        Отрисовка меню выбора цвета фона

        """
        window = 'cf'
        x_cor, y_cor = self.X / 8, self.Y / 4
        but_size = (150, 50)
        b1 = Button((x_cor, y_cor), but_size, 7, self.screen)
        b2 = Button((x_cor, y_cor + 50), but_size, 1, self.screen)
        b3 = Button((x_cor, y_cor + 100), but_size, 2, self.screen)
        b4 = Button((x_cor, y_cor + 150), but_size, 3, self.screen)
        b5 = Button((x_cor, y_cor + 200), but_size, 4, self.screen)
        b6 = Button((x_cor, y_cor + 250), but_size, 5, self.screen)
        b7 = Button((x_cor, self.Y - 100), but_size, 6, self.screen)
        buttons = [b1, b2, b3, b4, b5, b6]
        Run = True
        while Run:
            self.clock.tick(self.FPS)
            pg.display.update()
            pg.event.get()
            self.screen.blit(self.fon, (0, 0))
            x, y = pg.mouse.get_pos()
            b1.draw(x, y, L.naz)
            b2.draw(x, y, L.red)
            b3.draw(x, y, L.blue)
            b4.draw(x, y, L.green)
            b5.draw(x, y, L.yel)
            b6.draw(x, y, L.wit)
            b7.draw(None, None, L.chcol + ' ' + L.COLF)
            print_text('Game of live', self.X / 4, self.Y / 10, self.screen)
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    window = 'exit'
                elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    for b in buttons:
                        if b.get_clicked(x, y) == 1:
                            b.clicked = 0
                            if b.regime == 7:
                                window = 'settings'
                            elif b.regime in self.colors:
                                if L.lang == 'rus':
                                    self.col_fon_game = self.colors[b.regime]
                                    L.COLF = self.COLNAMESRUS[b.regime]
                                elif L.lang == 'eng':
                                    self.col_fon_game = self.colors[b.regime]
                                    L.COLF = self.COLNAMESENG[b.regime]
            if window in ['exit', 'settings']:
                Run = False
        return window

    def Colour_of_pixels(self):
        """
        Отрисовка меню выбора цвета пикселей

        """
        window = 'cp'
        x_cor, y_cor = self.X / 8, self.Y / 4
        but_size = (850, 50)
        b1 = Button((x_cor, y_cor), but_size, 7, self.screen)
        b2 = Button((x_cor, y_cor + 50), but_size, 1, self.screen)
        b3 = Button((x_cor, y_cor + 100), but_size, 2, self.screen)
        b4 = Button((x_cor, y_cor + 150), but_size, 3, self.screen)
        b5 = Button((x_cor, y_cor + 200), but_size, 4, self.screen)
        b6 = Button((x_cor, y_cor + 250), but_size, 5, self.screen)
        b7 = Button((x_cor, self.Y - 100), but_size, 6, self.screen)
        buttons = [b1, b2, b3, b4, b5, b6]
        Run = True
        while Run:
            self.clock.tick(self.FPS)
            pg.display.update()
            pg.event.get()
            self.screen.blit(self.fon, (0, 0))
            x, y = pg.mouse.get_pos()
            b1.draw(x, y, L.naz)
            b2.draw(x, y, L.red)
            b3.draw(x, y, L.blue)
            b4.draw(x, y, L.green)
            b5.draw(x, y, L.yel)
            b6.draw(x, y, L.wit)
            b7.draw(None, None, L.chcol + ' ' + L.COLP)
            print_text('Game of live', self.X / 4, self.Y / 10, self.screen)
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    window = 'exit'
                elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                    for b in buttons:
                        if b.get_clicked(x, y) == 1:
                            b.clicked = 0
                            if b.regime == 7:
                                window = 'settings'
                            elif b.regime in self.colors:
                                if L.lang == 'rus':
                                    self.col_fon_game = self.colors[b.regime]
                                    L.COLP = self.COLNAMESRUS[b.regime]
                                elif L.lang == 'eng':
                                    self.col_fon_game = self.colors[b.regime]
                                    L.COLP = self.COLNAMESENG[b.regime]
            if window in ['exit', 'settings']:
                Run = False
        return window


if __name__ == "__main__":
    print("This module is not for direct call!")