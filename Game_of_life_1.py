'''
Игра Жизнь
Правая кнопка мыши - добавить клетку;
Левая кнопка мыши - перемещение изображения;
Колесико мыши - изменить масштаб;
Пробел - пауза.

'''

import numpy as np
import pygame as pg
import time as t
from pygame.draw import polygon
from Format_transform import load_and_transform
from Menu_of_game import Menu, Buttons

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


#regime = 3        ############


def count_period(t, fps):
    return round(fps / t)


if __name__ == '__main__':
    game = Game_of_life(X, Y)
    
    pg.init()
    screen = pg.display.set_mode((X, Y))
    clock = pg.time.Clock()
    screen.fill(WHITE)
    pg.display.set_caption('Conways_game_of_life')
    pg.mixer.music.load('sound in menu.ogg')
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
    col_fon_game = WHITE
    M = Menu(X, Y, screen)
    M.main_menu()
    BUT = Buttons(50, 50, screen)




    game.setup(M.menu)
    print(menu)
    if M.menu != 0:
        t1, t2, t3 = 0, 0, 0
        measure1 = 0
        measure2 = 0
        while not finished:
            t1 += 1
            period_run = count_period(Trun, FPS)
            period_show = count_period(Tshow, FPS)
            clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    finished = True
                    
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 3:
                        track_mouse = 1
                        x_start, y_start = pg.mouse.get_pos()
                    if event.button  == 1:
                        play2 = 0
                        FPS = max_FPS
                        paint = 1
                    if event.button == 5:
                        x, y = pg.mouse.get_pos()
                        game.change_index_bias(x, y)
                        game.x_screen_bias, game.y_screen_bias = x, y
                        game.scale = np.round(game.scale * 0.9, 2)
            
                elif event.type == pg.MOUSEBUTTONUP:
                    if event.button == 3:
                        track_mouse = 0
                    if event.button == 1:
                        play2 = 1
                        FPS = start_FPS
                        paint = 0
                    if event.button == 4:
                        x, y = pg.mouse.get_pos()
                        game.change_index_bias(x, y)
                        game.x_screen_bias, game.y_screen_bias = x, y
                        game.scale = np.round(game.scale * 1.1, 2)
                        
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        play1 = not play1
            
            if track_mouse == 1:
                x_cur, y_cur = pg.mouse.get_pos()
                game.x_screen_bias += x_cur - x_start
                game.y_screen_bias += y_cur - y_start
                x_start, y_start = x_cur, y_cur
            if paint and (not play1 or not play2):
                x_paint , y_paint = pg.mouse.get_pos()
                print(game.get_mouse_index_coord(x_paint, y_paint))
                game.add_cell(x_paint, y_paint)
                
            if t1 % period_run == 0:  
                time1 = t.time()
                game.run(play1 and play2)
                time2 = t.time()
                t2 += 1
                measure1 += time2 - time1
                #print('Поколение:', game.generation)
            if t1 % period_show == 0:
                time3 = t.time()
                draw(game.rect_coordinetes(), M.col, screen)
                pg.display.update()
                screen.fill(M.col_fon_game)
                time4 = t.time()
                t3 += 1
                measure2 += time4 - time3
    
    pg.quit()
    print('Жизнь', round(measure1/t2, 4))
    print('Pygame', round(measure2/t3, 4))



