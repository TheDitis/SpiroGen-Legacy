"""
File: SpiroGenPlayground.py
Author: Ryan McKay
Date: April 12, 2020

Purpose: This is the Root of the SpiroGen application interface.
Input: None
Output: None, the application opens
"""
from tkinter import Frame, Button, ttk, Tk
from spirogen import spirogen as spiro
from spirogen.interface.PatternTab import PatternTab
from spirogen.interface.ColorSchemeTab import ColorSchemeTab
from spirogen.interface.Dialogs import SaveDialog, LoadDialog
import turtle
import os
import random
import json


class SpiroGenPlayground(ttk.Notebook):
    def __init__(self):
        super().__init__(Tk())  # initialize notebook (Frame that can use tabs)
        self.master.title('SiroGen')  # name the window
        self.master.geometry("600x950")  # set default window size
        self._patterntab = PatternTab(self)  # create the pattern control tab
        self._colorschemetab = ColorSchemeTab(self)  # create the colors tab
        # add both tabs to the notebook:
        self.add(self._patterntab, text="Pattern")
        self.add(self._colorschemetab, text="Color Scheme")
        # fill the master window
        self.pack(expan=1, padx=10, pady=10, fill='both')

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
        savebutton.pack(side="right", padx=20, pady=20)
        getbutton.pack(side="right", padx=20, pady=20)

        # add the button frame to the bottom of the window
        button_area.pack(side="bottom", fill='x')

        # basically, if settings directory doesn't exist, create it
        self.check_for_slash_create_save_directories()
        self.mainloop()  # run the tkinter loop to run the program

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
        SaveDialog(self.save)  # instantiate SaveDialog object with save method

    def open_load_dialog(self):
        LoadDialog(self.load)  # instantiate LoadDialog object with load method

    def check_for_slash_create_save_directories(self):
        paths = [
            './SpiroGenSettings',
            './SpiroGenSettings/sessions',
            './SpiroGenSettings/colors',
            './SpiroGenSettings/patterns'
        ]  # these are the settings folders

        # if they don't exist, we create them:
        for path in paths:
            if not os.path.exists(path):
                os.mkdir(path)

    def save(self, mode, name):
        name = name.lower()  # making sure the name is lowercase so there can only be one pattern per name
        colors = self._colorschemetab.save()  # collect the color data dict
        pattern = self._patterntab.save()  # collect the pattern data dict
        current = {'colors': colors, 'patterns': pattern}  # get the current settings for each tab
        files = os.listdir(f'./SpiroGenSettings/{mode}')  # get list of files in directory
        files = [f.replace('.json', '') for f in files]  # get the names without the file extensions
        if name not in files:
            if mode != 'sessions':  # if you are saving colors or pattern individually
                path = f'./SpiroGenSettings/{mode}/{name}.json'  # make path to new file
                with open(path, 'w') as file:  # open the file and save the data
                    json.dump(current[mode], file, indent=2)
            else:  # if you are saving both colors and pattern together:
                # generate ids for each:
                col_id = str(random.randint(100000, 199999))
                pat_id = str(random.randint(100000, 199999))
                # make an object with id pointers for each tab
                session = {'colors': col_id, 'patterns': pat_id}
                sessionpath = f"./SpiroGenSettings/sessions/{name}.json"  # make path to save session info
                # TODO: Add checking for id already existing
                with open(sessionpath, 'w') as file:  # save file pointer dict to file
                    json.dump(session, file, indent=2)
                for key in session:  # for each tab (colors and patterns):
                    path = f'./SpiroGenSettings/{key}/{session[key]}.json'  # make path with the new id as the file name
                    with open(path, 'w') as file:  # open the file and write data
                        json.dump(current[key], file, indent=2)
        else:  # if the name already exists:
            # TODO: ask if user wants to overwrite
            print('Name already exists. Try again')

    def load(self, mode, name):
        name = name.lower()
        destinations = {
            'colors': self._colorschemetab, 'patterns': self._patterntab
        }  # the tabs in an object to simplify loading data for each
        existing = os.listdir(f"./SpiroGenSettings/{mode}")  # get the list of file names in the folder for the given mode
        existing = [f.replace('.json', '') for f in existing]  # and removing the file extension
        if name in existing:  # if the save file exists in the folder
            path = f"./SpiroGenSettings/{mode}/{name}.json"  # make the path string
            if mode != 'sessions':  # if you are loading one tab individually:
                with open(path, 'r') as file:  # open file and grab data
                    data = json.load(file)
                destinations[mode].load(data)  # call the given tabs load method
            else:  # if you are loading a whole session:
                with open(path, 'r') as file:  # open the file and grab the data
                    ids = json.load(file)
                for k in ids:  # there are two keys (patterns, colors) each with an id pointer
                    path = f"./SpiroGenSettings/{k}/{ids[k]}.json"  # make path string with given id
                    with open(path, 'r') as file:  # open the file and try to grab the data
                        try:
                            data = json.load(file)
                        except json.decoder.JSONDecodeError:
                            print('Error loading data from ', path)
                    destinations[k].load(data)  # call load method for given tab
        else:  # if name doesn't exist in folder:
            print('Name not found. Try another mode, or a different name.')

    def run(self):
        try:
            self.setup_drawing()  # setup the window parameters
            self._patterntab.run(self._colorschemetab.colorscheme)  # call the run method of the pattern tab, passing the colorscheme info
        except turtle.Terminator:  # turtle sometimes throws errors when you try to launch after clicking to exit the previous
            self.setup_drawing()
            self._patterntab.run(self._colorschemetab.colorscheme)  # Running it a second time when this happens works just fine
