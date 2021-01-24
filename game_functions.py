import easygui
import numpy as np
from scipy.ndimage import convolve
import os
import tkinter as tk
from pygame.draw import polygon, line
from Format_transform import load_and_transform, rle_encoder
#from Life_algorithms import life


class Game_functions():
    n = 0
    def __init__(self, screen_width, screen_height):
        self.screen_x = screen_width
        self.screen_y = screen_height
        
        self.scale = 0
        self.cell_field = None
        self.cells = None
        self.live = 1
        self.k_window = np.array([2,2,2,2,1,2,2,2,2]).reshape(3,3)
        
        self.x_index_bias = 0
        self.y_index_bias = 0
        self.x_screen_bias = 0
        self.y_screen_bias = 0
        
        self.generation = 1
        self.field_width = 21
        self.field_height = 21
        self.x_start = None
        self.y_start = None
        
    def broaden_field(self, border = 1):
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
        chunk = np.where(self.field_width > 2*chunk and self.field_height > 2*chunk, chunk, 0)
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
        self.live = 0
        self.x_index_bias = 0
        self.y_index_bias = 0
        self.x_screen_bias = 0
        self.y_screen_bias = 0
        
        if regime == 1:                 # Случайная жизнь
            self.field_height = 100
            self.field_width = 200
            self.create_random_life()
            self.live = 1
            
        elif regime == 2:               # Загрузка расположения клеток из файла
            
            self.load()
            if self.live == 1:
                delta_x = 10
                delta_y = 10
                m, n = self.cells.shape
                self.field_height, self.field_width = m + delta_y, n + delta_x
                self.cell_field = np.zeros((self.field_height, self.field_width))
                self.cell_field[delta_y//2:-delta_y//2, delta_x//2:-delta_x//2] = self.cells                
            
        elif regime == 3:                # Пустое поле
            self.live = 1
            self.field_height = 105
            self.field_width = 205
            self.cell_field = np.zeros((self.field_height, self.field_width))
        
        self.set_scale()
    
    def run(self):
        self.generation += 1
        self.broaden_field()
        #self.cell_field = life(self.cell_field)
        self.life()
        self.shrink_field()
        
    def life(self):
        result = convolve(self.cell_field, self.k_window, mode="wrap")
        self.cell_field = (result>4) & (result<8)

    def load(self):
        #Path = 'Patterns/diagonal.rle'
        #Path = 'Patterns/2c5-spaceship-gun-p416.rle'
        #root = tk.Tk()
        #root.withdraw()
        #Path = tk.filedialog.askopenfilename()
        Path  = easygui.fileopenbox()
        #check = os.path.isfile(Path) and os.path.splitext(Path)[1] == '.rle'
        #print(os.path.splitext(Path)[1] == '.rle')
        if not Path == None:
            if os.path.isfile(Path) and os.path.splitext(Path)[1] == '.rle':
                self.cells = load_and_transform(Path)
                self.live = 1
        
    def download(self):
        Path = 'C:/Users/User/Downloads/'
        data = rle_encoder(self.cell_field)
        with open(Path + 'cell_field' + str(Game_functions.n) + '.rle', 'w') as f:
            f.write(data)
        Game_functions.n += 1
        
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
            
    def draw_life(self, color, space):
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
        # Рисуем квадратик,соответствующий каждой клетке
        for r in rect:
            polygon(space, color, [r[0:2], r[2:4], r[4:6], r[6:8]])
            
    def draw_grid(self, color, space):
        x_start = self.x_screen_bias % self.scale
        y_start = self.y_screen_bias % self.scale
        rect_vert_lines = np.arange(x_start, self.screen_x+0.001 + self.scale, self.scale)
        rect_hor_lines = np.arange(y_start, self.screen_y+0.001 + self.scale, self.scale)
        width = 1
        for cor in rect_vert_lines:
            line(space, color, [cor, 0], [cor, self.screen_y], width)
        for cor in rect_hor_lines:
            line(space, color, [0, cor], [self.screen_x, cor], width)
    
    pass

if __name__ == "__main__":
    print("This module is not for direct call!")