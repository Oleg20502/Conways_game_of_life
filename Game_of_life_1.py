
'''

Игра Жизнь

Правая кнопка мыши - добавить клетку;
Левая кнопка мыши - перемещение изображения;
Стрелка вверх - увеличить масштаб;
Стрелка вниз - уменьшить масштаб;
Пробел - пауза.


'''


import numpy as np
import pygame as pg
#import time as t
from pygame.draw import polygon

WHITE = (255, 255, 255)
RED = (225, 0, 50)
BLACK = (0, 0 , 0) 
lightBLACK = (3, 3, 3)
lightGreen = (0, 255, 0)
BLUE  = (0, 0, 255, 20)
GRAY = (125, 125, 125)
lightBlue = (64, 128, 255)
GREEN = (0, 200, 64, 20)
YELLOW = (225, 225, 0, 2)
PINK = (230, 50, 230, 0)
brown = (105, 82, 62, 255)
darkorange3 = (205, 102, 0, 255)
rosybrown5 = (159, 125, 125, 255)
sandybrown = (244, 164, 96, 255)
CLEAR = (0, 0, 0, 0)


class Game_of_life():
    def __init__(self, screen_width, screen_height):
        self.screen_x = screen_width
        self.screen_y = screen_height
        self.scale = 0
        self.x_index_bias = 0
        self.y_index_bias = 0
        self.x_screen_bias = screen_width // 3
        self.y_screen_bias = screen_height // 3
        self.generation = 1
        self.loop = 0
        
    def update_generation(self):
        # Подсчет соседей для каждой клетки кроме граничных
        m, n = self.cell_field.shape
        N = (self.cell_field[0:-2,0:-2] + self.cell_field[0:-2,1:-1] + self.cell_field[0:-2,2:] + self.cell_field[1:-1,0:-2] 
             + self.cell_field[1:-1,2:] + self.cell_field[2: ,0:-2] + self.cell_field[2: ,1:-1] + self.cell_field[2: ,2:])
        # Применение правил
        birth = (N == 3) & (self.cell_field[1:-1,1:-1] == 0)
        survive = ((N == 2) | (N == 3)) & (self.cell_field[1:-1,1:-1] == 1)
        self.new_cell_field = np.zeros((m, n))
        self.new_cell_field[1:-1,1:-1][birth | survive] = 1
        self.old_cell_field = self.cell_field
        self.cell_field = self.new_cell_field
        
    def create_random_life(self):
        self.cell_field = np.zeros((self.field_height, self.field_width))
        self.cell_field[1:-1,1:-1] = np.random.randint(0, 2, (self.field_height-2, self.field_width-2))
        pass
    
    def setup(self, regime):
        if regime == 1:
            self.field_height = 100
            self.field_width = 200
            self.create_random_life()
        elif regime == 3:
            self.cell_field = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                        [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                        [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
                                        [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
                                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
                                        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])            
            self.field_height, self.field_width = np.shape(self.cell_field)
        elif regime == 2:
            self.load_life()
            m, n = self.cell_field.shape
            self.field_width, self.field_height = m + 40, n + 40
        self.set_scale()
        pass
    
    def run(self, run):
        if run:
            if self.loop == 0:
                self.generation += 1
                self.broaden_field()
                self.update_generation()
                self.is_generation_change()
        pass
    
    def load_life(self):
        Path = 'Patterns/Gosper_Gun.txt'        #FIXME
        data_list = []
        with open(Path, 'r') as f:
            for line in f:
                data_list.append(line.split(','))
            self.cell_field = np.asarray(data_list, dtype='int')
        self.broaden_field(0)
    
    def set_scale(self):
        # FIXME
        self.scale = int(min(self.screen_x / (self.field_width),
                             self.screen_y / (self.field_height)))
    
    
    def coordinates_transform(self):
        #FIXME
        # Переводим индексы клеток в массиве в координаты для screen pygame-а
        m, n = self.index_coord.shape
        x_bias_array = np.full(m, self.x_index_bias).reshape((m, 1))
        y_bias_array = np.full(m, self.y_index_bias).reshape((m, 1))
        self.screen_coord = self.scale * (self.index_coord + np.hstack([x_bias_array, y_bias_array]))
        self.index_coord[::2] += self.x_index_bias
        self.index_coord[1::2] += self.y_index_bias
        self.screen_coord = self.scale * self.index_coord
        pass
    
    def rect_coordinetes(self):
        # Создание координат для каждой вершины кадждого квадратика
        indeses = np.asarray(self.cell_field.nonzero()).T[:,::-1]
        self.index_coord = indeses
        m, n = indeses.shape
        index_rect = np.hstack((indeses, indeses[:,0].reshape((m,1))+1, 
                                indeses[:,1].reshape((m,1)), indeses+1, 
                                 indeses[:,0].reshape((m,1)), indeses[:,1].reshape((m,1))+1))
        index_rect[:, ::2] += self.x_index_bias
        index_rect[:, 1::2] += self.y_index_bias
        self.screen_rect = np.zeros(np.shape(index_rect))
        self.screen_rect[:, ::2] = self.scale * index_rect[:, ::2] + self.x_screen_bias
        self.screen_rect[:, 1::2] = self.scale * index_rect[:, 1::2] + self.y_screen_bias
        return self.screen_rect

    def broaden_field(self, border = 1):
        # Расширяеет поле, т.е. массив клеток, если они подобрались близко к границам
        a, b = np.sum(self.cell_field[border, :]), np.sum(self.cell_field[-1-border, :])
        c, d = np.sum(self.cell_field[:, border]), np.sum(self.cell_field[:, -1-border])
        m, n = np.shape(self.cell_field)
        if a > 0:
            self.cell_field = np.vstack([np.zeros((1, n)), self.cell_field])
            self.y_index_bias -= 1
            m += 1
        if b > 0:
            self.cell_field = np.vstack([self.cell_field, np.zeros((1, n))])
            m += 1
        if c > 0:
            self.x_index_bias -= 1
            self.cell_field = np.hstack([np.zeros((m, 1)), self.cell_field])
        if d > 0:
            self.cell_field = np.hstack([self.cell_field, np.zeros((m, 1))])
            
    def add_cell(self, x, y):
        m, n = np.shape(self.cell_field)
        x_index_coord = round((x - self.x_screen_bias) // self.scale - self.x_index_bias)
        y_index_coord = round((y - self.y_screen_bias) // self.scale - self.y_index_bias)
        if m > y_index_coord >= 0 and n > x_index_coord >= 0:
            #self.cell_field[y_index_coord, x_index_coord] = not self.cell_field[y_index_coord, x_index_coord]
            self.cell_field[y_index_coord, x_index_coord] = 1

    def is_generation_change(self):
        if np.allclose(self.cell_field, self.old_cell_field):
            self.loop = 1


###################
#     VUSUALISATION
###################

def draw(Rect, color, space):
    # Рисуем квадратик,соответствующий каждой клетке
    for r in Rect:
        polygon(space, color, [r[0:2], r[2:4], r[4:6], r[6:8]])


def print_text(txt, x, y, font_colour = (0, 0, 0), font_type = 'text.ttf', font_size = 35):
        # Рисуем текст чёрного цвета, размера 35, с координатами x, y
        font_type = pg.font.Font(font_type, font_size)
        text = font_type.render(txt, True, font_colour)
        screen.blit(text, (x, y))


X, Y = 1000, 550
start_FPS = 60
max_FPS = 250
T = 15
x_start, y_start = 0, 0
x_cur, y_cur = 0, 0
track_mouse = 0
arrow_up_pressed = 0
arrow_down_pressed = 0
paint = 0
x_paint = 0
y_paint = 0

def count_period(fps):
    return round(fps / T)
#period = round(FPS / T)


if __name__ == '__main__':
    game = Game_of_life(X, Y)
    
    pg.init()
    screen = pg.display.set_mode((X , Y))
    clock = pg.time.Clock()  
    screen.fill(WHITE)
    pg.display.set_caption('Conways_game_of_life')


    #устанавливает инконку приложения (иконку надо закинуть в одну папку с содержимым игры, название иконки iconofgame.png )
    #icon = pg.image.load('iconofgame.png')
    #pg.display.set_icon(icon)

    pg.display.update()
    clock = pg.time.Clock()
    FPS = start_FPS
    finished = False
    play1, play2 = 1, 1
    t = 0
    menu = 1
    fon = pg.image.load('fon.jpg')


    while menu == 1:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type != pg.KEYDOWN:
                pg.display.update()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_1:
                    i = 1
                if event.key == pg.K_2:
                    i = 2
                if event.key == pg.K_3:
                    i = 3
                menu = 0


            screen.blit(fon, (0, 0))
            print_text('Game of live', X / 4, Y / 10)
            print_text('Нажмите 1 для запука произвольно поля', X / 4, Y / 4)
            print_text('Нажмите 2 для загруженного из файла поля', X / 4, (Y / 4 + 50))
            print_text('Нажмите 3 для рислвания своего поля', X / 4, (Y / 4 + 110))

    game.setup(i)

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
                    if event.button  == 1:
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
                x_paint , y_paint = pg.mouse.get_pos()
                game.add_cell(x_paint, y_paint)
            
            if t % period == 0:
                game.run(play1 and play2)
                #print('Поколение:', game.generation)
                draw(game.rect_coordinetes(), (225, 0, 50), screen)
                
                pg.display.update()
                screen.fill(WHITE)
            
    pg.quit()
