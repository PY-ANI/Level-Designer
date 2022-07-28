# File explorer module 
from tkinter import filedialog as fd
import pygame
import os


class Option_tile(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        pass

# Text display class
class text_tile(pygame.sprite.Sprite):
    def __init__(self,text,key,x,y,size,bold,path=None):
        super().__init__()
        self.key = key
        self.text = text
        self.bold = bold
        self.size = size
        self.image = pygame.font.SysFont("comicon",size,bold).render(text,True,(160,160,220))
        self.rect = self.image.get_rect(topleft=(x,y))
        self.file_path = path
        self.default_pos = (x,y)

    def animate(self):
        self.image = pygame.font.SysFont("comicon",self.size,self.bold).render(self.text,True,(150,250,150))

    def draw(self,win):
        win.blit(self.image,self.rect)
        self.image = pygame.font.SysFont("comicon",self.size,self.bold).render(self.text,True,(150,150,250))
    
    def update(self,scroll_y):
        if (self.rect.y+scroll_y) <= self.default_pos[1]: self.rect.y+=scroll_y

# Main directory display function
class File_Explorer():
    def __init__(self,x,y,size_x,size_y,color):
        self.color = color
        self.path = None
        self.data = None
        self.first = True
        self.return_path = None
        self.return_animation_set = None
        self.scroll_y = 0
        self.dir_len = 0
        self.text_size = 25
        self.image = pygame.Surface((size_x,size_y))
        self.image.fill(self.color)
        self.rect = self.image.get_rect(topleft=(x,y))
    
    # Directory path input function
    def get_dir(self):
        self.path = fd.askdirectory()
        if self.path:
            self.data = {}
            self.load_dir(self.path,0)
    
    #Load animation dir
    def load_animation_dir(self):
        dir_path = fd.askdirectory()
        if dir_path:
            self.return_path = None
            self.return_animation_set = []
            for dir_contents in os.listdir(dir_path):
                if '.png' in dir_contents:
                    self.return_animation_set.append(os.path.join(dir_path,dir_contents))


    # loading directory to memory
    def load_dir(self,path,depth):
        for i in os.listdir(path):
            if '.png' in i:
                self.data[self.dir_len] = text_tile(i,self.dir_len,depth*10,10+self.dir_len*self.text_size,self.text_size,False,path+'/'+i)
                self.dir_len+=1
            elif '.' not in i:
                self.data[self.dir_len] = text_tile(i,"dir",depth*10,10+self.dir_len*self.text_size,self.text_size,True)
                self.dir_len+=1
                self.load_dir(path+"/"+i,depth+1)

    # Directory display funtion
    def draw_dir(self,dir):
        for i in dir.values():
            if i.rect.y in range(10,self.rect.bottom):
                if type(i.key) == int: pygame.draw.line(self.image,(100,100,100),(i.rect.x-5,i.rect.y),(i.rect.x-5,i.rect.y+20))
                i.draw(self.image)
            i.update(self.scroll_y)

    # Main display function
    def draw(self,win):
        win.blit(self.image,self.rect)
        Mouse = pygame.mouse.get_pos()
        if not self.data:
            self.image.fill((0,0,0))
            self.image.blit(pygame.font.SysFont("comicon",20).render("Click Here !!",True,(200,210,220)),(10,50))
        if self.data and self.first:
            self.image.fill((0,0,0))
            self.draw_dir(self.data)
            self.first = False
        elif self.rect.collidepoint(Mouse) and self.data:
            self.image.fill(self.color)
            self.draw_dir(self.data)
            self.selection(Mouse)
    
    # Mouse selection and action binding
    def selection(self,rect):
        for i in self.data.values():
            if i.rect.collidepoint(rect[0]-self.rect.x,rect[1]-self.rect.y):
                i.animate()
                if pygame.mouse.get_pressed()[0]:
                    self.return_animation_set = None
                    self.return_path = i.file_path
                return

    # Reset function
    def reset(self):
        self.path = None
        self.data = None
        self.first = True
        self.return_path = None
        self.scroll_y = 0
        self.dir_len = 0
        self.image.fill(self.color)
