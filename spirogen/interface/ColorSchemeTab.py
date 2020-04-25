"""
File: ColorSchemeTab.py
Author: Ryan McKay
Date: April 13, 2020

Purpose: This a tkinter based tab for the spirogen interface that controls the
    color scheme for the pattern
Input: master Notebook
Output:
    save method outputs a dictionary to be saved as json
"""
from tkinter import StringVar, Label, Button, Entry, Frame
from copy import deepcopy
from spirogen.interface.Tab import Tab
from spirogen.interface.Parameter import Parameter
from spirogen.spirogen import ColorScheme
from spirogen.interface.Dialogs import ShiftLightnessDialog, \
    RampLightnessDialog, ColorSwatchDialog
from spirogen.interface.ColorSwatch import ColorSwatch


class ColorSchemeTab(Tab):
    def __init__(self, master):
        super().__init__(master)
        self._id = None  # currently unused, but will be for saving and loading
        # dictionary of default colors for initialization and the reset button:
        self._default = {
            'r': [255, 255, 255, 220, 75, 3, 3, 30, 125, 220, 255],
            'g': [0, 150, 255, 255, 255, 255, 145, 3, 3, 3, 0],
            'b': [0, 0, 0, 3, 3, 240, 255, 255, 255, 255, 0]
        }
        # self.backgroundcolor = self.rgb_tk((0, 0, 0))
        self._resetcolors = True  # this tells the color boxes to fill themselves with the defaults
        self._colordict = deepcopy(self._default)  # this is master list of colors that you use and edit. Starts as default

        # variables for the background color:
        self._bg_red = StringVar()
        self._bg_green = StringVar()
        self._bg_blue = StringVar()
        # putting them all into a single object:
        self._bg_vars = {
            'r': self._bg_red,
            'g': self._bg_green,
            'b': self._bg_blue
        }
        # this will be the swatch that shows you the color
        self._bg_color_example = None

        # label the background control area
        backgroundlabel = Label(self, text="Background:", font=self.h1)
        backgroundlabel.grid(
            row=2, column=3, columnspan=300, pady=(10, 5), sticky="nw"
        )
        # setup the controls for the background color
        self.setup_background_color_area()

        # label the pattern color control area
        patternlabel = Label(self, text="Pattern:", font=self.h1)
        patternlabel.grid(
            row=6, column=3, columnspan=300, pady=(10, 5), sticky="nw"
        )

        # initializing and setting the main parameters
        self._totalcolors = Parameter(
            self, label="Total Colors (fade smoothness)", from_=1, to=300,
            command=self.check_ratio_tot, row=9
        )  # this one sets the number of transitionary colors beginning to end of the selected colors
        self._totalcolors.set(100)
        self._colorstops = Parameter(
            self, label="Number of Stops", from_=1, to=11,
            command=self.update_colorstops, row=10
        )  # this one sets the number of colors you define specifically
        self._colorstops.set(5)

        settodefaultcolors = Button(
            self, text='Load Default Colors',
            command=self.reset_colors_to_default
        )  # resets colordict back to the default rainbow set
        settodefaultcolors.grid(row=18, column=3, columnspan=300)
        reversecolors = Button(
            self, text='Reverse Order', command=self.reverse_color_order
        )  # this button flips the order of the entire color dictionary
        reversecolors.grid(row=18, column=500, columnspan=300)

        # This comes from the Tab class, and it is a Separate frame that can
        # keep spacing independent from controls on the rest of the tab. this
        # is where the color boxes will go.
        self._spacedarea.grid(row=20, column=0, columnspan=800)

        self._colorshift = Parameter(
            self, label="Shift Position", from_=-6, to=6, row=25,
            command=self.shift_color, bigincrement=1
        )  # this control shifts the position of the colors in the dictionary
        self.previousshift = 0  # this is for determining the interval of shift (-1 or 1)

        # label the effects section of the tab
        effectslabel = Label(self, text="Effects:", font=self.h2)
        effectslabel.grid(
            row=28, column=3,columnspan=200, pady=(10, 5), padx=(10, 0)
        )

        # creating the buttons for each color transformation
        shiftlightnessbutton = Button(
            self, text="Shift Lightness",
            command=lambda: ShiftLightnessDialog(self.shift_lightness)
        )
        ramplightnessbutton = Button(
            self, text="Ramp Lightness", command=self.open_ramp_lightness_dialog
        )

        shiftlightnessbutton.grid(
            row=30, column=3, columnspan=200, pady=10, padx=(5, 0)
        )
        ramplightnessbutton.grid(row=30, column=210, columnspan=200)


    @property
    def colorscheme(self):
        # returns a spirogen ColorScheme object with the current parameters
        scheme = ColorScheme(self.currentcolors, self._totalcolors.get())
        return scheme

    @property
    def currentcolors(self):
        # this returns the set of color dictionary that you are actually using
        colors = {'r': [], 'g': [], 'b': []}
        for key in colors:
            colors[key] = self.colordict[key][:self._colorstops.get()]
        return colors

    @property
    def backgroundcolor(self):
        # gets the rgb value tuple
        return self.make_bg_color()

    @property
    def colordict(self):
        # getter for colordict
        return self._colordict

    @colordict.setter
    def colordict(self, val):
        # setter for colordict
        self._colordict = val

    def setup_background_color_area(self):
        # creates and places the controls for the backgorund color section

        # binding these variables to the method that groups the colors together,
        # so that the swatch updates in real time with changes.
        self._bg_red.trace('w', self.make_bg_color)
        self._bg_green.trace('w', self.make_bg_color)
        self._bg_blue.trace('w', self.make_bg_color)

        self._bg_color_example = ColorSwatch(
            self, self._bg_red, self._bg_green, self._bg_blue, height=20,
            curcolors=self.colordict, defaultcolors=self._default,
            width=25, highlightbackground='black', highlightthickness=1
        )  # this is the swatch preview of the color

        # setting default background color to black
        self._bg_red.set(0)
        self._bg_green.set(0)
        self._bg_blue.set(0)

        rlabel = Label(self, text='R:')
        glabel = Label(self, text='G:')
        blabel = Label(self, text='B:')
        rbox = Entry(self, textvariable=self._bg_red, width=5)
        gbox = Entry(self, textvariable=self._bg_green, width=5)
        bbox = Entry(self, textvariable=self._bg_blue, width=5)

        rlabel.grid(row=3, column=80, columnspan=60)
        rbox.grid(row=4, column=80, columnspan=60)
        glabel.grid(row=3, column=150, columnspan=60)
        gbox.grid(row=4, column=150, columnspan=60)
        blabel.grid(row=3, column=220, columnspan=60)
        bbox.grid(row=4, column=220, columnspan=60)
        self._bg_color_example.grid(row=4, column=300)

    def make_bg_color(self, *args):
        # get the value of each bg_color variable
        rstr = self._bg_red.get()
        gstr = self._bg_green.get()
        bstr = self._bg_blue.get()
        # if none of the boxes are empty:
        if all(map(lambda x: x != '', [rstr, gstr, bstr])):
            try:  # try to convert them to integers:
                r = round(float(rstr))
                g = round(float(gstr))
                b = round(float(bstr))
                color = self.rgb_tk(
                    (self._bg_red.get(),
                     self._bg_green.get(),
                     self._bg_blue.get())
                )  # create a tkinter compatible color
                self._bg_color_example.updatecolor(color)  # set the swatch to that color
                return self.rgb_tk((r, g, b))  # return a spirogen compatible color
            except ValueError:  # if the values could not be converted:
                # let the user know
                print('Color values must be numbers between 0 and 255')

    def reset_colors_to_default(self):
        # this method is run by the reset colors button, and is self explanitory
        self._resetcolors = True
        self.colordict = deepcopy(self._default)
        self.colordict = deepcopy(self._default)
        self._colorshift.set(0)
        self.update_color_boxes()

    def update_colorstops(self, *args):
        self.check_ratio_stops(*args) #
        self.make_color_boxes()

    def shift_color(self, *args):
        colordict = deepcopy(self.colordict)
        amt = self._colorshift.get()
        prev = self.previousshift
        self.previousshift = amt
        if amt < prev:
            interval = -1
        else:
            interval = 1
        if amt == 0:
            amt = 1
        for j in range(abs(amt)):
            for color in colordict:
                for i in range(len(colordict[color])):
                    ind = (i - interval) % len(colordict[color])
                    colordict[color][i] = self.colordict[color][ind]
        self.colordict = colordict
        self.update_color_boxes()

    def reverse_color_order(self, *args):
        colordict = deepcopy(self.colordict)
        for key in colordict:
            for i in range(len(colordict[key])):
                colordict[key][i] = self.colordict[key][-i -1]
        self.colordict = colordict
        self.update_color_boxes()

    def is_default_colors(self):
        for key in self.colordict:
            if key == 'r':
                def_r = self.colordict[key]
                r = self.colordict[key]
            elif key == 'g':
                def_g = self.colordict[key]
                g = self.colordict[key]
            elif key == 'b':
                def_b = self.colordict[key]
                b = self.colordict[key]
        r_match = all(map(lambda x: r.count(x) == def_r.count(x), r))
        g_match = all(map(lambda x: g.count(x) == def_g.count(x), g))
        b_match = all(map(lambda x: b.count(x) == def_b.count(x), b))
        return all([r_match, g_match, b_match])

    def check_ratio_tot(self, tot):
        tot = int(tot)
        if tot < self._colorstops.get():
            self._colorstops.set(tot)

    def check_ratio_stops(self, stops):
        stops = int(stops)
        if stops > self._totalcolors.get():
            self._totalcolors.set(stops)

    @staticmethod
    def rgb_tk(rgb):
        rgb = tuple([round(float(i)) for i in rgb])
        output = "#%02x%02x%02x" % rgb
        return output

    def make_color_boxes(self):
        """
        This method
        Returns:

        """
        n = self._colorstops.get()
        prevparams = []
        if 'colorparams' in self._progparams.keys():
            for group in self._progparams['colorparams']:
                entry = []
                for key in group:
                    if key == 'vals':
                        for widget in group[key].values():
                            entry.append(widget.get())
                    elif key == 'boxes':
                        for widget in group[key].values():
                            widget.grid_forget()
                    else:
                        widget = group[key]
                        widget.grid_forget()
                prevparams.append(entry)

        self._progparams['colorparams'] = []

        r_row, g_row, b_row = 10, 14, 18

        label_r = Label(self._spacedarea, text="R")
        label_g = Label(self._spacedarea, text="G")
        label_b = Label(self._spacedarea, text="B")

        label_r.grid(row=r_row, column=0, padx=(0, 10))
        label_g.grid(row=g_row, column=0, padx=(0, 10))
        label_b.grid(row=b_row, column=0, padx=(0, 10))

        for i in range(n):
            col_label = Label(self._spacedarea, text=str(i + 1))

            red = StringVar()
            red.trace(
                'w', lambda *x: self.update_color_dict(x, index=i, key='r')
            )
            redbox = Entry(self._spacedarea, width=3, textvariable=red)

            green = StringVar()
            green.trace(
                'w', lambda *x: self.update_color_dict(x, index=i, key='g')
            )
            greenbox = Entry(self._spacedarea, width=3, textvariable=green)

            blue = StringVar()
            blue.trace(
                'w', lambda *x: self.update_color_dict(x, index=i, key='b')
            )
            bluebox = Entry(self._spacedarea, width=3, textvariable=blue)

            red.set(self.colordict['r'][i])
            green.set(self.colordict['g'][i])
            blue.set(self.colordict['b'][i])

            color = self.rgb_tk((red.get(), green.get(), blue.get()))
            examplebox = ColorSwatch(
                self._spacedarea, red, green, blue, color=color,
                curcolors=self._colordict, defaultcolors=self._default
            )

            col = 20 * (i + 1)  # just so that I have flexibility in positioning things later if I make changes
            col_label.grid(row=8, column=col, pady=10, padx=1)
            redbox.grid(row=r_row, column=col)
            greenbox.grid(row=g_row, column=col)
            bluebox.grid(row=b_row, column=col)

            examplebox.grid(row=20, column=col, pady=10)

            self._progparams['colorparams'].append(
                {'boxes': {'r': redbox, 'g': greenbox,'b': bluebox},
                 'vals': {'r': red, 'g': green, 'b': blue},
                 'label': col_label,
                 'example': examplebox})
            # self.resetcolors = False
            # pass
            # self.progparams['curveboxes'].append([curvebox, label2])

    def update_color_dict(self, *args, index, key):
        colparams = self._progparams['colorparams']
        values = [i['vals'] for i in colparams]
        examples = [i['example'] for i in colparams]
        newcols = deepcopy(self.colordict)
        for i in range(len(values)):  # for index of values (tk StringVar objects):
            group = values[i]  # group =  {'r': rVar, 'g': gVar, 'b': bVar)
            rgb = []
            for key in group:  # for 'r', 'g', and 'b':
                shift = self._colorshift.get()  # get the value of the shift parameter
                ind = (i - 1) % len(self.colordict[key])  # set the index to edit, based on remainder of the index - shift amount
                strval = group[key].get()
                if strval != '':
                    val = round(float(strval))
                    self.colordict[key][ind] = val
                    newcols[key][i] = val
                    rgb.append(val)
            if len(rgb) == 3:
                examples[i].updatecolor(self.rgb_tk(rgb))
        self.colordict = newcols

    def update_color_boxes(self):
        self.make_color_boxes()
        for i in range(len(self._progparams['colorparams'])):
            group = self._progparams['colorparams'][i]
            rgb = []
            for key in group['vals']:
                val = self.colordict[key][i]
                rgb.append(val)
                group['vals'][key].set(val)
        self.make_color_boxes()

    def open_ramp_lightness_dialog(self):
        dialog = RampLightnessDialog(self.ramp_lightness)
        # dialog

    def shift_lightness(self, amount):
        scheme = ColorScheme(self.colordict, self._colorstops.get())
        scheme.shiftlightness(amount)
        self.colordict = scheme.colors
        self.update_color_boxes()

    def ramp_lightness(self, amount, direction, goto):
        scheme = ColorScheme(self.colordict, self._colorstops.get())
        scheme.ramplightness(amount, direction, goto)
        self.colordict = scheme.colors
        self.update_color_boxes()

    def save(self):
        output = {'background': {'r': self._bg_red.get(),
                                 'g': self._bg_green.get(),
                                 'b': self._bg_blue.get()},
                  'totalcolors': self._totalcolors.get(),
                  'nstops': self._colorstops.get(),
                  'colordict': self.colordict,
                  'id': self._id}
        return output

    def load(self, data):
        for k in data["background"]:
            self._bg_vars[k].set(data["background"][k])
        self._totalcolors.set(int(data["totalcolors"]))
        self._colorstops.set(int(data["nstops"]))
        self.colordict = data["colordict"]
        self.update_color_boxes()

