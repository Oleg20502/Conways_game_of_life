

import numpy as np
import pygame as pg
from Game_languages import Languages


L=Languages()
L.Russian()

def print_text(txt, x, y, screen, font_colour=(255, 255, 255), font_type='text.ttf', font_size=35):
    # Рисуем текст чёрного цвета, размера 35, с координатами x, y
    font_type = pg.font.Font(font_type, font_size)
    text = font_type.render(txt, True, font_colour)
    screen.blit(text, (x, y))

class Buttons():

    def __init__(self, width, height, screen):
        self.width = width
        self.height = height
        self.regim = None
        self.screen = screen

    def draw_and_action(self, x, y, text, i):
        mouse = pg.mouse.get_pos()
        click = pg.mouse.get_pressed()
        if x < mouse[0] < x + self.width and y < mouse[1] < y + self.height:
            pg.draw.rect(self.screen, (30, 150, 100), (x, y, self.width, self.height))
            if click[0] == 1:
                self.regim = i
        print_text(text, x + 8, y + 8, self.screen)

class Menu():
    def __init__(self, X, Y, screen):
        self.clock = pg.time.Clock()
        self.X = X
        self.Y =Y
        self.FPS = 10
        self.screen = screen
        self.menu = 0
        self.button = Buttons(850, 50, self.screen)
        self.fon = pg.image.load('fonn.jpeg')

    def main_menu(self):
        update_screen = 0
        while update_screen == 0:
            self.clock.tick(self.FPS)
            for event in pg.event.get():
                if event.type != pg.MOUSEBUTTONDOWN:
                    pg.display.update()
                if event.type == pg.MOUSEBUTTONDOWN:
                    update_screen = 1

                self.screen.blit(self.fon, (0, 0))
                self.button.draw_and_action(self.X / 8, self.Y / 4, L.zapp, 1)
                self.button.draw_and_action(self.X / 8, (self.Y / 4 + 50), L.zapz, 2)
                self.button.draw_and_action(self.X / 8, (self.Y / 4 + 110), L.zapn, 3)
                self.button.draw_and_action(self.X / 8, (self.Y / 4 + 160), L.nas, 4)
                self.button.draw_and_action(self.X / 8, (self.Y / 4 + 210), L.v, 5)
                print_text('Game of live', self.X / 4, self.Y / 10, self.screen)
        if self.button.regim == 1:
            self.menu = 1
        if self.button.regim == 2:
            self.menu = 2
        if self.button.regim == 3:
            self.menu = 3
        if self.button.regim == 4:
            self.Settings()
        if self.button.regim == 5:
            exit()

    def Settings(self):
        update_screen = 0
        while update_screen == 0:
            self.clock.tick(self.FPS)
            for event in pg.event.get():
                if event.type != pg.MOUSEBUTTONDOWN:
                    pg.display.update()
                if event.type == pg.MOUSEBUTTONDOWN:
                    update_screen = 1

                self.screen.blit(self.fon, (0, 0))
                self.button.draw_and_action(self.X / 8, self.Y / 4, L.naz, 6)
                self.button.draw_and_action(self.X / 8, (self.Y / 4 + 50), L.yz, 7)
                self.button.draw_and_action(self.X / 8, (self.Y / 4 + 110), L.s, 8)
                self.button.draw_and_action(self.X / 8, (self.Y / 4 + 160), L.zast, 9)
                self.button.draw_and_action(self.X / 8, (self.Y / 4 + 210), L.vcp, 10)
                print_text('Game of live', self.X / 4, self.Y / 10, self.screen)
        if self.button.regim == 6:
            self.main_menu()
        if self.button.regim == 7:
            self.Language()
        if self.button.regim == 8:
            self.Volume()
        if self.button.regim == 9:
            self.Fon()
        if self.button.regim == 10:
            self.Colour_of_pixels()

    def Language(self):
        update_screen = 0
        while update_screen == 0:
            self.clock.tick(self.FPS)
            for event in pg.event.get():
                if event.type != pg.MOUSEBUTTONDOWN:
                    pg.display.update()
                if event.type == pg.MOUSEBUTTONDOWN:
                    update_screen = 1

                self.screen.blit(self.fon, (0, 0))
                self.button.draw_and_action(self.X / 8, self.Y / 4, L.rus, 11)
                self.button.draw_and_action(self.X / 8, (self.Y / 4 + 50), L.eng, 12)
                self.button.draw_and_action(self.X / 8, (self.Y / 4 + 110), L.naz, 13)
                print_text('Game of live', self.X / 4, self.Y / 10, self.screen)
        if self.button.regim == 11:
            L.Russian()
            self.Language()
        if self.button.regim == 12:
            L.English()
            self.Language()
        if self.button.regim == 13:
            self.Settings()



    def Volume(self):
        update_screen = 0
        while update_screen == 0:
            self.clock.tick(self.FPS)
            for event in pg.event.get():
                if event.type != pg.MOUSEBUTTONDOWN:
                    pg.display.update()
                if event.type == pg.MOUSEBUTTONDOWN:
                    update_screen = 1

                self.screen.blit(self.fon, (0, 0))
                self.button.draw_and_action(self.X / 8, self.Y / 4, 'Включить звук', 14)
                self.button.draw_and_action(self.X / 8, (self.Y / 4 + 50), 'Выключить звук', 15)
                self.button.draw_and_action(self.X / 8, (self.Y / 4 + 110), 'Назад', 16)
                print_text('Game of live', self.X / 4, self.Y / 10, self.screen)
        if self.button.regim == 14:
            pg.mixer.music.play(-1)
            self.Volume()
        if self.button.regim == 15:
            pg.mixer.music.pause()
            self.Volume()
        if self.button.regim == 16:
            self.Settings()

    def Fon(self):
        update_screen = 0
        while update_screen == 0:
            self.clock.tick(self.FPS)
            for event in pg.event.get():
                if event.type != pg.MOUSEBUTTONDOWN:
                    pg.display.update()
                if event.type == pg.MOUSEBUTTONDOWN:
                    update_screen = 1

                self.screen.blit(self.fon, (0, 0))
                self.button.draw_and_action(self.X / 8, self.Y / 4, 'Красный', 17)
                self.button.draw_and_action(self.X / 8, (self.Y / 4 + 50), 'Синий', 181)
                self.button.draw_and_action(self.X / 8, (self.Y / 4 + 110), 'Зелёный', 182)
                self.button.draw_and_action(self.X / 8, (self.Y / 4 + 160), 'Жёлтый', 183)
                self.button.draw_and_action(self.X / 8, (self.Y / 4 + 210), 'Оранжевый', 184)
                self.button.draw_and_action(self.X / 8, (self.Y / 4 + 260), 'Белый', 185)
                self.button.draw_and_action(self.X / 8, (self.Y / 4 + 310), 'Назад', 19)
                print_text('Game of live', self.X / 4, self.Y / 10, self.screen)
        if self.button.regim == 17:
            #col_fon_game = RED
            self.Fon()
        if self.button.regim == 181:
            #col_fon_game = BLUE
            self.Fon()
        if self.button.regim == 182:
            #col_fon_game = GREEN
            self.Fon()
        if self.button.regim == 183:
            #col_fon_game = YELLOW
            self.Fon()
        if self.button.regim == 184:
            #col_fon_game = ORANGE
            self.Fon()
        if self.button.regim == 185:
            #col_fon_game = WHITE
            self.Fon()
        if self.button.regim == 19:
            self.Settings()

    def Colour_of_pixels(self):
        update_screen = 0
        while update_screen == 0:
            self.clock.tick(self.FPS)
            for event in pg.event.get():
                if event.type != pg.MOUSEBUTTONDOWN:
                    pg.display.update()
                if event.type == pg.MOUSEBUTTONDOWN:
                    update_screen = 1

                self.screen.blit(self.fon, (0, 0))
                self.button.draw_and_action(self.X / 8, self.Y / 4, 'Красный', 20)
                self.button.draw_and_action(self.X / 8, (self.Y / 4 + 50), 'Синий', 21)
                self.button.draw_and_action(self.X / 8, (self.Y / 4 + 110), 'Зелёный', 22)
                self.button.draw_and_action(self.X / 8, (self.Y / 4 + 160), 'Жёлтый', 23)
                self.button.draw_and_action(self.X / 8, (self.Y / 4 + 210), 'Оранжевый', 24)
                self.button.draw_and_action(self.X / 8, (self.Y / 4 + 260), 'Розовый', 25)
                self.button.draw_and_action(self.X / 8, (self.Y / 4 + 310), 'Назад', 26)
                print_text('Game of live', self.X / 4, self.Y / 10, self.screen)
        if self.button.regim == 20:
            ()
            self.Colour_of_pixels()
        if self.button.regim == 21:
            #col = GREEN
            self.Colour_of_pixels()
        if self.button.regim == 23:
            #col = YELLOW
            self.Colour_of_pixels()
        if self.button.regim == 24:
            #col = ORANGE
            self.Colour_of_pixels()
        if self.button.regim == 25:
            #col = PINK
            self.Colour_of_pixels()
        if self.button.regim == 26:
            self.Settings()
