# A level designer purely on python using pygame module for gui

import pygame
import pickle as pk
import json
from tkinter import filedialog as fd
from basic_classes import *
from file_explorer_class import File_Explorer
from designer_screen import screen
import os

# loading config data to global variables
with open("config.json","rb") as f:
    data = json.load(f)
    width,height,tile_size = data["width"],data["height"],data["tile_size"]

pygame.init()

win = pygame.display.set_mode((width,height))
pygame.display.set_caption("Level_Designer","Level_Designer")

clock = pygame.time.Clock()

# class initialisations
tile_screen = screen(0,0,int(width*0.8),height,(200,200,200)) # Main tile screen class
util_disp = utility_hud(int(width*0.8),0,int(width*0.2),int(height*0.25)) # Option menu class
dir_display = File_Explorer(int(width*0.8),int(height*0.25),int(width*0.2),int(height*0.75),(50,50,50)) # Directory display class 
preview_display = preview(int(width*0.88),0,int(width*0.10),int(width*0.10)) # Preview class

tile_screen.sprite_size = tile_size

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

            if event_1[0].button == 4: dir_display.scroll_y = 40
            elif event_1[0].button == 5: dir_display.scroll_y = -40

        if util_disp.rect.collidepoint(event_1[0].pos) and event_1[0].button == 1:
            for i, val in util_disp.utilities.items():
                if val.rect.collidepoint((event_1[0].pos[0] - util_disp.rect.x, event_1[0].pos[1] - util_disp.rect.y)):
                    if i == 0:
                        dir_display.reset()
                        tile_screen.reset()
                        dir_display.get_dir()
                    elif i == 1:
                        path = fd.askopenfilename(filetypes=[('pickle file','.pkl')])
                        if path:
                            tile_screen.reset()
                            tile_screen.save_data_path = path.strip(path.split('/')[-1])
                            with open(path,'rb') as fp:
                                tile_screen.return_sprite_list = pk.load(fp)
                            tile_screen.load_sprites()
                    elif i == 2:
                        path = fd.asksaveasfilename(defaultextension='.json',filetypes=[('pickle file','.pkl')])
                        if path:
                            with open(path,'wb') as fp:
                                pk.dump(tile_screen.return_sprite_list,fp)
                    elif i == 3:
                        os_name = os.name
                        if os_name == 'nt':
                            os.system("notepad.exe config.json")
                        elif os_name == 'posix':
                            os.system("nano config.json")
                    elif i == 4 and dir_display.path:
                        dir_display.load_animation_dir()
                        preview_display.change_data(dir_display.return_animation_set)

    # Key binding functions of tile screen
    Mouse = pygame.mouse.get_pos()
    
    if tile_screen.rect.collidepoint(Mouse):
        
        if pygame.key.get_mods() & pygame.KMOD_CTRL and pygame.mouse.get_pressed()[0]:
            
            if dir_display.return_animation_set:
                m_pos_x,m_pos_y = pygame.mouse.get_pos()
                tile_screen.get_sprite(m_pos_x,m_pos_y,dir_display.return_animation_set,dir_display.path)
            
            elif dir_display.return_path:
                m_pos_x,m_pos_y = pygame.mouse.get_pos()
                tile_screen.get_sprite(m_pos_x,m_pos_y,dir_display.return_path,dir_display.path)
            
        elif pygame.key.get_mods() & pygame.KMOD_LSHIFT and pygame.mouse.get_pressed()[0]:
            m_pos_x,m_pos_y = pygame.mouse.get_pos()
            tile_screen.get_sprite(m_pos_x,m_pos_y,'p',None)
        
        elif pygame.key.get_mods() & pygame.KMOD_LSHIFT and pygame.mouse.get_pressed()[2]:
            m_pos_x,m_pos_y = pygame.mouse.get_pos()
            tile_screen.get_sprite(m_pos_x,m_pos_y,'e',None)
        
        elif pygame.mouse.get_pressed()[2]:
            Mouse = pygame.mouse.get_pos()
            tile_screen.delete_sprite(Mouse[0],Mouse[1])
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

        if event_1:
            if event_1[0].button == 4 and tile_screen.layer < 4:
                tile_screen.layer += 1
            if event_1[0].button == 5 and tile_screen.layer > 1:
                tile_screen.layer -= 1

    mouse_scrl_x = m_x
    mouse_scrl_y = m_y

    win.fill((0,0,0))

    # Calling display funtions of classes
    tile_screen.draw(win)
    dir_display.draw(win)
    util_disp.draw(win)

    if dir_display.return_path:
        preview_display.change_data(dir_display.return_path)
        preview_display.draw(win)
    elif dir_display.return_animation_set:
        preview_display.draw(win)


    pygame.display.update()

pygame.quit()