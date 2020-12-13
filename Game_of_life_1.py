'''
Игра Жизнь
Правая кнопка мыши - добавить клетку;
Левая кнопка мыши - перемещение изображения;
Колесико мыши - изменить масштаб;
Пробел - пауза.

'''

import numpy as np
import pygame as pg
#import time as t
from pygame.draw import polygon
from Format_transform import load_and_transform
from Menu_of_game import Menu


def life(cell_field):
    #t1 = t.time()
    # Подсчет соседей для каждой клетки кроме граничных
    N = (cell_field[0:-2,0:-2] + cell_field[0:-2,1:-1] + cell_field[0:-2,2:] + cell_field[1:-1,0:-2] + 
        cell_field[1:-1,2:] + cell_field[2: ,0:-2] + cell_field[2: ,1:-1] + cell_field[2: ,2:])
    # Применение правил
    birth = np.logical_and(N == 3, np.logical_not(cell_field[1:-1,1:-1]))
    survive = np.logical_and(np.logical_or(N == 2, N == 3), cell_field[1:-1,1:-1])
    cell_field[1:-1,1:-1] = np.logical_or(birth, survive)
    #print('Новое поколение', t.time() - t1)
    return cell_field


class Game_functions():
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
        
    def broaden_field(self, border = 1):
        #t1 = t.time()
        # Расширяеет поле, т.е. массив клеток, если они подобрались близко к границам
        a, b = np.int(np.any(self.cell_field[border, :])), np.int(np.any(self.cell_field[-1-border, :]))
        c, d = np.int(np.any(self.cell_field[:, border])), np.int(np.any(self.cell_field[:, -1-border]))
        self.field_height += a + b
        self.field_width += c + d
        self.y_index_bias += a
        self.x_index_bias += c
        narrow_field = self.cell_field
        self.cell_field = np.zeros((self.field_height, self.field_width))
        self.cell_field[a:self.field_height-b, c:self.field_width-d] = narrow_field
        #print('Расширение поля', t.time() - t1)
    
    def shrink_field(self):
        chunk = 20
        a, b = np.all(self.cell_field[:chunk+1, :] == 0), np.all(self.cell_field[-chunk-1:, :] == 0)
        c, d = np.all(self.cell_field[:, :chunk+1] == 0), np.all(self.cell_field[:, -chunk-1:] == 0)
        x_start, y_start = chunk * c, chunk * a
        x_end, y_end = self.field_width - chunk * d, self.field_height - chunk * b
        self.cell_field = self.cell_field[ y_start: y_end, x_start: x_end]
        self.field_width = x_end - x_start
        self.field_height = y_end - y_start
        self.x_index_bias -= x_start
        self.y_index_bias -= y_start
        
    def adjust_field(self):
        n1, m1 = self.get_mouse_index_coord(0, 0)
        n2, m2 = self.get_mouse_index_coord(self.screen_x, self.screen_y)
        x_zero, y_zero = min(0, n1), min(0, m1)
        x_end, y_end = max(self.field_width, n2), max(self.field_height, m2)
        old_width, old_height = self.field_width, self.field_height
        self.field_width, self.field_height = x_end - x_zero, y_end - y_zero
        old_field = self.cell_field
        self.cell_field = np.zeros((self.field_height, self.field_width))
        self.cell_field[-y_zero: old_height-y_zero, -x_zero: old_width-x_zero] = old_field
        self.x_index_bias -= x_zero
        self.y_index_bias -= y_zero
        
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
            self.cell_field = life(self.cell_field)
            self.shrink_field()

    def load(self):
        Path = 'Patterns/2c5-spaceship-gun-p416.rle'
        self.cells = load_and_transform(Path)
    
    def set_scale(self):
        self.scale = np.round(np.min([self.screen_x / self.field_width,
                             self.screen_y / self.field_height]), 2)
        
    def hanlde_bounds(self, x, axis = 0):
        if axis != 0 and axis != 1:
            raise TypeError ('Axis should be 0 or 1')
        upper_bound = (1 - axis) * self.field_width + axis * self.field_height
        x = max(x, 0)
        x = min(x, upper_bound)
        return x
    
    def rect_coordinetes(self):
        # Создание координат для каждой вершины кадждого квадратика
        n1, m1 = self.get_mouse_index_coord(0, 0)
        n2, m2 = self.get_mouse_index_coord(self.screen_x, self.screen_y)
        n1, n2 = self.hanlde_bounds(n1, axis = 0), self.hanlde_bounds(n2, axis = 0)
        m1, m2 = self.hanlde_bounds(m1, axis = 1), self.hanlde_bounds(m2, axis = 1)
        indeses = np.asarray(self.cell_field[m1:m2,n1:n2].nonzero()).T[:,::-1]
        m, n = indeses.shape
        rect = np.hstack((indeses, indeses[:,0].reshape((m,1))+1, 
                                indeses[:,1].reshape((m,1)), indeses+1, 
                                 indeses[:,0].reshape((m,1)), indeses[:,1].reshape((m,1))+1))
        rect[:, ::2] = self.scale * (rect[:, ::2] - self.x_index_bias + n1)+ self.x_screen_bias
        rect[:, 1::2] = self.scale * (rect[:, 1::2] - self.y_index_bias + m1) + self.y_screen_bias
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


