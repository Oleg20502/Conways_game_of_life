
import numpy as np
from Format_transform import load_and_transform
from Life_algorithms import life


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
        
        self.generation = 1
        self.field_width = 21
        self.field_height = 21
        
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
            self.field_height = 105
            self.field_width = 205
            self.cell_field = np.zeros((self.field_height, self.field_width))
        
        self.set_scale()
    
    def run(self):
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


if __name__ == "__main__":
    print("This module is not for direct call!")