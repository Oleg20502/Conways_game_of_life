import easygui
import numpy as np
import os
import pygame as pg
from pygame.draw import rect, line
from scipy.ndimage import convolve

from Format_transform import load_and_transform, rle_encoder


def count_period(t, fps):
    return round(fps / t)


class Game_functions():
    """
    Класс Game_functions содержит функции для визуализации игры
    screen_width - ширина экрана
    screen_height - высрта экрана
    
    scale - масштабирующий коэффициент перехода от индексовых координат к экранным
    cell_field - 2D массив из нулей и единиц, поле с клетками 
    
    
    
    """
    n = 0
    def __init__(self, screen_width, screen_height, screen):
        self.screen_x = screen_width
        self.screen_y = screen_height
        self.screen = screen
        
        self.regime = 0
        self.cell_color = None
        self.field_color = None
        self.grid_color = (50, 50, 50)
        self.FPS = 20
        self.grid = 0
        
        self.scale = 0
        self.cell_field = None
        self.cells = None
        self.live = 1
        self.window = np.array([2,2,2,2,1,2,2,2,2]).reshape(3,3)
        self.generation = 0
        self.field_width = 21
        self.field_height = 21
        
        self.x_index_bias = 0
        self.y_index_bias = 0
        self.x_screen_bias = 0
        self.y_screen_bias = 0
        
        self.j_start = None
        self.i_start = None
        self.add = 0
        
    def broaden_field(self, border = 1):
        """
        Расширяеет поле, т.е. массив клеток, если они подобрались близко к границам
        
        """
        a, b = np.int(np.any(self.cell_field[border, :])), np.int(np.any(self.cell_field[-1-border, :]))
        c, d = np.int(np.any(self.cell_field[:, border])), np.int(np.any(self.cell_field[:, -1-border]))
        self.field_height += a + b
        self.field_width += c + d
        self.y_index_bias += a
        self.x_index_bias += c
        narrow_field = self.cell_field
        self.cell_field = np.zeros((self.field_height, self.field_width), dtype = 'int8')
        self.cell_field[a:self.field_height-b, c:self.field_width-d] = narrow_field
    
    def shrink_field(self):
        """
        Сжимает поле, если по краям образуются полосы мертвых клеток,
        шириной больше чем chunk.
        
        """
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
        """
        Подгоняет поле под размер экрана
        
        """
        n1, m1 = self.get_mouse_index_coord(-1, -1)
        n2, m2 = self.get_mouse_index_coord(self.screen_x+1, self.screen_y+1)
        x_zero, y_zero = min(0, n1), min(0, m1)
        x_end, y_end = max(self.field_width, n2), max(self.field_height, m2)
        old_width, old_height = self.field_width, self.field_height
        self.field_width, self.field_height = x_end - x_zero, y_end - y_zero
        old_field = self.cell_field
        self.cell_field = np.zeros((self.field_height, self.field_width), dtype = 'int8')
        self.cell_field[-y_zero: old_height-y_zero, -x_zero: old_width-x_zero] = old_field
        self.x_index_bias -= x_zero
        self.y_index_bias -= y_zero
    
    def create_random_life(self):
        """
        Создает поле, заполненное единицами и нулями случайным образом
        
        """
        self.cell_field = np.zeros((self.field_height, self.field_width), dtype = 'int8')
        self.cell_field[1:-1,1:-1] = np.random.randint(0, 2, (self.field_height-2, self.field_width-2))
    
    def setup(self):
        """
        Функция для подготовки работы в одном из режимов
        
        """
        self.live = 0
        self.x_index_bias = 0
        self.y_index_bias = 0
        self.x_screen_bias = 0
        self.y_screen_bias = 0
        
        if self.regime == 1:                 # Случайная жизнь
            self.field_height = 70
            self.field_width = 100
            self.create_random_life()
            self.live = 1
            
        elif self.regime == 2:               # Загрузка расположения клеток из файла
            
            self.load()
            if self.live == 1:
                delta_x = 10
                delta_y = 10
                m, n = self.cells.shape
                self.field_height, self.field_width = m + delta_y, n + delta_x
                self.cell_field = np.zeros((self.field_height, self.field_width), dtype = 'int8')
                self.cell_field[delta_y//2:-delta_y//2, delta_x//2:-delta_x//2] = self.cells                
            
        elif self.regime == 3:                # Пустое поле
            self.live = 1
            self.field_height = 105
            self.field_width = 205
            self.cell_field = np.zeros((self.field_height, self.field_width), dtype = 'int8')
        
        self.scale = np.round(np.min([self.screen_x / self.field_width,
                             self.screen_y / self.field_height]), 2)
    
    def run(self):
        """
        Осуществляет цикл смены поколений
        
        """
        self.generation += 1
        self.broaden_field()
        #self.cell_field = life(self.cell_field)
        self.life()
        self.shrink_field()
        print(self.cell_field.dtype)
        
    def life(self):
        """
        Просчитывает новое поколение
        
        """
        result = convolve(self.cell_field, self.window, mode="wrap")
        self.cell_field = np.logical_and(result > 4, result < 8)

    def load(self):
        """
        Загружает паттерн
        
        """
        Path  = easygui.fileopenbox()
        if not Path == None:
            if os.path.isfile(Path) and os.path.splitext(Path)[1] == '.rle':
                self.cells = load_and_transform(Path)
                self.live = 1
        
    def download(self):
        """
        Сохраняет состояние поля в файл в папку Загрузки
        
        """
        Path = 'C:/Users/User/Downloads/'
        data = rle_encoder(self.cell_field)
        with open(Path + 'cell_field' + str(Game_functions.n) + '.rle', 'w') as f:
            f.write(data)
        Game_functions.n += 1
        
    def hanlde_bounds(self, x, axis = 0):
        """
        Вспомогательная функция для контроля не выхода переменной x из границ экрана
        
        """
        if axis != 0 and axis != 1:
            raise TypeError ('Axis should be 0 or 1')
        upper_bound = (1 - axis) * self.field_width + axis * self.field_height
        x = max(x, 0)
        x = min(x, upper_bound)
        return x
        
    def change_index_bias(self, x, y):
        """
        Изменяет сбвиг индексовых координат
        
        """
        self.x_index_bias += np.int((x - self.x_screen_bias) // self.scale)
        self.y_index_bias += np.int((y - self.y_screen_bias) // self.scale)
    
    def get_mouse_index_coord(self, x, y):
        """
        На вход получает координаты положения мыши на экране.
        Возвращает кординаты мыши в индексовых координатах.
        
        """
        x_index = np.int((x - self.x_screen_bias) // self.scale + self.x_index_bias)
        y_index = np.int((y - self.y_screen_bias) // self.scale + self.y_index_bias)
        return x_index, y_index
        
    def add_cell(self, x, y):
        """
        На вход получает координаты положения мыши на экране.
        Функция добавляет живую клетку в сооьветствующую часть экрана.
        
        """
        j, i = self.get_mouse_index_coord(x, y)
        if self.add == 0:
            self.j_start, self.i_start = j, i
            self.add = 1
        j_end, i_end = j, i
        
        if j_end - self.j_start == 0:
            I = np.arange(self.i_start, i_end+1)
            J = np.full(np.size(I), j_end)
        else:
            k = (i_end - self.i_start) / (j_end - self.j_start)
            J = np.arange(self.j_start, j_end+1)
            I = self.i_start + np.round(k * (J - self.j_start)).astype('int64')
        for a in range(np.size(J)):
            self.cell_field[I[a], J[a]] = 1
        self.j_start, self.i_start = j_end, i_end
        
        
    def draw_life(self):
        """
        Отображает положение и состояния клеток на экране.
        
        """
        n1, m1 = self.get_mouse_index_coord(0, 0)
        n2, m2 = self.get_mouse_index_coord(self.screen_x, self.screen_y)
        n1, n2 = self.hanlde_bounds(n1, axis = 0), self.hanlde_bounds(n2, axis = 0)
        m1, m2 = self.hanlde_bounds(m1, axis = 1), self.hanlde_bounds(m2, axis = 1)
        indeses = np.asarray(self.cell_field[m1:m2,n1:n2].nonzero()).T[:,::-1]
        m, n = indeses.shape
        coord = np.zeros((m, n))
        coord[:, 0] = self.scale * (indeses[:, 0] - self.x_index_bias + n1)+ self.x_screen_bias
        coord[:, 1] = self.scale * (indeses[:, 1] - self.y_index_bias + m1) + self.y_screen_bias
        for c in coord:
            rect(self.screen, self.cell_color, [c[0], c[1], int(self.scale)+1, int(self.scale)+1])
            
    def draw_grid(self):
        """
        Рисует на экране сетку. 
        
        """
        if self.grid and self.scale > 4.0:
            x_start = self.x_screen_bias % self.scale
            y_start = self.y_screen_bias % self.scale
            rect_vert_lines = np.arange(x_start, self.screen_x+0.001 + self.scale, self.scale)
            rect_hor_lines = np.arange(y_start, self.screen_y+0.001 + self.scale, self.scale)
            width = 1
            for cor in rect_vert_lines:
                line(self.screen, self.grid_color, [cor, 0], [cor, self.screen_y], width)
            for cor in rect_hor_lines:
                line(self.screen, self.grid_color, [0, cor], [self.screen_x, cor], width)
    
    def life_loop(self):
    
        start_FPS = 60
        max_FPS = 250
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
        finished = False
        window = 'exit'
        counter = 0
        
        self.setup()
        if self.live == 0:
            return 'menu'
        
        pg.display.update()
        clock = pg.time.Clock()
        FPS = start_FPS
    
        while not finished:
            counter += 1
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
                        self.add = 0
                    if event.button == 4:
                        scroll_up = 1
                        
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        play1 = not play1
                    elif event.key == pg.K_ESCAPE:
                        window = 'menu'
                        finished = True
                    elif event.key == pg.K_s:
                        self.download()
                    elif event.key == pg.K_c:
                        self.cell_field = 0 * self.cell_field
               
            if scroll_down:
                x, y = pg.mouse.get_pos()
                self.change_index_bias(x, y)
                self.x_screen_bias, self.y_screen_bias = x, y
                self.scale = np.round(max(self.scale * 0.9, 0.5), 2)
                scroll_down = 0
                
            if scroll_up:
                x, y = pg.mouse.get_pos()
                self.change_index_bias(x, y)
                self.x_screen_bias, self.y_screen_bias = x, y
                self.scale = np.round(min(self.scale * 1.1, 50), 2)
                scroll_up = 0
            
            if track_mouse == 1:
                x_cur, y_cur = pg.mouse.get_pos()
                self.x_screen_bias += x_cur - x_start
                self.y_screen_bias += y_cur - y_start
                x_start, y_start = x_cur, y_cur
            
            if paint:
                self.adjust_field()
                x_paint , y_paint = pg.mouse.get_pos()
                self.add_cell(x_paint, y_paint)
                
            if play1 and play2:
                self.run()
            if counter % period_show == 0:
                self.draw_life()
                self.draw_grid()
                pg.display.update()
                self.screen.fill(self.field_color)
        return window


if __name__ == "__main__":
    print("This module is not for direct call!")