
import numpy as np
import pygame as pg
from pygame.draw import *


class Game_of_life():
    def __init__(self, screen_width, screen_height, fps):
        self.screen_x = screen_width
        self.screen_y = screen_height
        self.fps = fps
        self.field_height = 1000
        self.field_width = 2000
        
    def update_generation(self):
        # Подсчет соседей для каждой клетки кроме граничных
        N = (self.cell_field[0:-2,0:-2] + self.cell_field[0:-2,1:-1] + self.cell_field[0:-2,2:] + self.cell_field[1:-1,0:-2] 
             + self.cell_field[1:-1,2:] + self.cell_field[2: ,0:-2] + self.cell_field[2: ,1:-1] + self.cell_field[2: ,2:])
        # Применение правил
        birth = (N == 3) & (self.cell_field[1:-1,1:-1] == 0)
        survive = ((N == 2) | (N == 3)) & (self.cell_field[1:-1,1:-1] == 1)
        self.cell_field[...] = 0
        self.cell_field[1:-1,1:-1][birth | survive] = 1
    
    def create_random_life(self):
        self.cell_field = np.zeros((self.screen_height, self.screen_width))
        self.cell_field[1:-1,1:-1] = np.random.randint(0, 2, (self.screen_height-2, self.screen_width-2))
        pass
    
    def setup(self):
        
        pass
    
    def load_life(self):
        Path = 'some name'        #FIXME
        with open(Path, 'r') as f:
            f.readlines()
            self.cell_field = f
        
        def handle_events(self):
        
            pass
    
    def update_scale(self):
        self.scale = int(min(self.screen_width / (1.0001 * self.field_width),
                             self.screen_height / (1.0001 * self.field_height)))
        pass
    
    def coordinates_transform(self):
        #FIXME
        # Переводим индексы клеток в массиве в координаты для screen pygame-а
        m, n = self.index_coord.shape
        x_bias_array = np.full(m, self.x_bias).reshape((m, 1))
        y_bias_array = np.full(m, self.y_bias).reshape((m, 1))
        self.screen_coord = self.scale * (self.index_coord + np.hstack([x_bias_array, y_bias_array]))
        self.index_coord[::2] += self.x_bias
        self.index_coord[1::2] += self.y_bias
        self.screen_coord = self.scale * self.index_coord
        pass
    
    def rect_coor(self):
        # Создание координат для каждой вершины кадждого квадратика
        indeses = self.cell_field.nonzero().T
        self.index_coord = indeses
        index_rect = np.hstack((indeses, indeses[:,0]+1, indeses[:,1], indeses+1, 
                                 indeses[:,0], indeses[:,1]+1))
        index_rect[::2] += self.x_bias
        index_rect[1::2] += self.y_bias
        self.screen_rect = self.scale * index_rect
        return self.screen_rect

    def broaden_field(self):
        # Расширяеет поле, т.е. массив клеток, если они подобрались близко к границам
        a, b = np.sum(self.cell_field[1, :]), np.sum(self.cell_field[-2, :])
        c, d = np.sum(self.cell_field[:, 1]), np.sum(self.cell_field[:, -2])
        m, n = np.shape(self.cell_field)
        if a > 0:
            self.cell_field = np.vstack([np.zeros((1, n)), self.cell_field])
            self.y_bias -= 1
            m += 1
        if b > 0:
            self.cell_field = np.vstack([self.cell_field, np.zeros((1, n))])
            m += 1
        if c > 0:
            self.x_bias -= 1
            self.cell_field = np.hstack([np.zeros((m, 1)), self.cell_field])
        if d > 0:
            self.cell_field = np.hstack([self.cell_field, np.zeros((m, 1))])
    
        
###################
#     VUSUALISATION
###################


        
X, Y = 1000, 550
FPS = 15

if __name__ == '__main__':
    game = Game_of_life(X, Y, FPS)
    game.setup()