'''
Игра Жизнь
Правая кнопка мыши - добавить клетку;
Левая кнопка мыши - перемещение изображения;
Колесико мыши - изменить масштаб;
Пробел - пауза.

'''

import numpy as np
import pygame as pg
from ji import *


import time as t
from pygame.draw import polygon
from Format_transform import load_and_transform

WHITE = (255, 255, 255)
RED = (225, 0, 50)
BLACK = (0, 0, 0)
lightBLACK = (3, 3, 3)
lightGreen = (0, 255, 0)
BLUE = (0, 0, 255, 20)
GRAY = (125, 125, 125)
lightBlue = (64, 128, 255)
GREEN = (0, 200, 64, 20)
YELLOW = (225, 225, 0, 2)
PINK = (230, 50, 230, 0)
ORANGE = (255, 165, 0)
brown = (105, 82, 62, 255)
darkorange3 = (205, 102, 0, 255)
rosybrown5 = (159, 125, 125, 255)
sandybrown = (244, 164, 96, 255)
CLEAR = (0, 0, 0, 0)
zapp = 'Запуск произвольного поля'
zapz = 'Запуск произвольного загруженного из файла поля'
zapn = 'Рисование рислвания своего поля'
nas = 'Настройки'
v = 'Выход'
naz = 'Назад'
yz = 'Язык'
s = 'Звук'
zast = 'Заставка'
vcp = 'Выбор цвета пикселей'
rus = 'Русский'
eng = 'Английский'

