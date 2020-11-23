
import numpy as np
import pygame as pg
from pygame.draw import *

WHITE = (255, 255, 255)
RED = (225, 0, 50)
BLACK = (0 , 0 , 0) 
lightBLACK = (3,3,3)
lightGreen = (0, 255, 0)
BLUE  = (0,0,255, 20)
GRAY = (125, 125, 125)
lightBlue = (64, 128, 255)
GREEN = (0, 200, 64, 20)
YELLOW = (225, 225, 0, 2)
PINK = (230, 50, 230, 0)
brown = (105, 82, 62, 255)
darkorange3 = (205, 102, 0, 255)
rosybrown5 = (159, 125, 125, 255)
sandybrown = (244, 164, 96, 255)
CLEAR = (0,0,0,0)                     # Прозрачный


class Cell():
    def init(self, x, y):
        self.x = x
        self.y = y
        self.live = 1


X_size = 200
Y_size = 100


def createlife(width, height):
    # Функция инициализации жизни
    field = np.zeros((height, width))
    field[1:-1,1:-1] = np.random.randint(0, 2, (height-2, width-2))
    return field

'''def update_gen(array):
    window_life = np.array([[1,1,1],[1,0,1],[1,1,1]])
    life_conv = signal.convolve2d(field, window_life, mode='same')
    m, n = np.shape(field)
    new_field = np.zeros((m, n))
    for i in range(m):
        for j in range(n):
            if field[i, j] == 1:
                if 1 < life_conv[i, j] < 4:
                    new_field[i, j] = 1
            else:
                if life_conv[i, j] == 3:
                    new_field[i, j] = 1
    return new_field'''
   
def update_generation(area):
    # Подсчет соседей для каждой клетки кроме граничных
    N = (area[0:-2,0:-2] + area[0:-2,1:-1] + area[0:-2,2:] + area[1:-1,0:-2] 
         + area[1:-1,2:] + area[2: ,0:-2] + area[2: ,1:-1] + area[2: ,2:])
    # Применение правил
    birth = (N == 3) & (area[1:-1,1:-1] == 0)
    survive = ((N == 2) | (N == 3)) & (area[1:-1,1:-1] == 1)
    area[...] = 0
    area[1:-1,1:-1][birth | survive] = 1
    return area

def set_scale(x_size, y_size, scr_x, scr_y):
    # Устанавливаем масштаб
    scale = int(min(scr_x / (1.001 * x_size), scr_y / (1.001 * y_size)))
    return scale

x_bias = 5
y_bias = 5

def coor_transform(coor, scale):
    # Переводим индексы клеток в массиве в координаты для screen pygame-а
    global x_bias
    global y_bias
    m, n = coor.shape
    x_bias_array = np.full(m, x_bias).reshape((m, 1))
    y_bias_array = np.full(m, y_bias).reshape((m, 1))
    new_coor = scale * (coor + np.hstack([x_bias_array, y_bias_array]))
    return new_coor

def rect_coor(array, scale):
    # Создание координат для каждой вершины кадждого квадратика
    m, n = np.shape(array)
    Rect_array = []
    for i in range(m):
        for j in range(n):
            if array[i, j] > 0:
                coor = np.array([[j, i],[j+1, i], [j+1, i+1], [j, i+1]])
                Rect_array.append(list(coor_transform(coor, scale)))
    return Rect_array

def draw(array, color, scale, space):
    # Рисуем квадратик,соответствующий каждой клетке
    Rect = rect_coor(array, scale)
    for r in Rect:
        polygon(space, color, [list(r[0]), list(r[1]), list(r[2]), list(r[3])])

def broaden_field(field):
    # Расширяеет поле, т.е. массив клеток, если они подобрались близко к границам
    global x_bias
    global y_bias
    a, b = np.sum(field[1, :]), np.sum(field[-2, :])
    c, d = np.sum(field[:, 1]), np.sum(field[:, -2])
    m, n = np.shape(field)
    if a > 0:
        field = np.vstack([np.zeros((1, n)), field])
        y_bias -= 1
        m += 1
    if b > 0:
        field = np.vstack([field, np.zeros((1, n))])
        m += 1
    if c > 0:
        x_bias -= 1
        field = np.hstack([np.zeros((m, 1)), field])
    if d > 0:
        field = np.hstack([field, np.zeros((m, 1))])
    return field


screen_X = 1000
screen_Y = 550
FPS = 15

pg.init()
screen = pg.display.set_mode((screen_X , screen_Y))
clock = pg.time.Clock()  
screen.fill(WHITE)

pg.display.update()
clock = pg.time.Clock()
finished = False

scale = set_scale(X_size, Y_size, screen_X, screen_Y)

'''field = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ,0], 
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
'''

field = np.array([[0,0,0,0,0,0,0,1,0,0],
                [0,0,0,0,0,1,0,1,1,0],
                [0,0,0,0,0,1,0,1,0,0],
                [0,0,0,0,0,1,0,0,0,0],
                [0,0,0,1,0,0,0,0,0,0],
                [0,1,0,1,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0,0,0]])

field = createlife(X_size, Y_size)
generation = 1

while not finished:
    clock.tick(FPS)
    field = broaden_field(field)
    new_field = update_generation(field)
    generation += 1
    print('Поколение:', generation)
    draw(new_field, (225, 0, 50), scale, screen)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            finished = True
    pg.display.update()
    screen.fill(WHITE)
    field = new_field
pg.quit()