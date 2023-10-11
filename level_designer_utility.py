from level_designer_workspace import *

class Popup(pygame.Surface):
    def __init__(self,win,window_size,pos):
        super().__init__(window_size)
        self.window = win
        self.rect = self.get_rect(topleft=pos)

        self.close_btn_rect = pygame.Rect(window_size[0]-20,0,20,20)

class SubWindow:
    def __init__(self, win, window_size, pos):
        self.win = win
        self.surface = pygame.Surface(window_size)
        self.rect = self.surface.get_rect(topleft=pos)

        self.close_btn_rect = pygame.Rect(window_size[0]-20,0,20,20)

class preview:
    def __init__(self, window, width, height, pos, flags, assets):
        self.window = window
        self.flags = flags
        self.assets = assets
        self.img_width = int(width*.8)
        self.img_height = int(height*.8)
        self.img_pos = pos[0]+int(width*.1), pos[1]+int(height*.1)
        self.rect = pygame.Rect(pos[0], pos[1], width, height)

        self.image = None

        # debug
        self.font_kernel = pygame.font.SysFont("comicsans",20,True)

    def draw(self):
        pygame.draw.rect(self.window, (60, 60, 60), self.rect, 2)
        if self.image:
            self.window.blit(self.image, self.img_pos)
    
    def update(self, frame = 0):
        if self.flags["tile_type"] == "Normal" and self.flags["selected"]:
            self.image = pygame.transform.scale(self.assets[self.flags['tile_type']][self.flags["selected"]], (self.img_width, self.img_height))
        elif self.flags["tile_type"] == "Animated" and self.flags["selected"]:
            animation_buffer = self.assets[self.flags["tile_type"]][self.flags["selected"]]
            self.image = pygame.transform.scale(animation_buffer[frame%animation_buffer.__len__()], (self.img_width, self.img_height))