def draw(Rect, color, space):
    # Рисуем квадратик,соответствующий каждой клетке
    for r in Rect:
        polygon(space, color, [r[0:2], r[2:4], r[4:6], r[6:8]])

def count_period(t, fps):
    return round(fps / t)

def main():
    X, Y = 1000, 550
    start_FPS = 60
    max_FPS = 250
    Trun = 60
    Tshow = 20
    x_start, y_start = 0, 0
    x_cur, y_cur = 0, 0
    track_mouse = 0
    scroll_up = 0
    scroll_down = 0
    paint = 0
    x_paint = 0
    y_paint = 0
    play1, play2 = 0, 1

    game = Game_functions(X, Y)
    
    pg.init()
    screen = pg.display.set_mode((X, Y))
    clock = pg.time.Clock()
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
    M = Menu(X, Y, screen)
    M.main_menu()

    game.setup(M.menu)
    
    counter = 0
    #t2, t3 = 0, 0
    #measure1 = 0
    #measure2 = 0
    while not finished:
        counter += 1
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
                    scroll_down = 1
        
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 3:
                    track_mouse = 0
                if event.button == 1:
                    play2 = 1
                    FPS = start_FPS
                    paint = 0
                if event.button == 4:
                    scroll_up = 1
                    
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    play1 = not play1
        
        if scroll_down:
            x, y = pg.mouse.get_pos()
            game.change_index_bias(x, y)
            game.x_screen_bias, game.y_screen_bias = x, y
            game.scale = np.round(max(game.scale * 0.9, 0.5), 2)
            scroll_down = 0
            
        if scroll_up:
            x, y = pg.mouse.get_pos()
            game.change_index_bias(x, y)
            game.x_screen_bias, game.y_screen_bias = x, y
            game.scale = np.round(min(game.scale * 1.1, 50), 2)
            scroll_up = 0
        
        if track_mouse == 1:
            x_cur, y_cur = pg.mouse.get_pos()
            game.x_screen_bias += x_cur - x_start
            game.y_screen_bias += y_cur - y_start
            x_start, y_start = x_cur, y_cur
        if paint and (not play1 or not play2):
            game.adjust_field()
            x_paint , y_paint = pg.mouse.get_pos()
            game.add_cell(x_paint, y_paint)
            
        if counter % period_run == 0:  
            #time1 = t.time()
            game.run(play1 and play2)
            #time2 = t.time()
            #t2 += 1
            #measure1 += time2 - time1
            #print('Поколение:', game.generation)
        if counter % period_show == 0:
            #time3 = t.time()
            draw(game.rect_coordinetes(), M.col, screen)
            pg.display.update()
            screen.fill(M.col_fon_game)
            #time4 = t.time()
            #t3 += 1
            #measure2 += time4 - time3
    pg.quit()
    #print('Жизнь', round(measure1/t2, 4))
    #print('Pygame', round(measure2/t3, 4))

if __name__ == '__main__':
    main()

