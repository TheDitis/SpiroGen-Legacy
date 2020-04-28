"""
File: SpiroGenPlayground.py
Author: Ryan McKay
Date: April 12, 2020

Purpose: This is the Root of the SpiroGen application interface.
Input: None
Output: None, the application opens
"""
from tkinter import Frame, Button, ttk, Tk, Menu
from spirogen import spirogen as spiro
from spirogen.interface.PatternTab import PatternTab
from spirogen.interface.ColorSchemeTab import ColorSchemeTab
from spirogen.interface.Dialogs import SaveDialog, LoadDialog
from spirogen.interface.Help import HelpIndex, Tutorial
import turtle
import os
from copy import deepcopy
import json


class TopMenu(Menu):
    def __init__(self, master):
        super().__init__(master)
        filemenu = Menu(self, tearoff=0)
        filemenu.add_command(label="Open", command=master.open_load_dialog)
        filemenu.add_command(label="Save", command=master.open_save_dialog)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=master.quit)
        self.add_cascade(label="File", menu=filemenu)

        helpmenu = Menu(self, tearoff=0)
        helpmenu.add_command(label="Tutorial", command=Tutorial)
        helpmenu.add_command(label="Help Index", command=HelpIndex)
        self.add_cascade(label="Help", menu=helpmenu)


