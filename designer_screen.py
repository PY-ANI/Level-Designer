# Main tile screen class module 

import pygame

#  sprite class
class sprite_tile():
    def __init__(self,x,y,size,surface_path=None):
        self.animate = False
        self.image = pygame.transform.scale(pygame.image.load(surface_path).convert_alpha(),(size,size))
        self.rect = self.image.get_rect(topleft=(x,y))

    def draw(self,win,sc_x,sc_y):
        win.blit(self.image,(self.rect.x+sc_x,self.rect.y+sc_y))

class character_sprite():
    def __init__(self,x,y,size,char_type):
        self.size = size
        self.char_type = char_type
        self.image = pygame.Surface((size,size))
        self.rect = self.image.get_rect(topleft = (x,y))
    
    def draw(self,win,sc_x,sc_y):
        if self.char_type == 'p': pygame.draw.circle(win,(0,200,0),(self.rect.centerx+sc_x,self.rect.centery+sc_y),self.size//4)
        else: pygame.draw.circle(win,(200,0,0),(self.rect.centerx+sc_x,self.rect.centery+sc_y),self.size//4)

# Main screen class contains all sprites
class screen():
    def __init__(self,x,y,size_x,size_y,color):
        self.image = pygame.Surface((size_x,size_y))
        self.rect = self.image.get_rect(topleft=(x,y))
        self.sprites = {}
        self.path = None
        self.return_sprite_list = {}
        self.first = True
        self.color = color
        self.sprite_size = 100
        self.scroll_x = 0
        self.scroll_y = 0
        self.layer = 1
        self.save_data_path = None

    # display function 
    def draw(self,win:pygame.Surface):
        win.blit(self.image,self.rect)
        if self.first or self.rect.collidepoint(pygame.mouse.get_pos()):
            if not self.first: self.first = False
            self.image.fill(self.color)
            for lyr in self.sprites.keys():
                for k_1, v_1 in self.sprites[lyr].items():
                    for k_2, v_2 in v_1.items():
                        if k_1+(self.scroll_y//self.sprite_size) in range(-1,(self.image.get_height()//self.sprite_size)+1) and k_2+(self.scroll_x//self.sprite_size) in range(-1,(self.image.get_width()//self.sprite_size)+1):
                            v_2.draw(win,self.scroll_x,self.scroll_y)
    
        self.image.blit(pygame.font.SysFont("comicon",20).render(f"X-offset : {self.scroll_x}, Y-offset : {self.scroll_y}, Layer : {self.layer}",True,(30,30,30)),(10,10))

    # sprite input function
    def get_sprite(self,pos_x:int,pos_y:int,surf_path:str|bytes,current_dir_path:str|bytes):
        pos_x -= self.scroll_x
        pos_y -= self.scroll_y
        k_x,k_y = pos_x//self.sprite_size,pos_y//self.sprite_size

        if self.layer not in self.sprites.keys():
            self.sprites[self.layer] = {}
            self.return_sprite_list[self.layer] = {}

        if k_y in self.sprites[self.layer].keys():
            if surf_path == 'p' or surf_path == 'e':
                self.sprites[self.layer][k_y][k_x] = character_sprite((pos_x-pos_x%self.sprite_size),(pos_y-pos_y%self.sprite_size),self.sprite_size,surf_path)
                self.return_sprite_list[self.layer][str(k_y)][str(k_x)] = surf_path
                return
            self.sprites[self.layer][k_y][k_x] = sprite_tile((pos_x-pos_x%self.sprite_size),(pos_y-pos_y%self.sprite_size),self.sprite_size,surf_path)
            self.return_sprite_list[self.layer][str(k_y)][str(k_x)] = surf_path.replace(current_dir_path+'/',"")
        else:
            if surf_path == 'p' or surf_path == 'e':
                self.sprites[self.layer][k_y] = {k_x:character_sprite((pos_x-pos_x%self.sprite_size),(pos_y-pos_y%self.sprite_size),self.sprite_size,surf_path)}
                self.return_sprite_list[self.layer][str(k_y)] = {str(k_x):surf_path}
                return
            self.sprites[self.layer][k_y] = {k_x:sprite_tile((pos_x-pos_x%self.sprite_size),(pos_y-pos_y%self.sprite_size),self.sprite_size,surf_path)}
            self.return_sprite_list[self.layer][str(k_y)] = {str(k_x):surf_path.replace(current_dir_path+'/',"")}

    # Sprite loading to main sprite dict funtion
    def load_sprites(self):
        for lyr in self.return_sprite_list.keys():
            self.sprites[lyr] = {}
            for y, val_1 in self.return_sprite_list[lyr].items():
                self.sprites[lyr][int(y)] = {}
                for x, val_2 in val_1.items():
                    if val_2 == 'p' or val_2 == 'e':
                        self.sprites[int(lyr)][int(y)][int(x)] = character_sprite(int(x)*self.sprite_size,int(y)*self.sprite_size,self.sprite_size,val_2)
                    else:
                        self.sprites[int(lyr)][int(y)][int(x)] = sprite_tile(int(x)*self.sprite_size,int(y)*self.sprite_size,self.sprite_size,self.save_data_path+val_2)

    # Sprite deletion function
    def delete_sprite(self,pos_x:int,pos_y:int):
        pos_x -= self.scroll_x
        pos_y -= self.scroll_y
        pos_x,pos_y = pos_x//self.sprite_size,pos_y//self.sprite_size
        
        if pos_y in self.sprites[self.layer].keys() and pos_x in self.sprites[self.layer][pos_y].keys():
            self.sprites[self.layer][pos_y].pop(pos_x)
            self.return_sprite_list[self.layer][str(pos_y)].pop(str(pos_x))


    # reset function
    def reset(self):
        self.sprites.clear()
        self.return_sprite_list.clear()
        self.scroll_x = 0
        self.scroll_y = 0
        self.first = True
