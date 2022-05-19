# Main tile screen class module 

import pygame

#  sprite class
class sprite_tile(pygame.sprite.Sprite):
    def __init__(self,x,y,size,surface_path=None):
        super().__init__()
        self.animate = False
        self.image = pygame.transform.scale(pygame.image.load(surface_path).convert_alpha(),(size,size))
        self.rect = self.image.get_rect(topleft=(x,y))

# Main screen class contains all sprites
class screen(pygame.sprite.Sprite):
    def __init__(self,x,y,size_x,size_y,color):
        super().__init__()
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
                            self.image.blit(v_2.image,(v_2.rect.x+self.scroll_x,v_2.rect.y+self.scroll_y))
    
        self.image.blit(pygame.font.SysFont("comicon",20).render(f"X-offset : {self.scroll_x}, Y-offset : {self.scroll_y}, Layer : {self.layer}",True,(30,30,30)),(10,10))

    # sprite input function
    def get_sprite(self,pos_x:int,pos_y:int,surf_path:str|bytes):
        pos_x -= self.scroll_x
        pos_y -= self.scroll_y
        k_x,k_y = pos_x//self.sprite_size,pos_y//self.sprite_size

        if self.layer not in self.sprites.keys():
            self.sprites[self.layer] = {}
            self.return_sprite_list[self.layer] = {}

        if k_y in self.sprites[self.layer].keys():
            self.sprites[self.layer][k_y][k_x] = sprite_tile((pos_x-pos_x%self.sprite_size),pos_y-pos_y%self.sprite_size,self.sprite_size,surf_path)
            self.return_sprite_list[self.layer][str(k_y)][str(k_x)] = surf_path
        else:
            self.sprites[self.layer][k_y] = {k_x:sprite_tile((pos_x-pos_x%self.sprite_size),pos_y-pos_y%self.sprite_size,self.sprite_size,surf_path)}
            self.return_sprite_list[self.layer][str(k_y)] = {str(k_x):surf_path}

    # Sprite loading to main sprite dict funtion
    def load_sprites(self):
        for lyr in self.return_sprite_list.keys():
            self.sprites[lyr] = {}
            for y, val_1 in self.return_sprite_list[lyr].items():
                self.sprites[lyr][int(y)] = {}
                for x, val_2 in val_1.items():
                    self.sprites[lyr][int(y)][int(x)] = sprite_tile(int(x)*self.sprite_size,int(y)*self.sprite_size,self.sprite_size,val_2) 

    # Sprite deletion function
    def delete_sprite(self,pos_x:int,pos_y:int):
        pos_x -= self.scroll_x
        pos_y -= self.scroll_y
        pos_x,pos_y = pos_x//self.sprite_size,pos_y//self.sprite_size
        try:
            self.sprites[self.layer][pos_y].pop(pos_x)
            self.return_sprite_list[self.layer][pos_y].pop(pos_x)
        except:
            pass
    
    # reset function
    def reset(self):
        self.sprites.clear()
        self.return_sprite_list.clear()
        self.scroll_x = 0
        self.scroll_y = 0
        self.first = True
        self.sprite_size = 100
