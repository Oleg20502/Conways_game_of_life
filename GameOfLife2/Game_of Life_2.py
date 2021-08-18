
import easygui
import numpy as np
import os
import pygame as pg
from pygame.draw import rect, line
from scipy.ndimage import convolve

from Format_transform import load_and_transform, rle_encoder
from Buttons import Button

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
    def __init__(self, screen_width, screen_height, dx, dy, screen):
        self.screen_x = screen_width
        self.screen_y = screen_height
        self.dx = dx
        self.dy = dy
        self.screen = screen
        
        self.regime = 0
        self.cell_color = WHITE
        self.field_color = BLACK
        self.grid_color = (50, 50, 50)
        self.FPS = 20
        self.grid = 0
        
        self.cells = None
        self.live = 0
        self.scale = 8.0
        self.window = np.array([2,2,2,2,1,2,2,2,2]).reshape(3,3)
        self.generation = 0
        self.field_width = 21
        self.field_height = 21
        self.cell_field = np.zeros((self.field_height, self.field_width))
        
        self.x_index_bias = 0
        self.y_index_bias = 0
        self.x_screen_bias = dx
        self.y_screen_bias = dy
        
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
        n1, m1 = self.get_mouse_index_coord(self.dx-1, self.dy-1)
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
    
    def create_random_life(self, m, n):
        """
        Создает поле, заполненное единицами и нулями случайным образом
        
        """
        self.field_height, self.field_width = m, n
        self.live = 1
        self.cell_field = np.zeros((self.field_height, self.field_width), dtype = 'int8')
        self.cell_field[1:-1,1:-1] = np.random.randint(0, 2, (self.field_height-2, self.field_width-2))
    
    def kill_life(self):
        self.cell_field = 0 * self.cell_field
        self.generation = 0
    
    def run(self):
        """
        Осуществляет цикл смены поколений
        
        """
        self.generation += 1
        self.broaden_field()
        #self.cell_field = life(self.cell_field)
        self.life()
        self.shrink_field()
    
    def life(self):
        """
        Просчитывает новое поколение
        
        """
        result = convolve(self.cell_field, self.window, mode="wrap")
        self.cell_field = np.logical_and(result > 4, result < 8)

    def load_life(self):
        """
        Загружает паттерн
        
        """
        self.live = 0
        #self.x_index_bias = 0
        #self.y_index_bias = 0
        #self.x_screen_bias = 0
        #self.y_screen_bias = 0
        
        Path  = easygui.fileopenbox()
        if not Path == None:
            if os.path.isfile(Path) and os.path.splitext(Path)[1] == '.rle':
                self.cells = load_and_transform(Path)
                self.live = 1
        if self.live == 1:
            delta_x = 10
            delta_y = 10
            m, n = self.cells.shape
            self.field_height, self.field_width = m + delta_y, n + delta_x
            self.cell_field = np.zeros((self.field_height, self.field_width), dtype = 'int8')
            self.cell_field[delta_y//2:-delta_y//2, delta_x//2:-delta_x//2] = self.cells
        
    def download_life(self):
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
        
    def add_cell(self, x, y, add = 1):
        """
        На вход получает координаты положения мыши на экране.
        Функция добавляет живую клетку в сооьветствующую часть экрана.
        
        """
        self.adjust_field()
        
        j, i = self.get_mouse_index_coord(x, y)
        if add == 0:
            self.j_start, self.i_start = j, i
            #self.add = 1
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
        n1, m1 = self.get_mouse_index_coord(self.dx, self.dy)
        n2, m2 = self.get_mouse_index_coord(self.screen_x, self.screen_y)
        n1, n2 = self.hanlde_bounds(n1, axis = 0), self.hanlde_bounds(n2, axis = 0)
        m1, m2 = self.hanlde_bounds(m1, axis = 1), self.hanlde_bounds(m2, axis = 1)
        indeses = np.asarray(self.cell_field[m1:m2,n1:n2].nonzero()).T[:,::-1]
        m, n = indeses.shape
        coord = np.zeros((m, n))
        coord[:, 0] = self.scale * (indeses[:, 0] - self.x_index_bias + n1) + self.x_screen_bias
        coord[:, 1] = self.scale * (indeses[:, 1] - self.y_index_bias + m1) + self.y_screen_bias
        for c in coord:
            rect(self.screen, self.cell_color, [c[0], c[1], int(self.scale)+1, int(self.scale)+1])
            
    def draw_grid(self):
        """
        Рисует на экране сетку. 
        
        """
        if self.grid and self.scale > 4.0:
            x_start = (self.x_screen_bias - self.dx) % self.scale
            y_start = (self.y_screen_bias - self.dy) % self.scale
            rect_vert_lines = np.arange(self.dx + x_start, self.screen_x+0.001 + self.scale, self.scale)
            rect_hor_lines = np.arange(self.dy + y_start, self.screen_y+0.001 + self.scale, self.scale)
            width = 1
            for cor in rect_vert_lines:
                line(self.screen, self.grid_color, [cor, self.dy], [cor, self.screen_y], width)
            for cor in rect_hor_lines:
                line(self.screen, self.grid_color, [self.dx, cor], [self.screen_x, cor], width)
    
    def scroll(self, k, x, y, s_max = 50, s_min = 0.5):
        self.change_index_bias(x, y)
        self.x_screen_bias, self.y_screen_bias = x, y
        if k > 1:
            self.scale = np.round(min(self.scale * k, s_max), 2)
        else:
            self.scale = np.round(max(self.scale * k, s_min), 2)


def main():

    X, Y = 1000, 550
    delta_x = 150
    delta_y = 100
    finished = False
    actions = np.zeros(10)
    
    x_start, y_start = 0, 0
    track_mouse = 0
    #scroll_up = 0
    #scroll_down = 0
    paint = 0
    play1, play2 = 0, 1
    finished = False
    counter = 0
    
    pg.init()
    screen = pg.display.set_mode((X, Y))
    clock = pg.time.Clock()
    FPS = 50
    Tshow = 20
    
    game = Game_functions(X, Y, delta_x, delta_y, screen)
    
    b1 = Button((0, 0), (150, 50), 0, (50, 150, 100))
    b2 = Button((0, 50), (150, 50), 1, (50, 150, 100))
    b3 = Button((150, 0), (150, 50))
    b4 = Button((300, 0), (150, 50))
    b5 = Button((0, 100), (150, 50), 2, (50, 150, 100))
    b6 = Button((0, 150), (150, 50), 3, (50, 150, 100))
    b7 = Button((150, 50), (150, 50), 4, (50, 150, 100))
    b8 = Button((300, 50), (150, 50), 5, (50, 150, 100))
    buttons = [b1, b2,  b5, b6, b7]
    
    period_show = count_period(Tshow, FPS)
            
    while not finished:
        counter += 1
        clock.tick(FPS)
        x, y = pg.mouse.get_pos()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                finished = True
                
            elif event.type == pg.MOUSEBUTTONDOWN:
                if delta_x < x < X and delta_y < y < Y:
                    if event.button == 1:
                        
                        if actions[0]:
                            paint = 1
                            game.add_cell(x, y, 0)
                            
                        elif actions[1]:
                            print('bye')
                            
                    
                    if event.button == 3:
                        track_mouse = 1
                        x_start, y_start = x, y
                        print('Hi')
                
                    if event.button == 5:
                        game.scroll(0.9, x, y)
                
                elif event.button == 1:
                    for b in buttons:
                        actions[b.regime] = b.get_clicked(x, y)
                        print(actions)
                        if b.regime != 0:
                            b.clicked = 0
                    
                    if actions[1]:
                        game.kill_life()
                        
                    if actions[2]:
                        game.load_life()
                        
                    if actions[3]:
                        game.download_life()
                        
                    if actions[4]:
                        game.grid = not game.grid
                    
                    if actions[5]:
                        game.cell_color, game.field_color = game.field_color, game.cell_color

            elif event.type == pg.MOUSEBUTTONUP:
                if delta_x < x < X and delta_y < y < Y:
                    
                    if event.button == 1:
                        paint = 0
                    
                    if event.button == 3:
                        track_mouse = 0
                    
                    if event.button == 4:
                        game.scroll(1.1, x, y)
                    
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    play1 = not play1
                elif event.key == pg.K_ESCAPE:
                    finished = True
                elif event.key == pg.K_s:
                    game.download_life()
                elif event.key == pg.K_c:
                    game.kill_life()
        
        if track_mouse == 1:
            #x_cur, y_cur = pg.mouse.get_pos()
            game.x_screen_bias += x - x_start
            game.y_screen_bias += y - y_start
            x_start, y_start = x, y
    
        if paint:
            #x_p , y_p = pg.mouse.get_pos()
            if delta_x < x < X and delta_y < y < Y:
                game.add_cell(x, y)
        
        if play1 and not paint:
            game.run()
        if counter % period_show == 0:
            game.draw_life()
            game.draw_grid()
            b1.draw('Draw life', screen)
            b2.draw('Kill life', screen)
            b3.draw(str(x - delta_x)+', '+str(y - delta_y), screen)
            b4.draw(str(game.generation), screen)
            b5.draw('Load life', screen)
            b6.draw('Download', screen)
            b7.draw('Grid', screen)
            b8.draw(repr(game.cell_color), screen)
            
            pg.display.update()
            screen.fill((30, 30, 30))
            rect(screen, game.field_color, [delta_x, delta_y, X-delta_x, Y-delta_y])
    
    pg.quit()


if __name__ == "__main__":
    #print("This module is not for direct call!")
    main()