class Application(ttk.Notebook):
    def __init__(self):
        super().__init__(Tk())  # initialize notebook (Frame that can use tabs)
        menu = TopMenu(self)
        self.master.title('SiroGen')  # name the window
        self.master.geometry("600x1000")  # set default window size
        # fill the master window
        self.pack(expan=1, padx=10, pady=10, fill='both')

        self._patterntab = PatternTab(self)  # create the pattern control tab
        self._colorschemetab = ColorSchemeTab(self)  # create the colors tab

        # add both tabs to the notebook:
        self.add(self._patterntab, text="Pattern")
        self.add(self._colorschemetab, text="Color Scheme")

        self._settingnames = {
            'sessions': None, 'colors': None, 'patterns': None
        }

        self._settingspath = './spirogen/interface/settings/'

        # create a frame for the load, save, and run buttons
        button_area = Frame(self)

        # create those three buttons:
        getbutton = Button(
            button_area, text="Load", command=self.open_load_dialog
        )
        savebutton = Button(
            button_area, text="Save", command=self.open_save_dialog
        )
        runbutton = Button(button_area, text="Run", command=self.run)

        # add those three buttons to the button frame
        runbutton.pack(side="right", padx=40, pady=20)
        savebutton.pack(side="left", padx=40, pady=20)
        getbutton.pack(side="left", padx=0, pady=20)

        # add the button frame to the bottom of the window
        button_area.pack(side="bottom", fill='x')

        # basically, if settings directory doesn't exist, create it
        self.check_for_slash_create_save_directories()
        self._showtut = self.check_if_should_show_tutorial()

        if self._showtut: # if the tutorial should be shown:
            self.bind("<Enter>", self.open_tutorial)
        self.master.config(menu=menu)
        self.master.mainloop()  # run the tkinter loop to run the program

    def setup_drawing(self):
        spiro.reset()  # this just brings the drawing cursor back to center
        speed = 10  # this controls render speed (basically skipped frames)
        drawspeed = 1000  # this controls how fast the cursor moves
        default_resolution = (1920, 1200)  # size of drawing window
        smaller_resolution = (1520, 800)
        bgcolor = self._colorschemetab.backgroundcolor  # get bgcolor from tab
        spiro.setup(
            drawspeed, speed, bgcolor, hide=True, resolution=default_resolution
        )  # this is the spirogen function for initailizing the turtle drawing

    def open_save_dialog(self):
        SaveDialog(self.save, self._settingnames)  # instantiate SaveDialog object with save method

    def open_load_dialog(self):
        LoadDialog(self.load)  # instantiate LoadDialog object with load method

    def check_for_slash_create_save_directories(self):
        paths = [
            f'{self._settingspath[:-1]}',  # the root directory without the slash
            f'{self._settingspath}sessions',  # each of the folders within
            f'{self._settingspath}colors',
            f'{self._settingspath}patterns',
            f'{self._settingspath}tutorial'
        ]  # these are the settings folders

        # the path to the file that determines whether the tutorial should launch
        showtutpath = f'{self._settingspath}tutorial/showtutorial.json'

        # if they don't exist, we create them:
        for path in paths:
            if not os.path.exists(path):
                os.mkdir(path)
                if path == 'tutorial':  # if the tutorial path doesn't exist:
                    # create the file that determines whether or not the
                    # tutorial should launch and set it to false since the
                    # assests will be missing.
                    with open(showtutpath, 'w') as file:
                        json.dump({'showtutorial': False}, file)

    def check_if_should_show_tutorial(self):
        # this method reads the file that determines whether the tutorial should
        # launch automatically. The tutorial should open on first launch only
        showtutpath = f'{self._settingspath}tutorial/showtutorial.json'
        with open(showtutpath, 'r') as file:
            showtut = json.load(file)['showtutorial']
        if showtut:
            with open(showtutpath, 'w') as file:
                json.dump({'showtutorial': False}, file)
            return True
        else:
            return False

    def open_tutorial(self, *args):
        if self._showtut:
            Tutorial()
        self._showtut = False

    def save(self, mode, name):
        name = name.lower()  # making sure the name is lowercase so there can only be one pattern per name
        colname, colors = self._colorschemetab.save(mode, name)  # collect the color data dict
        patname, pattern = self._patterntab.save(mode, name)  # collect the pattern data dict
        names = {'colors': colname, 'patterns': patname}
        print(names)
        self._settingnames[mode] = name
        current = {'colors': colors, 'patterns': pattern}  # get the current settings for each tab
        files = os.listdir(f'{self._settingspath}{mode}')  # get list of files in directory
        files = [f.replace('.json', '') for f in files]  # get the names without the file extensions
        if name not in files:
            if mode != 'sessions':  # if you are saving colors or pattern individually
                path = f'{self._settingspath}{mode}/{name}.json'  # make path to new file
                with open(path, 'w') as file:  # open the file and save the data
                    json.dump(current[mode], file, indent=2)
            else:  # if you are saving both colors and pattern together:
                ids = deepcopy(self._settingnames)
                ids.pop('sessions')
                for k in ids:
                    if ids[k]:
                        self._settingnames[k] = names[k]
                        ids[k] = names[k]
                    else:
                        ids[k] = f"from {name} session"
                # TODO: Add checking for id already existing
                sessionpath = f"{self._settingspath}/sessions/{name}.json"  # make path to save session info
                for key in ids:  # for each tab (colors and patterns):
                    path = f'{self._settingspath}/{key}/{ids[key]}.json'  # make path with the new id as the file name
                    while os.path.exists(path):  # while a file with this given name exists
                        with open(path, 'r') as file:  # open the
                            existing = json.load(file)
                        if existing != current[key]:  # if the current version is different from the saved version:
                            if ids[key][-1].isdigit():  # if the last character is a digit:
                                if ids[key][-2].isdigit():  # if the second character is also a digit:

                                    num = int(ids[key][-2:]) + 1  # grab the number and increment it
                                    ids[key] = ids[key][:-2] + str(num)  # and replace the old number with the new
                                    print(ids[key])
                                else:  # if there is only one digit:
                                    print('one digit')
                                    num = int(ids[key][-1]) + 1  # increment the number
                                    ids[key] = ids[key][:-1] + str(num)  # and replace it
                                    print(ids[key])
                            else:  # if name does not have a number after it:
                                print('no digits')
                                ids[key] += ' ' + str(2)  # add a number to the end
                                print(ids[key])
                        else:
                            break
                        path = f'{self._settingspath}/{key}/{ids[key]}.json'
                        print('2', path)
                    path = f'{self._settingspath}/{key}/{ids[key]}.json'
                    with open(path, 'w') as file:  # open the file and write data
                        json.dump(current[key], file, indent=2)
                with open(sessionpath, 'w') as file:  # save file pointer dict to file
                    json.dump(ids, file, indent=2)
        else:  # if the name already exists:
            # TODO: ask if user wants to overwrite
            print('Name already exists. Try again')

    def load(self, mode, name):
        name = name.lower()
        destinations = {
            'colors': self._colorschemetab, 'patterns': self._patterntab
        }  # the tabs in an object to simplify loading data for each
        existing = os.listdir(f"{self._settingspath}/{mode}")  # get the list of file names in the folder for the given mode
        existing = [f.replace('.json', '') for f in existing]  # and removing the file extension
        if name in existing:  # if the save file exists in the folder
            path = f"{self._settingspath}/{mode}/{name}.json"  # make the path string
            if mode != 'sessions':  # if you are loading one tab individually:
                with open(path, 'r') as file:  # open file and grab data
                    try:
                        data = json.load(file)
                        destinations[mode].load(name, data)  # call the given tabs load method
                        self._settingnames[mode] = name
                        destinations[mode].name = name
                    except json.decoder.JSONDecodeError:
                        print('Error loading data from ', path)
            else:  # if you are loading a whole session:
                with open(path, 'r') as file:  # open the file and grab the data
                    ids = json.load(file)
                for k in ids:  # there are two keys (patterns, colors) each with an id pointer
                    path = f"{self._settingspath}/{k}/{ids[k]}.json"  # make path string with given id
                    with open(path, 'r') as file:  # open the file and try to grab the data
                        try:
                            data = json.load(file)
                        except json.decoder.JSONDecodeError:
                            print('Error loading data from ', path)
                    self._settingnames[k] = ids[k]
                    destinations[k].load(ids[k], data)  # call load method for given tab
                self._settingnames['sessions'] = name
        else:  # if name doesn't exist in folder:
            print('Name not found. Try another mode, or a different name.')

    def run(self):
        try:
            self.setup_drawing()  # setup the window parameters
            self._patterntab.run(self._colorschemetab.colorscheme)  # call the run method of the pattern tab, passing the colorscheme info
        except turtle.Terminator:  # turtle sometimes throws errors when you try to launch after clicking to exit the previous
            self.setup_drawing()
            self._patterntab.run(self._colorschemetab.colorscheme)  # Running it a second time when this happens works just fine