class Game_of_life():
    def __init__(self, screen_width, screen_height):
        self.screen_x = screen_width
        self.screen_y = screen_height
        
        self.scale = 0
        self.cell_field = None
        self.cells = None
        
        self.x_index_bias = 0
        self.y_index_bias = 0
        self.x_screen_bias = 0
        self.y_screen_bias = 0
        
        self.generation = 0
        
    def update_generation(self):
        # Подсчет соседей для каждой клетки кроме граничных
        N = (self.cell_field[0:-2,0:-2] + self.cell_field[0:-2,1:-1] + self.cell_field[0:-2,2:] + self.cell_field[1:-1,0:-2] + 
            self.cell_field[1:-1,2:] + self.cell_field[2: ,0:-2] + self.cell_field[2: ,1:-1] + self.cell_field[2: ,2:])
        # Применение правил
        birth = np.logical_and(N == 3, np.logical_not(self.cell_field[1:-1,1:-1]))
        survive = np.logical_and(np.logical_or(N == 2, N == 3), self.cell_field[1:-1,1:-1])
        self.cell_field[1:-1,1:-1] = birth | survive
        
    def broaden_field(self, border = 1):
        # Расширяеет поле, т.е. массив клеток, если они подобрались близко к границам
        a, b = np.sum(self.cell_field[border, :]), np.sum(self.cell_field[-1-border, :])
        c, d = np.sum(self.cell_field[:, border]), np.sum(self.cell_field[:, -1-border])
        if a > 0:
            self.cell_field = np.vstack([np.zeros((1, self.field_width)), self.cell_field])
            self.y_index_bias += 1
            self.field_height += 1
        if b > 0:
            self.cell_field = np.vstack([self.cell_field, np.zeros((1, self.field_width))])
            self.field_height += 1
        if c > 0:
            self.x_index_bias += 1
            self.cell_field = np.hstack([np.zeros((self.field_height, 1)), self.cell_field])
            self.field_width += 1
        if d > 0:
            self.cell_field = np.hstack([self.cell_field, np.zeros((self.field_height, 1))])
            self.field_width += 1
        
    def create_random_life(self):
        self.cell_field = np.zeros((self.field_height, self.field_width))
        self.cell_field[1:-1,1:-1] = np.random.randint(0, 2, (self.field_height-2, self.field_width-2))
    
    def setup(self, regime):
        if regime == 1:                 # Случайная жизнь
            self.field_height = 100
            self.field_width = 200
            self.create_random_life()
            
        elif regime == 2:               # Загрузка расположения клеток из файла
            self.load()
            delta_x = 10
            delta_y = 10
            m, n = self.cells.shape
            self.field_height, self.field_width = m + delta_y, n + delta_x
            self.cell_field = np.zeros((self.field_height, self.field_width))
            self.cell_field[delta_y//2:-delta_y//2, delta_x//2:-delta_x//2] = self.cells
            
        elif regime == 3:                # Пустое поле
            self.field_height = 100
            self.field_width = 200
            self.cell_field = np.zeros((self.field_height, self.field_width))
        
        self.set_scale()
    
    
    def run(self, run):
        if run:
            self.generation += 1
            self.broaden_field()
            self.update_generation()
    
    
    def load_life(self):
        Path = 'Patterns/Gosper_Gun.txt'  # FIXME
        data_list = []
        with open(Path, 'r') as f:
            for line in f:
                data_list.append(line.split(','))
            self.cell_field = np.asarray(data_list, dtype='int')
        self.broaden_field(0)


class Buttons:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.regim = None

    def draw_and_action(self, x, y, text, i):
        mouse = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()
        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            pg.draw.rect(screen, (30, 150, 100), (x, y, self.width, self.height))
            if click[0] == 1:
                self.regim = i
        print_text(text, x + 8, y + 8)

        
    def load(self):
        Path = 'Patterns/2c5-spaceship-gun-p416.rle'
        self.cells = load_and_transform(Path)
    
    def set_scale(self):
        self.scale = np.round(np.min([self.screen_x / self.field_width,
                             self.screen_y / self.field_height]), 2)
    
    def rect_coordinetes(self):
        # Создание координат для каждой вершины кадждого квадратика
        #n1, m1 = self.get_mouse_index_coord(0, 0)
        #n2, m2 = self.get_mouse_index_coord(self.screen_x, self.screen_y)
        #indeses = np.asarray(self.cell_field[m1:m2,n1:n2].nonzero()).T[:,::-1]
        indeses = np.asarray(self.cell_field.nonzero()).T[:,::-1]
        m, n = indeses.shape
        rect = np.hstack((indeses, indeses[:,0].reshape((m,1))+1, 
                                indeses[:,1].reshape((m,1)), indeses+1, 
                                 indeses[:,0].reshape((m,1)), indeses[:,1].reshape((m,1))+1))
        rect[:, ::2] = self.scale * (rect[:, ::2] - self.x_index_bias)+ self.x_screen_bias
        rect[:, 1::2] = self.scale * (rect[:, 1::2] - self.y_index_bias) + self.y_screen_bias
        return rect
        
    def change_index_bias(self, x, y):
        self.x_index_bias += np.int((x - self.x_screen_bias) // self.scale)
        self.y_index_bias += np.int((y - self.y_screen_bias) // self.scale)
    
    def get_mouse_index_coord(self, x, y):
        x_index = np.int((x - self.x_screen_bias) // self.scale + self.x_index_bias)
        y_index = np.int((y - self.y_screen_bias) // self.scale + self.y_index_bias)
        return x_index, y_index
        
    def add_cell(self, x, y):
        j, i = self.get_mouse_index_coord(x, y)
        if self.field_height > i >= 0 and self.field_width > j >= 0:
            self.cell_field[i, j] = 1

        

###################
#     VUSUALISATION
###################

def draw(Rect, color, space):
    # Рисуем квадратик,соответствующий каждой клетке
    for r in Rect:
        polygon(space, color, [r[0:2], r[2:4], r[4:6], r[6:8]])


def print_text(txt, x, y, font_colour=(255, 255, 255), font_type='text.ttf', font_size=35):
    # Рисуем текст чёрного цвета, размера 35, с координатами x, y
    font_type = pg.font.Font(font_type, font_size)
    text = font_type.render(txt, True, font_colour)
    screen.blit(text, (x, y))


def main_menu():
    update_screen = 0
    while update_screen == 0:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type != pg.MOUSEBUTTONDOWN:
                pg.display.update()
            if event.type == pg.MOUSEBUTTONDOWN:
                update_screen = 1

            screen.blit(fon, (0, 0))
            button.draw_and_action(X / 8, Y / 4, zapp, 1)
            button.draw_and_action(X / 8, (Y / 4 + 50), zapz, 2)
            button.draw_and_action(X / 8, (Y / 4 + 110), zapn, 3)
            button.draw_and_action(X / 8, (Y / 4 + 160), nas, 4)
            button.draw_and_action(X / 8, (Y / 4 + 210), v, 5)
            print_text('Game of live', X / 4, Y / 10)
    if button.regim == 1 or button.regim == 2 or button.regim == 3:
        global menu
        menu = 0
    if button.regim == 4:
        Settings()
    if button.regim == 5:
        exit()


def Settings():
    update_screen = 0
    while update_screen == 0:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type != pg.MOUSEBUTTONDOWN:
                pg.display.update()
            if event.type == pg.MOUSEBUTTONDOWN:
                update_screen = 1

            screen.blit(fon, (0, 0))
            button.draw_and_action(X / 8, Y / 4, naz, 6)
            button.draw_and_action(X / 8, (Y / 4 + 50), yz, 7)
            button.draw_and_action(X / 8, (Y / 4 + 110), s, 8)
            button.draw_and_action(X / 8, (Y / 4 + 160), zast, 9)
            button.draw_and_action(X / 8, (Y / 4 + 210), vcp, 10)
            print_text('Game of live', X / 4, Y / 10)
    if button.regim == 6:
        main_menu()
    if button.regim == 7:
        Language()
    if button.regim == 8:
        Volume()
    if button.regim == 9:
        Fon()
    if button.regim == 10:
        Colour_of_pixels()

def Language():
    update_screen = 0
    while update_screen == 0:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type != pg.MOUSEBUTTONDOWN:
                pg.display.update()
            if event.type == pg.MOUSEBUTTONDOWN:
                update_screen = 1

            screen.blit(fon, (0, 0))
            button.draw_and_action(X / 8, Y / 4, rus, 11)
            button.draw_and_action(X / 8, (Y / 4 + 50), eng, 12)
            button.draw_and_action(X / 8, (Y / 4 + 110), naz, 13)
            print_text('Game of live', X / 4, Y / 10)
    if button.regim == 11:
        Russian()
        Language()
    if button.regim == 12:
        English()
        Language()
    if button.regim == 13:
        Settings()

def Russian():
    global zapp, zapz, zapn, nas, v, naz, yz, s, zast, vcp, rus, eng
    zapp = 'Запуск произвольного поля'
    zapz = 'Запуск произвольного загруженного из файла поля'
    zapn = 'Рисование рислвания своего поля'
    nas = 'Настройки'
    v = 'Выход'
    naz = 'Назад'
    yz = 'Язык'
    s = 'Звук'
    zast = 'Заставка'
    vcp = 'Выбор цвета пикселей'
    rus = 'Русский'
    eng = 'Английский'

def English():
    global zapp, zapz, zapn, nas, v, naz, yz, s, zast, vcp, rus, eng
    zapp = 'Launch custom field'
    zapz = 'Launch an arbitrary field loaded from a file'
    zapn = 'Draw a custom field'
    nas = 'Settings'
    v = 'Exit'
    naz = 'Back'
    yz = 'Language'
    s = 'Sound'
    zast = 'Screensaver'
    vcp = 'Select pixel color'
    rus = 'Russian'
    eng = 'English'


def Volume():
    update_screen = 0
    while update_screen == 0:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type != pg.MOUSEBUTTONDOWN:
                pg.display.update()
            if event.type == pg.MOUSEBUTTONDOWN:
                update_screen = 1

            screen.blit(fon, (0, 0))
            button.draw_and_action(X / 8, Y / 4, 'Включить звук',14)
            button.draw_and_action(X / 8, (Y / 4 + 50), 'Выключить звук', 15)
            button.draw_and_action(X / 8, (Y / 4 + 110), 'Назад', 16)
            print_text('Game of live', X / 4, Y / 10)
    if button.regim == 14:
        pg.mixer.music.play(-1)
        Volume()
    if button.regim == 15:
        pg.mixer.music.pause()
        Volume()
    if button.regim == 16:
        Settings()


def Fon():
    update_screen = 0
    while update_screen == 0:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type != pg.MOUSEBUTTONDOWN:
                pg.display.update()
            if event.type == pg.MOUSEBUTTONDOWN:
                update_screen = 1

            screen.blit(fon, (0, 0))
            button.draw_and_action(X / 8, Y / 4, 'Красный', 17)
            button.draw_and_action(X / 8, (Y / 4 + 50), 'Синий', 181)
            button.draw_and_action(X / 8, (Y / 4 + 110), 'Зелёный', 182)
            button.draw_and_action(X / 8, (Y / 4 + 160), 'Жёлтый', 183)
            button.draw_and_action(X / 8, (Y / 4 + 210), 'Оранжевый', 184)
            button.draw_and_action(X / 8, (Y / 4 + 260), 'Белый', 185)
            button.draw_and_action(X / 8, (Y / 4 + 310), 'Назад', 19)
            print_text('Game of live', X / 4, Y / 10)
    if button.regim == 17:
        global col_fon_game
        col_fon_game = RED
        Fon()
    if button.regim == 181:
        col_fon_game = BLUE
        Fon()
    if button.regim == 182:
        col_fon_game = GREEN
        Fon()
    if button.regim == 183:
        col_fon_game = YELLOW
        Fon()
    if button.regim == 184:
        col_fon_game = ORANGE
        Fon()
    if button.regim == 185:
        col_fon_game = WHITE
        Fon()
    if button.regim == 19:
        Settings()


def Colour_of_pixels():
    update_screen = 0
    while update_screen == 0:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type != pg.MOUSEBUTTONDOWN:
                pg.display.update()
            if event.type == pg.MOUSEBUTTONDOWN:
                update_screen = 1

            screen.blit(fon, (0, 0))
            button.draw_and_action(X / 8, Y / 4, 'Красный', 20)
            button.draw_and_action(X / 8, (Y / 4 + 50), 'Синий', 21)
            button.draw_and_action(X / 8, (Y / 4 + 110), 'Зелёный', 22)
            button.draw_and_action(X / 8, (Y / 4 + 160), 'Жёлтый', 23)
            button.draw_and_action(X / 8, (Y / 4 + 210), 'Оранжевый', 24)
            button.draw_and_action(X / 8, (Y / 4 + 260), 'Розовый', 25)
            button.draw_and_action(X / 8, (Y / 4 + 310), 'Назад', 26)
            print_text('Game of live', X / 4, Y / 10)
    if button.regim == 20:
        global col
        col = RED
        Colour_of_pixels()
    if button.regim == 21:
        col = BLUE
        Colour_of_pixels()
    if button.regim == 22:
        col = GREEN
        Colour_of_pixels()
    if button.regim == 23:
        col = YELLOW
        Colour_of_pixels()
    if button.regim == 24:
        col = ORANGE
        Colour_of_pixels()
    if button.regim == 25:
        col = PINK
        Colour_of_pixels()
    if button.regim == 26:
        Settings()





X, Y = 1000, 550
start_FPS = 30
max_FPS = 250
Trun = 30
Tshow = 20
x_start, y_start = 0, 0
x_cur, y_cur = 0, 0
track_mouse = 0
arrow_up_pressed = 0
arrow_down_pressed = 0
scroll_up = 0
scroll_down = 0
paint = 0
x_paint = 0
y_paint = 0
play1, play2 = 0, 1


regime = 3        ############


def count_period(t, fps):
    return round(fps / t)


if __name__ == '__main__':
    game = Game_of_life(X, Y)
    
    pg.init()
    screen = pg.display.set_mode((X, Y))
    clock = pg.time.Clock()
    screen.fill(WHITE)
    pg.display.set_caption('Conways_game_of_life')
    pg.mixer.music.load('sound in menu.mp3')
    pg.mixer.music.set_volume(0.35)
    pg.mixer.music.play(-1)
    # устанавливает инконку приложения (иконку надо закинуть в одну папку с содержимым игры, название иконки iconofgame.png )
    # icon = pg.image.load('iconofgame.png')
    # pg.display.set_icon(icon)

    pg.display.update()
    clock = pg.time.Clock()
    FPS = start_FPS
    finished = False
    menu = 1
    col = RED
    fon = pg.image.load('fonn.jpeg')
    button = Buttons(850, 50)
    col_fon_game = WHITE
    main_menu()




    game.setup(button.regim)
    print(menu)
    if menu == 0:
        while not finished:
            t += 1
            period = count_period(FPS)
            clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    finished = True

                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 3:
                        track_mouse = 1
                        x_start, y_start = pg.mouse.get_pos()
                    if event.button == 1:
                        play2 = 0
                        FPS = max_FPS
                        paint = 1
                    if event.button == 5:
                        print(event)

                elif event.type == pg.MOUSEBUTTONUP:
                    if event.button == 3:
                        track_mouse = 0
                    if event.button == 1:
                        play2 = 1
                        FPS = start_FPS
                        paint = 0
                    if event.button == 4:
                        print(event)

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_UP:
                        arrow_up_pressed = 1
                    elif event.key == pg.K_DOWN:
                        arrow_down_pressed = 1
                    if event.key == pg.K_SPACE:
                        play1 = not play1

                elif event.type == pg.KEYUP:
                    if event.key == pg.K_UP:
                        arrow_up_pressed = 0
                    elif event.key == pg.K_DOWN:
                        arrow_down_pressed = 0

            if track_mouse == 1:
                x_cur, y_cur = pg.mouse.get_pos()
                game.x_screen_bias += x_cur - x_start
                game.y_screen_bias += y_cur - y_start
                x_start, y_start = x_cur, y_cur
            if arrow_up_pressed:
                game.scale *= 1.1
            if arrow_down_pressed:
                game.scale *= 0.9
            if paint and (not play1 or not play2):
                x_paint, y_paint = pg.mouse.get_pos()
                game.add_cell(x_paint, y_paint)

            if t % period == 0:
                game.run(play1 and play2)
                # print('Поколение:', game.generation)
                draw(game.rect_coordinetes(), col, screen)

                pg.display.update()
                screen.fill(col_fon_game)

    pg.quit()



