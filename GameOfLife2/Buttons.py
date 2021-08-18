import pygame as pg
from pygame.draw import rect


def print_text(txt, x0, y0, screen, font_color=(255, 255, 255), font_type='text.ttf', font_size=35):
    """
    Рисуем текст чёрного цвета, размера 35, с координатами x, y
     txt: текст
     x: координата левого верхнего конца по x
     y: оордината левого верхнего конца по y
     screen: экран
     font_color: цвет текста
     font_type: тип шрифта
     font_size: размер текста

    """
    font_type = pg.font.Font(font_type, font_size)
    text = font_type.render(txt, True, font_color)
    screen.blit(text, (x0, y0))


class Button():
    def __init__(self, coor, size, regime = None, color = (0, 0, 0, 0)):
        self.x0 = coor[0]
        self.y0 = coor[1]
        self.width = size[0]
        self.height = size[1]
        self.regime = regime
        #self.text = text
        self.color = color
        #self.screen = screen
        
        self.clicked = 0
        
    def draw(self, text, screen=None):
        rect(screen, self.color, (self.x0, self.y0, self.width, self.height))
        #if x != None and y != None:
        #    if self.x0 < x < self.x0 + self.width and self.y0 < y  < self.y0 + self.height:
        #        rect(screen, (30, 150, 100), (self.x0, self.y0, self.width, self.height))
        print_text(text, self.x0 + 8, self.y0 + 8, screen)
        
    def get_clicked(self, x, y):
        if self.x0 < x < self.x0 + self.width and self.y0 < y  < self.y0 + self.height:
            self.clicked = 1
        return self.clicked