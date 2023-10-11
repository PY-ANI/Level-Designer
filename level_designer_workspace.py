from level_designer_dtype import *

class label:
    def __init__(self, win, text:str, color:tuple[int,int,int], size:int, pos:tuple[int,int], is_center:bool=False):
        self.win = win
        self.surf = pygame.font.SysFont("comicsans", size, True).render(text, True, color)
        self.rect = self.surf.get_rect(center=pos) if is_center else self.surf.get_rect(topleft=pos)
    
    def draw(self):
        self.win.blit(self.surf, self.rect)

class designer_workspace:
    def __init__(self, win, width, height, pos, flags, keystate, config, **kargs):
        self.win = win
        self.flags = flags
        self.keystate = keystate
        self.config = config
        self.foreignfunc = kargs['func'] if kargs and kargs.get("func") else None

        self.surface = pygame.Surface((width,height))
        self.rect = self.surface.get_rect(topleft=pos)

        self.head_font_kernel = pygame.font.SysFont("comicsans",30,True)
        self.body_font_kernel = pygame.font.SysFont("comicsans",14,True)

        self.buttons = [
            Button(self.surface,120,30,(self.rect.w//2,260),"New Project",center=True,func=self.create_new_project),
            Button(self.surface,80,30,(self.rect.w//2+30,250),"Browse",func=self.browse),
            Button(self.surface,20,10,(self.rect.w//2-25,400),"X+",center=True,func=lambda:self.update_tile_size((1,0))),
            Button(self.surface,20,10,(self.rect.w//2+25,400),"X-",center=True,func=lambda:self.update_tile_size((-1,0))),
            Button(self.surface,20,10,(self.rect.w//2,375),"Y+",center=True,func=lambda:self.update_tile_size((0,1))),
            Button(self.surface,20,10,(self.rect.w//2,425),"Y-",center=True,func=lambda:self.update_tile_size((0,-1))),
            Button(self.surface,100,30,(self.rect.w//2-60,600),"Cancel",center=True,func=self.cancle),
            Button(self.surface,100,30,(self.rect.w//2+60,600),"Apply",center=True,func=self.apply),
        ]

        self.labels = [
            label(self.surface, "Project Directory -", (200,200,200), 20, (self.rect.w//2-160,260), True),
            label(self.surface, "Tile Dimension -", (200,200,200), 20, (self.rect.w//2-160,400), True),
        ]

        self.head_surf = self.head_font_kernel.render("Level Designer", True, (200,200,200))
        self.head_rect = self.head_surf.get_rect(center=(self.rect.w//2,60))

        self.setup_project_config = False

    def draw(self):
        self.win.blit(self.surface, self.rect)

    def update(self):
        self.surface.fill((40,40,40))

        self.surface.blit(self.head_surf, self.head_rect)

        if self.setup_project_config:
            
            self.surface.blit(self.body_font_kernel.render(self.config["dir_path"],True,(100,100,100)), (self.rect.w//2-10,280))
            self.surface.blit(self.body_font_kernel.render(f"X:{self.config['tile_size'][0]}, Y:{self.config['tile_size'][1]}",True,(100,100,100)), (self.rect.w//2+60,390))

            for label in self.labels:
                label.draw()
            
            for btn in self.buttons[1:]:
                btn.draw()
                if self.keystate["mouse_click"] and self.keystate["mouse_click"][0].button == 1 and btn.rect.collidepoint(self.keystate["mouse_pos"]): btn.action()

        else:
            for btn in self.buttons[:1]:
                btn.draw()
                if self.keystate["mouse_click"] and self.keystate["mouse_click"][0].button == 1 and btn.rect.collidepoint(self.keystate["mouse_pos"]): btn.action()
    
    def create_new_project(self):
        self.setup_project_config = True
        self.config["setup_mode"] = "create"
    
    def load_project(self):
        self.setup_project_config = True
        self.config["setup_mode"] = "load"
    
    def apply(self):
        if self.config["dir_path"]:
            self.flags["startup"] = False
            self.setup_project_config = False
            self.config["sprite_dir"] = os.path.join(self.config["dir_path"],"sprites")
            self.config["animated_sprite_dir"] = os.path.join(self.config["dir_path"],"animated")
            if self.foreignfunc != None: self.foreignfunc()

    def cancle(self):
        self.setup_project_config = False
    
    def browse(self):
        self.config["dir_path"] = askdirectory(title="Select Project Directory -",mustexist=True)
    
    def update_tile_size(self,deltasize:tuple[int, int]):
        self.config["tile_size"][0] += deltasize[0]
        self.config["tile_size"][1] += deltasize[1]
    