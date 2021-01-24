"""

Игра Жизнь

Правая кнопка мыши - добавить клетку;
Левая кнопка мыши - перемещение изображения;
Колесико мыши - изменить масштаб;
Пробел - пауза;
Escape - выход в меню.

"""

import numpy as np
import pygame as pg

from game_functions import Game_functions
from Menu_of_game import Menu


def count_period(t, fps):
    return round(fps / t)

def life_loop(X, Y, game, M, screen):
    
    start_FPS = 60
    max_FPS = 250
    Trun = 60
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
    
    game.setup(M.menu)
    if game.live == 0:
        return 'menu'
    
    pg.display.update()
    clock = pg.time.Clock()
    FPS = start_FPS

    while not finished:
        counter += 1
        period_run = count_period(Trun, FPS)
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
                if event.button == 4:
                    scroll_up = 1
                    
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    play1 = not play1
                elif event.key == pg.K_ESCAPE:
                    window = 'menu'
                    finished = True
                elif event.key == pg.K_s:
                    game.download()
           
        if scroll_down:
            x, y = pg.mouse.get_pos()
            game.change_index_bias(x, y)
            game.x_screen_bias, game.y_screen_bias = x, y
            game.scale = np.round(max(game.scale * 0.9, 0.5), 2)
            scroll_down = 0
            
        if scroll_up:
            x, y = pg.mouse.get_pos()
            game.change_index_bias(x, y)
            game.x_screen_bias, game.y_screen_bias = x, y
            game.scale = np.round(min(game.scale * 1.1, 50), 2)
            scroll_up = 0
        
        if track_mouse == 1:
            x_cur, y_cur = pg.mouse.get_pos()
            game.x_screen_bias += x_cur - x_start
            game.y_screen_bias += y_cur - y_start
            x_start, y_start = x_cur, y_cur
        
        if paint and (not play1 or not play2):
            game.adjust_field()
            x_paint , y_paint = pg.mouse.get_pos()
            game.add_cell(x_paint, y_paint)
            
        if counter % period_run == 0 and play1 and play2:
            game.run()
        if counter % period_show == 0:
            game.draw_life(M.col, screen)
            if game.scale > 3.5:
                game.draw_grid(M.col, screen)
            pg.display.update()
            screen.fill(M.col_fon_game)
    return window

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
    
    M = Menu(X, Y, screen)
    game = Game_functions(X, Y)

    while Play:
        if window == 'menu':
            window = M.main_menu()
        elif window == 'life':
            window = life_loop(X, Y, game, M, screen)
        else:
            Play = False
    pg.quit()

if __name__ == '__main__':
    main()

