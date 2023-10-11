import os
import pygame
from time import time
# from pprint import pprint
from json import load, dump
from tkinter.filedialog import asksaveasfilename, askdirectory, askopenfile


# utility  functions
def sub_tuple(tuple1:tuple, tuple2:tuple):
    return map(lambda a,b:a-b, tuple1, tuple2)

def add_tuple(tuple1:tuple, tuple2:tuple):
    return map(lambda a,b:a+b, tuple1, tuple2)

def mul_tuple(tuple1:tuple, tuple2:tuple):
    return map(lambda a,b:a*b, tuple1, tuple2)

def div_tuple(tuple1:tuple, tuple2:tuple):
    return map(lambda a,b:a/b, tuple1, tuple2)

def abs_div_tuple(tuple1:tuple, tuple2:tuple):
    return map(lambda a,b:a/b, tuple1, tuple2)


# utility classes
class sprite:
    def __init__(self, sprite_type, sprite):
        self.sprite_type = sprite_type
        self.sprite = sprite
        self.is_animated = sprite_type == "Animated"

class Button:
    def __init__(self, window, width, height, pos, btn_name, func = lambda:print("yes"), center=False):
        self.window = window
        self.font_surf = pygame.font.SysFont("arial", 20, True).render(btn_name, True, (150, 150, 150))
        self.surface = pygame.Surface((max(self.font_surf.get_width(), width), max(self.font_surf.get_height(), height)))
        self.rect = self.surface.get_rect(center=pos) if center else self.surface.get_rect(topleft=pos)
        self.font_rect = self.font_surf.get_rect(center=(self.surface.get_width()//2, self.surface.get_height()//2))
        self.action = func
    
        self.update()

    def draw(self):
        self.window.blit(self.surface, self.rect)
    
    def update(self):
        self.surface.fill((80,80,80))
        self.surface.blit(self.font_surf, self.font_rect)

class Switch:
    def __init__(self, window, width, height, pos, btn_name):
        self.window = window
        self.text = btn_name
        self.font_surf = pygame.font.SysFont("arial", 20, True).render(btn_name, True, (150, 150, 150))
        self.surface = pygame.Surface((max(self.font_surf.get_width(), width), max(self.font_surf.get_height(), height)))
        self.rect = self.surface.get_rect(topleft=pos)
        self.font_rect = self.font_surf.get_rect(center=(self.surface.get_width()//2, self.surface.get_height()//2))
    
    def draw(self):
        self.window.blit(self.surface, self.rect)
    
    def switch(self, on):
        if on: self.surface.fill((60,60,60))
        else: self.surface.fill((80,80,80))
        self.surface.blit(self.font_surf, self.font_rect)