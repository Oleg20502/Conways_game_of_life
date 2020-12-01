import numpy as np
import pygame as pg
from pygame.draw import polygon


def print_text(txt, x, y, font_colour=(0, 0, 0), font_type='text.ttf', font_size=35):
    # Рисуем текст чёрного цвета, размера 35, с координатами x, y
    font_type = pg.font.Font(font_type, font_size)
    text = font_type.render(txt, True, font_colour)
    screen.blit(text, (x, y))

class Buttons:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        
    def draw(self, x, y, text, actuon=None):
        mouse = pg.mouse.get.pos()
        click = pg.mouse.get_pressed()

        if x < mouse[0] < x + self.width:
            if y < mouse[1] < y + self.height:
                pg.draw.rect(screen, (23, 204, 58), (x, y, self.width, self.height))


        else:
            pg.draw.rect(screen, (13, 162, 58), (x, y, self.width, self.height))

        print_text(text, x+10, y+10)