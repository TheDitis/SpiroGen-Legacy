from tkinter import Frame, Button, ttk
import spirogen as spiro
from PatternTab import PatternTab
from ColorSchemeTab import ColorSchemeTab
import json
from Dialogs import SaveDialog, LoadDialog
import os
import random


class Application(ttk.Notebook):
    def __init__(self, master):
        super().__init__(master)

        self.patterntab = PatternTab(self)
        # patterntab = ttk.Frame(tabcontrol)
        self.add(self.patterntab, text="Pattern")
        self.colorschemetab = ColorSchemeTab(self)
        self.add(self.colorschemetab, text="Color Scheme")

        self.pack(expan=1, padx=10, pady=10, fill='both')

        button_area = Frame(self)

        getbutton = Button(button_area, text="Load", command=self.open_load_dialog)
        savebutton = Button(button_area, text="Save", command=self.open_save_dialog)
        runbutton = Button(button_area, text="Run", command=self.run)

        runbutton.pack(side="right", padx=40, pady=20)
        savebutton.pack(side="right", padx=20, pady=20)
        getbutton.pack(side="right", padx=20, pady=20)

        button_area.pack(side="bottom", fill='x')

        self.check_for_slash_create_save_directories()

    def setup_drawing(self):
        spiro.reset()
        speed = 10
        drawspeed = 1000
        default_resolution = (1920, 1200)
        smaller_resolution = (1520, 800)
        bgcolor = self.colorschemetab.backgroundcolor
        spiro.setup(drawspeed, speed, bgcolor, hide=True, resolution=default_resolution)

    def open_save_dialog(self):
        SaveDialog(self.save)

    def open_load_dialog(self):
        LoadDialog(self.load)

    def check_for_slash_create_save_directories(self):
        paths = ['./SpiroGenSettings', './SpiroGenSettings/sessions', './SpiroGenSettings/colors', './SpiroGenSettings/patterns']
        for path in paths:
            if not os.path.exists(path):
                os.mkdir(path)

    def save(self, mode, name):
        colors = self.colorschemetab.save()
        pattern = self.patterntab.save()
        current = {'colors': colors, 'patterns': pattern}
        files = os.listdir(f'./SpiroGenSettings/{mode}')
        files = [f.replace('.json', '') for f in files]
        if name not in files:
            if mode != 'sessions':
                path = f'./SpiroGenSettings/{mode}/{name}.json'
                with open(path, 'w') as file:
                    json.dump(current[mode], file, indent=2)
            else:
                col_id = str(random.randint(100000, 199999))
                pat_id = str(random.randint(100000, 199999))
                session = {'colors': col_id, 'patterns': pat_id}
                sessionpath = f"./SpiroGenSettings/sessions/{name}.json"
                # TODO: Add checking for id already existing
                with open(sessionpath, 'w') as file:
                    json.dump(session, file, indent=2)
                for key in session:
                    path = f'./SpiroGenSettings/{key}/{session[key]}.json'
                    with open(path, 'w') as file:
                        json.dump(current[key], file, indent=2)
        else:
            print('Name already exists. Try again')

    def load(self, mode, name):
        name = name.lower()
        destinations = {'colors': self.colorschemetab, 'patterns': self.patterntab}
        existing = os.listdir(f"./SpiroGenSettings/{mode}")
        existing = [f.replace('.json', '') for f in existing]
        if name in existing:
            path = f"./SpiroGenSettings/{mode}/{name}.json"
            if mode != 'sessions':
                with open(path, 'r') as file:
                    data = json.load(file)
                destinations[mode].load(data)
            else:
                with open(path, 'r') as file:
                    ids = json.load(file)
                for k in ids:
                    path = f"./SpiroGenSettings/{k}/{ids[k]}.json"
                    with open(path, 'r') as file:
                        try:
                            data = json.load(file)
                        except:
                            print('PATH', path)
                    destinations[k].load(data)
        else:
            print('Name not found. Try another mode, or a different name.')
        # with open('settings/colors/colors.json', 'r') as file:
        #     data = json.load(file)
        #     if mode != 'sessions':
        #         if name.lower() in data[mode]:
        #             loaddata = data[mode][name.lower()]
        #             destinations[mode].load(loaddata)
        #         else:
        #             print('name does not seem to exist')
        #     else:
        #         print("mode = 'sessions'")
        # self.colorschemetab.load(data['colorscheme'])

    def run(self):
        try:
            self.setup_drawing()
            self.patterntab.run(self.colorschemetab.colorscheme)
        except:  # turtle sometimes throws errors when you try to launch after clicking to exit the previous
            self.setup_drawing()
            self.patterntab.run(self.colorschemetab.colorscheme)  # Running it a second time when this happens works just fine
