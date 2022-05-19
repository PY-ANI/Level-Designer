# A level designer purely on python using pygame module for gui

import pygame
import pickle as pk
from tkinter import filedialog as fd
from basic_classes import *
from file_explorer_class import File_Explorer
from designer_screen import screen

pygame.init()

width,height = 1300,600
win = pygame.display.set_mode((width,height))
pygame.display.set_caption("Level_Designer","Level_Designer")

clock = pygame.time.Clock()

# class initialisations

dir_display = File_Explorer(1100,150,200,448,(50,50,50)) # Directory display class 
tile_screen = screen(0,0,1090,596,(200,200,200)) # Main tile screen class
util_disp = utility_hud(1100,0,200,130) # Option menu class
preview_display = preview(1200,10,100,100) # Preview class

mouse_scrl_x = 0
mouse_scrl_y = 0

m_x,m_y = 0,0

single_click = True

fps = 60
Mouse = None
run = False


while not run:
    clock.tick(fps)

    run = pygame.event.get(pygame.QUIT)

    dir_display.scroll_y = 0

    # Key bindings for Directory class and Option class

    event_1 = pygame.event.get(pygame.MOUSEBUTTONDOWN)
    if event_1:
        if dir_display.rect.collidepoint(event_1[0].pos):
            if not dir_display.path:
                dir_display.get_dir()

            if event_1[0].button == 4: dir_display.scroll_y = 20
            elif event_1[0].button == 5: dir_display.scroll_y = -20

        if util_disp.rect.collidepoint(event_1[0].pos) and event_1[0].button == 1:
            for i, val in util_disp.utilities.items():
                if val.rect.collidepoint((event_1[0].pos[0] - util_disp.rect.x, event_1[0].pos[1] - util_disp.rect.y)):
                    if i == 0:
                        dir_display.reset()
                        tile_screen.reset()
                        dir_display.get_dir()
                    if i == 1:
                        path = fd.askopenfilename(filetypes=[('pickle file','.pkl')])
                        if path:
                            tile_screen.reset()
                            with open(path,'rb') as fp:
                                tile_screen.return_sprite_list = pk.load(fp)
                            tile_screen.load_sprites()
                    if i == 2:
                        path = fd.asksaveasfilename(defaultextension='.json',filetypes=[('pickle file','.pkl')])
                        if path:
                            with open(path,'wb') as fp:
                                pk.dump(tile_screen.return_sprite_list,fp)


    win.fill((0,0,0))

    # Calling display funtions of classes

    dir_display.draw(win)
    tile_screen.draw(win)
    util_disp.draw(win)
    preview_display.draw(win,dir_display.return_path)

    # Key binding functions of tile screen

    Mouse = pygame.mouse.get_pos()
    if tile_screen.rect.collidepoint(Mouse):
        if dir_display.return_path and pygame.key.get_mods() & pygame.KMOD_CTRL and pygame.mouse.get_pressed()[0]:
            m_pos_x,m_pos_y = pygame.mouse.get_pos()
            tile_screen.get_sprite(m_pos_x,m_pos_y,dir_display.return_path)
        else:
            if single_click and pygame.mouse.get_pressed()[0]:
                single_click = False
                mouse_scrl_x,mouse_scrl_y = pygame.mouse.get_pos()

            if pygame.mouse.get_pressed()[0]:
                m_x,m_y = pygame.mouse.get_pos()
                tile_screen.scroll_x += (m_x-mouse_scrl_x)
                tile_screen.scroll_y += (m_y-mouse_scrl_y)
            else:
                single_click = True

        if pygame.mouse.get_pressed()[2]:
            Mouse = pygame.mouse.get_pos()
            tile_screen.delete_sprite(Mouse[0],Mouse[1])
        
        if event_1:
            if event_1[0].button == 4 and tile_screen.layer < 4:
                tile_screen.layer += 1
            if event_1[0].button == 5 and tile_screen.layer > 1:
                tile_screen.layer -= 1

    mouse_scrl_x = m_x
    mouse_scrl_y = m_y

    pygame.display.update()

pygame.quit()