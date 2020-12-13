

import numpy as np
import pygame as pg
from Game_languages import Languages


WHITE = (255, 255, 255)
RED = (225, 0, 50)
BLACK = (0, 0, 0)
lightBLACK = (3, 3, 3)
lightGreen = (0, 255, 0)
BLUE = (0, 0, 255, 20)
GRAY = (125, 125, 125)
lightBlue = (64, 128, 255)
GREEN = (0, 200, 64, 20)
YELLOW = (225, 225, 0, 2)
PINK = (230, 50, 230, 0)
ORANGE = (255, 165, 0)

L=Languages(1)
L.Russian()
L.Sound(1)



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


    def no_action_button(self, x, y, text):
        print_text(text, x + 8, y + 8, self.screen)

    def no_action_button_color(self, x, y, text):
        pg.draw.rect(self.screen, (30, 150, 100), (x, y, self.width, self.height))
        print_text(text, x + 8, y + 8, self.screen)


class Menu():
    def __init__(self, X, Y, screen):
        self.clock = pg.time.Clock()
        self.X = X
        self.Y =Y
        self.FPS = 9000
        self.screen = screen
        self.menu = 0
        self.button = Buttons(850, 50, self.screen)
        self.button_no_action = Buttons(150, 150, self.screen)
        self.fon = pg.image.load('fonn.jpeg')
        self.col = RED
        self.col_fon_game = WHITE
        self.Chcolfon = L.wit
        self.Chcolpx = L.red

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
                self.button_no_action.no_action_button(self.X / 8, (self.Y - 100), L.chlan)
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
                self.button.draw_and_action(self.X / 8, self.Y / 4, L.tons, 14)
                self.button.draw_and_action(self.X / 8, (self.Y / 4 + 50), L.toffs, 15)
                self.button.draw_and_action(self.X / 8, (self.Y / 4 + 110), L.naz, 16)
                self.button_no_action.no_action_button(self.X / 8, (self.Y - 100), L.sound)
                print_text('Game of live', self.X / 4, self.Y / 10, self.screen)
        if self.button.regim == 14:
            L.Sound(1)
            L.regim_of_sound = 1
            pg.mixer.music.play(-1)
            self.Volume()
        if self.button.regim == 15:
            L.Sound(0)
            L.regim_of_sound = 0
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
                self.button.draw_and_action(self.X / 8, self.Y / 4, L.red, 17)
                self.button.draw_and_action(self.X / 8, (self.Y / 4 + 50), L.blue, 181)
                self.button.draw_and_action(self.X / 8, (self.Y / 4 + 110), L.green, 182)
                self.button.draw_and_action(self.X / 8, (self.Y / 4 + 160), L.yel, 183)
                self.button.draw_and_action(self.X / 8, (self.Y / 4 + 210), L.wit, 184)
                self.button.draw_and_action(self.X / 8, (self.Y / 4 + 260), L.naz, 19)
                self.button_no_action.no_action_button(self.X / 8, (self.Y - 100), (L.chcol + ' ' + L.COLF))
                print_text('Game of live', self.X / 4, self.Y / 10, self.screen)
        if self.button.regim == 17:
            self.col_fon_game = RED
            L.COLF = L.red
            self.Fon()
        if self.button.regim == 181:
            self.col_fon_game = BLUE
            L.COLF = L.blue
            self.Fon()
        if self.button.regim == 182:
            self.col_fon_game = GREEN
            L.COLF = L.green
            self.Fon()
        if self.button.regim == 183:
            self.col_fon_game = YELLOW
            L.COLF = L.yel
            self.Fon()
        if self.button.regim == 184:
            self.col_fon_game = WHITE
            L.COLF = L.wit
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
                self.button.draw_and_action(self.X / 8, self.Y / 4, L.red, 1)
                self.button.draw_and_action(self.X / 8, (self.Y / 4 + 50), L.blue, 2)
                self.button.draw_and_action(self.X / 8, (self.Y / 4 + 110), L.green, 3)
                self.button.draw_and_action(self.X / 8, (self.Y / 4 + 160), L.yel, 4)
                self.button.draw_and_action(self.X / 8, (self.Y / 4 + 210), L.pink, 5)
                self.button.draw_and_action(self.X / 8, (self.Y / 4 + 260), L.naz, 6)
                self.button_no_action.no_action_button(self.X / 8, (self.Y - 100), (L.chcol + ' ' + L.COLP))
                print_text('Game of live', self.X / 4, self.Y / 10, self.screen)
        if self.button.regim == 1:
            self.col = RED
            L.COLP = L.red
            self.Colour_of_pixels()
        if self.button.regim == 2:
            self.col = BLUE
            L.COLP = L.blue
            self.Colour_of_pixels()
        if self.button.regim == 3:
            self.col = GREEN
            L.COLP = L.green
            self.Colour_of_pixels()
        if self.button.regim == 4:
            self.col = YELLOW
            L.COLP = L.yel
            self.Colour_of_pixels()
        if self.button.regim == 5:
            self.col = PINK
            L.COLP = L.pink
            self.Colour_of_pixels()
        if self.button.regim == 6:
            self.Settings()