class dir_navigator:
    def __init__(self, window, width, height, pos, title, flags, keystate, assets):
        self.window = window
        self.flags = flags
        self.keystate = keystate
        self.assets = assets
        self.title = pygame.font.SysFont("comicsans",20,True).render(title, True, (150,150,150))
        self.title_rect = self.title.get_rect(center=(width//2, self.title.get_height()//2))
        self.surface = pygame.Surface((width, height+self.title.get_height()))
        self.rect = self.surface.get_rect(topleft=pos)
        self.font_kernel = pygame.font.SysFont("comicsans",14,True)

        self.max_y = height//22-1
        self.shift_y = {"Normal":0, "Animated":0}

    def draw(self):
        self.surface.fill((60,60,60))
        self.surface.blit(self.title, self.title_rect)

        if dirs := self.assets.get(self.flags["tile_type"]):
            for i in range(min(dirs["dirs"].__len__(), self.max_y+1)):
                if dirs["dirs"][i-self.shift_y[self.flags['tile_type']]] == self.flags["selected"]: pygame.draw.rect(self.surface,(70,70,70),(2,30+22*i,self.rect.w-4,22),2)
                self.surface.blit(self.font_kernel.render(dirs["dirs"][i-self.shift_y[self.flags['tile_type']]],True,(200,200,200)), (10,30+22*i))
            
            if self.rect.collidepoint(self.keystate["rel_mouse_pos"]):
                if key := self.keystate["scroll"]:
                    if key[0].y > 0 and self.shift_y[self.flags['tile_type']]:
                        self.shift_y[self.flags['tile_type']] += key[0].y
                    elif key[0].y < 0 and len(dirs["dirs"][self.shift_y[self.flags['tile_type']]:]) > self.max_y:
                        self.shift_y[self.flags['tile_type']] += key[0].y


                shift_pos = tuple(sub_tuple(self.keystate["rel_mouse_pos"],self.rect.topleft))
                if self.keystate["mouse_click"] and self.keystate["mouse_click"][0].button == 1 and shift_pos[1] > 30:
                    try:
                        self.flags["selected"] = dirs["dirs"][(shift_pos[1]-30)//22-self.shift_y[self.flags['tile_type']]]
                    except IndexError as _: ...

        self.window.blit(self.surface, self.rect)

class toolbar:
    def __init__(self, window, width, height, pos, keystate, flags, assets, map_dict, layers, config):
        self.window = window
        self.surface = pygame.Surface((width, height))
        self.rect = self.surface.get_rect(topleft=pos)
        self.head_font_kernel = pygame.font.SysFont("comicsans",20,True)
        self.body_font_kernel = pygame.font.SysFont("comicsans",14,True)

        self.keystate = keystate
        self.flags = flags
        self.map_dict = map_dict
        self.layers = layers
        self.config = config

        self.assets_cache = assets
        self.assets = {
            "Normal": {},
            "Animated": {},
        }

        self.subwindow = SubWindow(self.window, (400, 500), (300, 100))
        self.popup = Popup(self.window, (400,200), (300,100))

        self.preview = preview(self.surface, width, width//2, (0, 130), self.flags, self.assets_cache)
        self.dir_list_navbar = dir_navigator(self.surface, width, 200, (0, self.preview.rect.bottom+31), "Assets", self.flags, self.keystate, self.assets)

        self.switchs = [
            Switch(self.surface, 100, 30, (0, self.preview.rect.bottom+1), "Normal"),
            Switch(self.surface, 100, 30, (100, self.preview.rect.bottom+1), "Animated"),
        ]
    
        self.buttons = [
            Button(self.surface, 196, 30, (2, 2), "Export", self.export_map),
            Button(self.surface, 96, 30, (2, 34), "+ Layer", self.layer_configure),
            Button(self.surface, 96, 30, (102, 34), "- Layer", self.remove_layer),
            Button(self.surface, 196, 30, (2, 66), "Preview"),
            Button(self.surface, 96, 30, (2, 98), "Reload Dir",self.load_n_cache_assets),
            Button(self.surface, 96, 30, (102, 98), "Load Map",self.import_map),
        ]
    
        # self.font_kernel = pygame.font.SysFont("comicsans",12,True)

        # self.load_n_cache_assets()

    def draw(self):
        self.surface.fill((100, 100, 100))

        for btn in self.buttons:
            btn.draw()
            if btn.rect.collidepoint(self.keystate["rel_mouse_pos"]):
                pygame.draw.rect(self.surface, (70,70,70), btn.rect, 3)
                if self.keystate["mouse_click"] and self.keystate["mouse_click"][0].button == 1: btn.action()
        
        self.preview.draw()

        for switch in self.switchs:
            if self.keystate["mouse_click"] and self.keystate["mouse_click"][0].button == 1 and switch.rect.collidepoint(self.keystate["rel_mouse_pos"]): self.flags["tile_type"] = switch.text; self.flags["selected"] = None
            if self.flags["tile_type"] == switch.text: switch.switch(True)
            else: switch.switch(False)
            switch.draw()
        
        self.dir_list_navbar.draw()

        self.window.blit(self.surface, self.rect)
    
    def update(self, frame = 0):
        self.preview.update(frame)
        ...

    def load_n_cache_assets(self):
        d_tree = list(os.walk(self.config["sprite_dir"]))
        for root,_,files in d_tree:
            for file in files:
                self.assets["Normal"][os.path.join(root.split("\\")[-1], file)] = os.path.join(root.removeprefix(self.config["dir_path"]+"\\"), file)
        self.assets["Normal"]["dirs"] = list(self.assets["Normal"].keys())
        del d_tree
        d_tree = list(os.walk(self.config["animated_sprite_dir"]))
        for root,_,files in d_tree:
            if files:
                self.assets["Animated"][root.split("\\")[-1]] = list(map(lambda file: os.path.join(root.removeprefix(self.config["dir_path"]+"\\"), file), files))
        self.assets["Animated"]["dirs"] = list(self.assets["Animated"].keys())
    
        for key, value in self.assets["Normal"].items():
            if key != "dirs":
                self.assets_cache["Normal"][key] = self.get_surface(os.path.join(self.config["dir_path"], value))
        for key, value in self.assets["Animated"].items():
            if key != "dirs":
                self.assets_cache["Animated"][key] = list(map(lambda file: self.get_surface(os.path.join(self.config["dir_path"], file)), value))
    
    def get_surface(self,path):
        return pygame.image.load(path).convert_alpha()
    
    def layer_configure(self):

        flags = {
            "name":"",
            "pos":1
        }

        text_input = pygame.Rect(140,70,200,40)
        switchs = [
            Switch(self.subwindow.surface, 100, 30, (40, 180), "Before"),
            Switch(self.subwindow.surface, 100, 30, (140, 180), "After"),
        ]
        apply_btn = Button(self.subwindow.surface,80,30,(160,460),"Apply",self.add_layer)


        is_textinput_on = False
        popup_loop = True
        while popup_loop:
            
            mouse_pos = tuple(sub_tuple(pygame.mouse.get_pos(), self.subwindow.rect.topleft))
            mouse_click = pygame.event.get(pygame.MOUSEBUTTONDOWN)
            key_down = pygame.event.get(pygame.KEYDOWN)
            
            if mouse_click and mouse_click[0].button == 1:
                if self.subwindow.close_btn_rect.collidepoint(mouse_pos):
                    popup_loop = False
                elif text_input.collidepoint(mouse_pos):
                    is_textinput_on = True
                else:
                    is_textinput_on = False
            
            if key_down and is_textinput_on:
                if key_down[0].key in range(97,123) or key_down[0].key in range(48,58):
                    flags["name"] += chr(key_down[0].key - 32 if key_down[0].mod in (1, 2, 8192) else key_down[0].key)
                elif key_down[0].key == 8:
                    flags["name"] = flags["name"][:-1]

            self.subwindow.surface.fill((100,100,100))
            self.subwindow.surface.blit(self.head_font_kernel.render("Layer Config",True,(200,200,200)), (10,0))

            self.subwindow.surface.blit(self.body_font_kernel.render("Layer Name :-",True,(200,200,200)), (20,80))
            self.subwindow.surface.blit(self.body_font_kernel.render(flags["name"],True,(200,200,200)),(text_input.x+2,text_input.y+10))
            pygame.draw.rect(self.subwindow.surface, (60,160,60) if is_textinput_on else(60,60,60), text_input, 2, 4)
            self.subwindow.surface.blit(self.body_font_kernel.render("Layer index (relative to current layer) :-",True,(200,200,200)), (20,140))
            for i, switch in enumerate(switchs):
                if mouse_click and mouse_click[0].button == 1 and switch.rect.collidepoint(mouse_pos):
                    flags["pos"] = i
                    is_textinput_on = False
                if flags["pos"] == i: switch.switch(True)
                else: switch.switch(False)
                switch.draw()
            apply_btn.draw()
            if apply_btn.rect.collidepoint(mouse_pos):
                pygame.draw.rect(self.subwindow.surface,(70,70,70),apply_btn.rect,2)
                if mouse_click and mouse_click[0].button == 1 :
                    if flags["name"].isalnum(): apply_btn.action(flags); popup_loop = False
            
            pygame.draw.rect(self.subwindow.surface,(200,0,0),self.subwindow.close_btn_rect)
            self.window.blit(self.subwindow.surface, self.subwindow.rect)
            pygame.draw.rect(self.window,(0,0,0),self.subwindow.rect,1)
            pygame.display.update()
        pygame.event.clear()
    
    def confirmation_dialog(self) -> bool: 
        loop = True
        out_stream = False

        buttons = [
            Button(self.popup,80,30,(100,160),"OK",lambda : True),
            Button(self.popup,80,30,(200,160),"CANCEL",lambda : False),
        ]
        
        while loop:

            mouse_click = pygame.event.get(pygame.MOUSEBUTTONDOWN)
            mouse_pos = tuple(sub_tuple(pygame.mouse.get_pos(), self.popup.rect.topleft))

            if self.popup.close_btn_rect.collidepoint(mouse_pos) and mouse_click and mouse_click[0].button == 1:
                loop = False
                out_stream = False
            
            self.popup.fill((100,100,100))

            for btn in buttons:
                btn.draw()
                if btn.rect.collidepoint(mouse_pos):
                    pygame.draw.rect(self.popup,(60,60,60),btn.rect,2)
                    if mouse_click and mouse_click[0].button == 1:
                        loop = False
                        out_stream = btn.action()

            self.popup.blit(self.head_font_kernel.render("Delete 'Current Layer' ? ",True,(200,200,200)),(40,24))

            pygame.draw.rect(self.popup,(200,0,0),self.popup.close_btn_rect)
            self.window.blit(self.popup, self.popup.rect)
            pygame.draw.rect(self.window,(0,0,0),self.popup.rect,1)
            pygame.display.update()
        
        pygame.event.clear()
        return out_stream

    def add_layer(self, flag):
        if flag['pos']:
            self.flags["layer_index"]+=1
            self.layers.append(flag['name'])
        else:
            self.layers.insert(self.flags["layer_index"],flag['name'])
        self.flags["current_layer"] = flag["name"]
        self.map_dict[flag['name']] = {}
    
    def remove_layer(self):
        if self.layers.__len__() > 1 and self.confirmation_dialog():
            del self.map_dict[self.layers.pop(self.flags['layer_index'])]
            self.flags['layer_index'] %= self.layers.__len__()
            self.flags['current_layer'] = self.layers[self.flags['layer_index']]
    
    def export_map(self):
        if path := asksaveasfilename(confirmoverwrite=True,defaultextension=".json",filetypes=[('JSON','.json')]):
            data = {}
            data['assets'] = self.assets
            data['config'] = self.config
            data['map'] = self.map_dict
            with open(path, "w") as fp:
                dump(data, fp, default = lambda _obj: _obj.__dict__)
    
    def import_map(self):
        if file := askopenfile(mode="r",filetypes=[("json",".json")],initialdir=self.config["dir_path"]):
            data = load(fp=file,parse_int=lambda num_str: int(num_str))
            
            self.map_dict.clear()
            self.layers.clear()
            self.layers.extend(list(data["map"].keys()))
            self.ResetFlags()

            self.config.update(data["config"])

            for key1, val1 in data["map"].items():
                self.map_dict[key1] = {}
                for key2, val2 in val1.items():
                    self.map_dict[key1][int(key2)] = {int(key3):sprite(val3["sprite_type"],val3["sprite"]) for key3, val3 in val2.items() if self.assets_cache[val3["sprite_type"]].get(val3["sprite"])}

            file.close()
    
    def ResetFlags(self):
        self.flags["selected"] = None
        self.flags["layer_index"] = 0
        self.flags["current_layer"] = self.layers[0]

class display_window:
    def __init__(self, window, width, height, pos, flags, keystate, assets, map_dict, layers, config):
        self.window = window
        self.flags = flags
        self.keystate = keystate
        self.assets = assets
        self.map_dict = map_dict
        self.surface = pygame.Surface((width, height))
        self.rect = self.surface.get_rect(topleft=pos)
        self.shift_offset = [0,0]
        self.placement_mode = 0
        self.prev_mouse_pos = (0,0)

        self.layers = layers
        self.config = config

        self.placement_types = {
            0 : "Tiled",
            1 : "Non-Tiled"
        }

        self.font_kernel = pygame.font.SysFont("comicsans",20,False)
    
    def draw(self):
        self.window.blit(self.surface, self.rect)
    
    def update(self, frame=0):
        self.surface.fill((40,40,40))

        abs_x, abs_y = self.keystate["mouse_pos"]
        abs_x, abs_y = (abs_x-self.shift_offset[0])//self.config["tile_size"][0], (abs_y-self.shift_offset[1])//self.config["tile_size"][1]
        
        if self.keystate["mouse_hold"][0]:
            if self.keystate["key_pressed"][pygame.K_LCTRL]:
                self.shift_offset[0] += self.keystate['mouse_pos'][0]-self.prev_mouse_pos[0]
                self.shift_offset[1] += self.keystate['mouse_pos'][1]-self.prev_mouse_pos[1]
                self.prev_mouse_pos = self.keystate['mouse_pos']
            elif self.flags["selected"]:
                if row := self.map_dict[self.flags["current_layer"]].get(abs_y):
                    row[abs_x] = sprite(self.flags["tile_type"], self.flags['selected'])
                else:
                    self.map_dict[self.flags["current_layer"]][abs_y] = {abs_x : sprite(self.flags["tile_type"], self.flags['selected'])}
        else:
            self.prev_mouse_pos = self.keystate['mouse_pos']

        if scrl := self.keystate["scroll"]:
            if self.keystate["key_pressed"][pygame.K_LCTRL]: self.flags["layer_index"]+=scrl[0].y; self.flags["layer_index"]%=self.layers.__len__(); self.flags["current_layer"] = self.layers[self.flags["layer_index"]]
        
        if self.keystate["mouse_hold"][2]:
            if row := self.map_dict[self.flags["current_layer"]].get(abs_y):
                if row.get(abs_x): del row[abs_x]
        
        for layer in self.layers:
            if self.flags["current_layer"] == layer: continue
            for y in range(-1-self.shift_offset[1]//self.config["tile_size"][1],(self.rect.bottom-self.shift_offset[1])//self.config["tile_size"][1]+1):
                if row := self.map_dict[layer].get(y):
                    for x in range(-1-self.shift_offset[0]//self.config["tile_size"][0],(self.rect.right-self.shift_offset[0])//self.config["tile_size"][0]+1):
                        if asset := row.get(x):
                            if asset.is_animated:
                                self.surface.blit(self.assets["Animated"][asset.sprite][frame%self.assets["Animated"][asset.sprite].__len__()], (x*self.config["tile_size"][0]+self.shift_offset[0], y*self.config["tile_size"][1]+self.shift_offset[1]))
                            else:
                                self.surface.blit(self.assets["Normal"][asset.sprite], (x*self.config["tile_size"][0]+self.shift_offset[0], y*self.config["tile_size"][1]+self.shift_offset[1]))
        
        for y in range(-1-self.shift_offset[1]//self.config["tile_size"][1],(self.rect.bottom-self.shift_offset[1])//self.config["tile_size"][1]+1):
            if row := self.map_dict[self.flags["current_layer"]].get(y):
                for x in range(-1-self.shift_offset[0]//self.config["tile_size"][0],(self.rect.right-self.shift_offset[0])//self.config["tile_size"][0]+1):
                    if asset := row.get(x):
                        if asset.is_animated:
                            self.surface.blit(self.assets["Animated"][asset.sprite][frame%self.assets["Animated"][asset.sprite].__len__()], (x*self.config["tile_size"][0]+self.shift_offset[0], y*self.config["tile_size"][1]+self.shift_offset[1]))
                        else:
                            self.surface.blit(self.assets["Normal"][asset.sprite], (x*self.config["tile_size"][0]+self.shift_offset[0], y*self.config["tile_size"][1]+self.shift_offset[1]))


        self.surface.blit(self.font_kernel.render(str(self.shift_offset),True,(200,200,200),(40,40,40)),(10,2))
        self.surface.blit(self.font_kernel.render(f"placement-mode : {self.placement_types[self.placement_mode]}",True,(200,200,200),(40,40,40)),(200,2))
        self.surface.blit(self.font_kernel.render(f'layer : {self.flags["current_layer"]}',True,(200,200,200),(40,40,40)),(480,2))

class Level_Designer:
    def __init__(self):
        pygame.init()

        self.width = 1200
        self.height = 700
        self.window = pygame.display.set_mode((self.width, self.height))
        self.icon = pygame.image.load("icon.ico").convert_alpha()
        self.clock = pygame.time.Clock()
        pygame.display.set_icon(self.icon)
        pygame.display.set_caption("Level Designer")
        pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)

        self.initial_time = time()
        self.delta_time = 0
        self.fps = 8
        self.current_frame = 0

        self.flags = {
            "tile_type": "Normal",
            "selected": None,
            "layer_index": 0,
            "current_layer": "terrain",
            "startup": True,
        }

        self.keystate = {
            "mouse_pos" : (0, 0),
            "rel_mouse_pos" : (0, 0),
            "mouse_hold" : None,
            "mouse_click" : None,
            "key_down" : None,
            "scroll" : None,
        }

        self.config = {
            "setup_mode": "create",
            "dir_path": "",
            "tile_size": [20,20],
        }

        self.map_dict = {
            'terrain': {},
        }
        
        self.assets_cache = {
            "Normal": {},
            "Animated": {},
        }
        
        self.layers = [
            "terrain",
        ]

        self.editor = display_window(self.window, self.width-200, self.height, (0,0), self.flags, self.keystate, self.assets_cache, self.map_dict, self.layers, self.config)
        self.toolbar = toolbar(self.window, 200, self.height, (self.editor.rect.right, 0), self.keystate, self.flags, self.assets_cache, self.map_dict, self.layers, self.config)
        self.workspace = designer_workspace(self.window, self.width, self.height, (0,0), self.flags, self.keystate, self.config, func = self.toolbar.load_n_cache_assets)

        # debug
        self.font_kernel = pygame.sysfont.SysFont("comicsans",20,True)

        self.startup = True

    def update_frame(self):
        self.current_frame = (self.current_frame+self.delta_time)%self.fps
    
    def update_timedelta(self):
        self.delta_time = time()-self.initial_time
        self.delta_time *= self.fps
        self.initial_time = time()

    def update_keystate(self):
        self.keystate["mouse_pos"] = pygame.mouse.get_pos()
        self.keystate["rel_mouse_pos"] = tuple(map(lambda a,b:a-b, self.keystate["mouse_pos"], self.toolbar.rect.topleft))
        self.keystate["mouse_hold"] = pygame.mouse.get_pressed(3)
        self.keystate["mouse_click"] = pygame.event.get(pygame.MOUSEBUTTONDOWN)
        self.keystate["scroll"] = pygame.event.get(pygame.MOUSEWHEEL)
        self.keystate["key_down"] = pygame.event.get(pygame.KEYDOWN)
        self.keystate["key_pressed"] = pygame.key.get_pressed()

    def run(self):
        self.toolbar.update()
        while not pygame.event.get(pygame.QUIT):

            # self.clock.tick(self.fps)

            self.update_timedelta()
            self.update_frame()
            self.update_keystate()
            
            if self.keystate["key_down"] and self.keystate["key_down"][0].key == pygame.K_SPACE:
                if self.flags['startup']: self.flags['startup'] = False
                else: self.flags['startup'] = True

            if self.flags["startup"]:
                self.workspace.update()

                self.workspace.draw()
            else:
                if self.editor.rect.collidepoint(self.keystate["mouse_pos"]):
                    self.editor.update(int(self.current_frame))
                else:
                    self.toolbar.update(int(self.current_frame))

                self.editor.draw()
                self.toolbar.draw()

            pygame.display.update()
        
        pygame.quit()