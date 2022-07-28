# Basic class module for Preview class and Option class

import pygame
import time

class preview():
    def __init__(self,x,y,size_x,size_y):
        self.size_x = size_x
        self.size_y = size_y
        self.image = pygame.Surface((size_x,size_y))
        self.rect = self.image.get_rect(topleft = (x,y))
        self.frames = []
        self.frame_count = 0
        self.current_frame = 0
    
    def change_data(self,data):
        if type(data) == list:
            self.frames = data
        else:
            self.frames.clear()
            self.frames.append(data)
        self.frame_count = self.frames.__len__()
        self.last_time = time.time()
        self.current_frame = int((time.time()-self.last_time)%self.frame_count)

    def draw(self,win):
        win.blit(self.image,self.rect)

        win.blit(pygame.transform.scale(pygame.image.load(self.frames[self.current_frame]).convert_alpha(),(self.size_x,self.size_y)),self.rect)

        self.current_frame = time.time()-self.last_time
        if self.current_frame >= 60: self.last_time = time()

class utility_tile():
    def __init__(self,name,x,y,size):
        self.name = name
        self.size = size
        self.animate = False
        self.image_1 = pygame.font.SysFont("comicon",self.size,True).render(self.name,True,(180,180,180))
        self.image_2 = pygame.font.SysFont("comicon",self.size,True).render(self.name,True,(120,240,120))
        self.rect = self.image_1.get_rect(topleft=(x,y))

    def draw(self,win):
        if self.animate:
            win.blit(self.image_2,self.rect)
        else:
            win.blit(self.image_1,self.rect)


class utility_hud():
    def __init__(self,x,y,size_x,size_y):
        self.image = pygame.Surface((size_x,size_y))
        self.rect = self.image.get_rect(topleft=(x,y))
        self.utilities = {}
        self.first = True
        self.setup()

    def setup(self):
        self.utilities[0] = utility_tile("New",10,15,25)
        self.utilities[1] = utility_tile("Load",10,35,25)
        self.utilities[2] = utility_tile("Save",10,55,25)
        self.utilities[3] = utility_tile("Config",10,75,25)
        self.utilities[4] = utility_tile("animation",10,95,25)

    def draw(self,win):
        win.blit(self.image,self.rect)
        mouse = pygame.mouse.get_pos()
        if self.first or self.rect.collidepoint(mouse):
            if self.first: self.first = False
            self.image.fill((0,0,0))
            for i in self.utilities.values():
                if i.rect.collidepoint((mouse[0] - self.rect.x,mouse[1] - self.rect.y)):
                    i.animate = True
                i.draw(self.image)
                i.animate = False
