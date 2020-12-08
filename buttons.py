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
        self.regim = None

    def draw_and_action(self, x, y, text, i):
        mouse = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()
        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            pg.draw.rect(screen, (30, 150, 100), (x, y, self.width, self.height))
            if click[0] == 1:
                self.regim = i
        print_text(text, x + 8, y + 8)


class Menu

    def __init__(self):__


def main_menu (menu):
    while menu == 1:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type != pg.MOUSEBUTTONDOWN:
                pg.display.update()
            if button.regim != None:
                menu = 0


            screen.blit(fon, (0, 0))
            button.draw_and_action(X / 8, Y / 4, 'Запуск произвольного поля', 1)
            button.draw_and_action(X / 8, (Y / 4 + 50), 'Запуск произвольного загруженного из файла поля', 2)
            button.draw_and_action(X / 8, (Y / 4 + 110), 'Рисование рислвания своего поля', 3)
            button.draw_and_action(X / 8, (Y / 4 + 160), 'Настройки', 4)
            button.draw_and_action(X / 8, (Y / 4 + 210), 'Выход', 5)
            print_text('Game of live', X / 4, Y / 10)
    return menu

def settings():
    update_screen = 0
    while update_screen == 0:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type != pg.MOUSEBUTTONDOWN:
                pg.display.update()
            if event.type == pg.MOUSEBUTTONDOWN:
                update_screen = 1

            screen.blit(fon, (0, 0))
            button.draw_and_action(X / 8, Y / 4, 'Назад', 6)
            button.draw_and_action(X / 8, (Y / 4 + 50), 'Сменить язык', 7)
            button.draw_and_action(X / 8, (Y / 4 + 110), 'Звук', 8)
            button.draw_and_action(X / 8, (Y / 4 + 160), 'Заставка', 9)
            print_text('Game of live', X / 4, Y / 10)

