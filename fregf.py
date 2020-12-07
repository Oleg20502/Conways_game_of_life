import numpy as np
import pygame as pg
#import time as t
from pygame.draw import polygon
#from buttons import *


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
    if button.regim == 4:
        settings()
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
    if button.regim == 6:
        main_menu(1)

    X, Y = 1000, 550
    start_FPS = 60
    max_FPS = 250
    T = 15
    x_start, y_start = 0, 0
    x_cur, y_cur = 0, 0
    track_mouse = 0
    arrow_up_pressed = 0
    arrow_down_pressed = 0
    paint = 0
    x_paint = 0
    y_paint = 0

    def count_period(fps):
        return round(fps / T)

    # period = round(FPS / T)

    if __name__ == '__main__':


        pg.init()
        screen = pg.display.set_mode((X, Y))
        clock = pg.time.Clock()
        screen.fill(WHITE)
        pg.display.set_caption('Conways_game_of_life')

        # устанавливает инконку приложения (иконку надо закинуть в одну папку с содержимым игры, название иконки iconofgame.png )
        # icon = pg.image.load('iconofgame.png')
        # pg.display.set_icon(icon)

        pg.display.update()
        clock = pg.time.Clock()
        FPS = start_FPS
        finished = False
        play1, play2 = 1, 1
        t = 0
        menu = 1
        fon = pg.image.load('fon.jpg')
        button = Buttons(850, 50)
