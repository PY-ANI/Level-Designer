from json import dump, load
from os import listdir, path, mkdir
from shutil import copy
from tkinter.filedialog import askopenfilenames, askdirectory, asksaveasfile, askopenfile
from tkinter.messagebox import askyesno

class workspace():
    def __init__(self) -> None:

        self.sprite_dir = 'sprites'
        self.working_dir = None
        self.sprite_dir_path = None

        self.is_updated = False

        self.cached_sprites = {}

        self.json_template = {
            'sprite_keys':[],
            'map':{},
        }

    def setup_workspace(self):
        
        self.working_dir = askdirectory(mustexist=True,title="setup workspace directory",)
        if self.working_dir:
            self.cached_sprites.clear()
            self.json_template['map'].clear()
            self.json_template['sprite_keys'].clear()
            self.sprite_dir_path = path.join(self.working_dir,self.sprite_dir)
            if not path.exists(self.sprite_dir): mkdir(self.sprite_dir_path)
            else:
                self.load_sprite_dir()

            return True

    def get_sprites(self):

        if not self.working_dir: return False

        files = askopenfilenames(defaultextension='.png', filetypes=[("PNG",'.png'), ("JPG",'.jpeg')], title="select sprites to import")

        is_for_all = False

        if files:
            for file in files:
                filename = file.split('/')[-1]
                if not is_for_all and path.exists(path.join(self.sprite_dir_path,filename)):
                    if askyesno("Overwrite File in Destination ?",file):
                        is_for_all = askyesno(message="Apply to all files ?")
                    else: continue

                copy(file,path.join(self.sprite_dir_path,filename))
            
            self.load_sprite_dir()


    def load_sprite_dir(self):
        if not self.working_dir: return False
        for sprite in listdir(self.sprite_dir_path):
            if path.isfile(path.join(self.sprite_dir,sprite)) and not self.cached_sprites.get(sprite):
                self.json_template['sprite_keys'].append(sprite)

                self.is_updated = True
    
    def export_map(self):
        file = asksaveasfile('w',confirmoverwrite=True,defaultextension='.json',filetypes=[('JSON','.json')],title='Save As',initialfile='Map_data')
        if file:
            dump(self.json_template,file)

    def import_map(self):
        file = askopenfile('r',defaultextension='.json',filetypes=[('JSON','.json')],title='Open File')
        if file:
            self.json_template = load(file)
            self.json_template['map'] = self.jsondict_to_dict(self.json_template['map'])
            self.is_updated = True

            return True
        
    def jsondict_to_dict(self,dt):
        rt_dict = {}
        for y, row in dt.items():
            rt_dict[int(y)] = {}
            for x, sp in row.items():
                rt_dict[int(y)][int(x)] = sp

        return rt_dict