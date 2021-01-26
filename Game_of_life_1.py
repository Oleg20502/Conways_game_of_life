"""

Игра Жизнь

Правая кнопка мыши - добавить клетку;
Левая кнопка мыши - перемещение изображения;
Колесико мыши - изменить масштаб;
Пробел - пауза;
Клавиша C - очистить поле;
Клавиша S - сохранить поле клеток в файл;
Escape - выход в меню.

"""

import pygame as pg

from game_functions import Game_functions
from Game_menu import Menu


def main():
    X, Y = 1000, 550
    window = 'menu'
    Play = True
    
    pg.init()
    screen = pg.display.set_mode((X, Y))
    pg.display.set_caption("Conway's Game Of Life")
    pg.mixer.music.load('sound in menu.ogg')
    pg.mixer.music.set_volume(0.01)
    pg.mixer.music.play(-1)
    
    game = Game_functions(X, Y, screen)
    M = Menu(X, Y, screen, game)

    while Play:
        if window == 'menu':
            window = M.main_menu()
        elif window == 'life':
            window = game.life_loop()
        else:
            Play = False
    pg.quit()

if __name__ == '__main__':
    main()

