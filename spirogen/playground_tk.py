from spirogen import setup, Transform, Analyze, Colors, ColorScheme, Pattern, PolarPattern, Wave, Rectangle, Circle, RadialAngularPattern, FlowerPattern, FlowerPattern2, DrawPath, TimesTable, CascadeLines, LVL2, wait, reset, bye
from functools import partial
from tkinter import *
from tkinter import ttk
from copy import deepcopy


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

        getbutton = Button(button_area, text="Load")
        savebutton = Button(button_area, text="Save")
        runbutton = Button(button_area, text="Run", command=self.run)

        runbutton.pack(side="right", padx=40, pady=20)
        savebutton.pack(side="right", padx=20, pady=20)
        getbutton.pack(side="right", padx=20, pady=20)

        button_area.pack(side="bottom", fill='x')

    def run(self):
        self.patterntab.run(self.colorschemetab.colorscheme)


class Tab(Frame):
    def __init__(self, master):
        super().__init__(master)
        self._rangewidth = 500
        self.pack(padx=50, pady=50)
        self._rangewidth = 500
        self.columns = 800
        self.rows = 800
        self.bind("<Configure>", self.config)

        self.spacedarea = Frame(self)
        self.progparams = {}


    def config(self, event):
        w, h = event.width, event.height
        for i in range(self.rows):
            self.grid_rowconfigure(i, minsize=h/8000, weight=1)
        for i in range(self.columns):
            self.grid_columnconfigure(i, minsize=w/8000, weight=1)

    @property
    def rangewidth(self):
        return self._rangewidth

    @rangewidth.setter
    def rangewidth(self, val):
        self._rangewidth = val


class Parameter(Scale):
    def __init__(self, master=None, columnspan=700, column=1, row=None, pady=20, **kwargs):
        self.rangewidth = 10000
        super().__init__(master, length=self.rangewidth, activebackground='green', orient="horizontal", **kwargs)
        self.column = column
        self.columnspan = 790
        self.row = row
        self.label = kwargs['label']
        self.grid(column=self.column, columnspan=self.columnspan, row=self.row, pady=pady)

    def __repr__(self):
        return f"{self.label}: {self.get()}"


class PatternTab(Tab):
    def __init__(self, master):
        self.parameters = {}

        super().__init__(master)

        # Setting dropdown menu for selecting pattern type
        patterns = ['layeredflowers', 'radialangular', 'sinespiral']
        self.patternselection = StringVar(self)
        self.patternselection.trace('w', self.setpattern)
        self.patternselection.set(patterns[0])  # TODO: Set Startup pattern type here
        self.patternmenu = OptionMenu(self, self.patternselection, *patterns)
        dropdownlabel = Label(self, text="Select a Pattern")
        dropdownlabel.grid(row=0, column=400, pady=(20, 0))
        self.patternmenu.grid(row=1, column=400)

    def setpattern(self, *args):
        # self.runbutton['command'] = func
        patterntype = self.patternselection.get()
        if patterntype == 'layeredflowers':
            self.set_layered_flowers()
        elif patterntype == 'radialangular':
            self.set_radial_angular()
        elif patterntype == 'sinespiral':
            self.set_sin_spiral()

    def set_layered_flowers(self):
        # self.patterntype = "layeredflowers"
        self.clear()
        layers = Parameter(self, label="layers", from_=10, to=200, row=3)
        layers.set(100)
        angle1 = Parameter(self, label="rotation angle", from_=-20.0, to=20.0, resolution=0.1, bigincrement=0.1, row=4)
        npetals = Parameter(self, label="petals", from_=1.0, to=80, resolution=1, tickinterval=9, row=5)
        npetals.set(2)
        innerdepth = Parameter(self, label="Petal Depth", from_=0, to=6, resolution=0.1, bigincrement=0.1, row=6)
        innerdepth.set(1)
        size = Parameter(self, label="size", from_=1, to=10, row=7)
        pensize = Parameter(self, label="pen size", from_=1, to=40, row=8)

        self.parameters = {'layers': layers, "npetals": npetals, "innerdepth": innerdepth, "rotate": angle1, "sizefactor": size, "pensize": pensize}

    def set_radial_angular(self):
        # self.patterntype = "radialangular"
        # for p in self.parameters.values():
        #     p.grid_forget()
        self.clear()

        size = Parameter(self, label="Size", from_=10, to=1000, row=3)
        size.set(500)

        n_angles = IntVar(self)

        self.spacedarea.grid(row=6, column=0, columnspan=800)

        pensize =  Parameter(self, label="Pen Size", from_=1, to=40, row=10)
        # self.anglearea.grid_columnconfigure(weight=1)

        self.parameters = {"size": size, 'pensize': pensize}  # for the parameters that feed into the pattern function
        self.progparams = {'n_angles': n_angles}  # for the parameters that help create function parameters, but dont feed in directly

        options = [1, 2, 3, 4]  # number of possible angles
        n_angles.trace('w', self.make_angle_boxes)
        n_angles.set(options[0])

        n_angles_menu = OptionMenu(self, n_angles, *options)
        dropdownlabel = Label(self, text="Number of Angles:")
        dropdownlabel.grid(row=4, column=400, pady=(10, 0))
        n_angles_menu.grid(row=5, column=400)

        self.progparams['n_angles'] = n_angles
        self.progparams['n_angles_menu'] = n_angles_menu
        self.progparams['n_angle_label'] = dropdownlabel

    def make_angle_boxes(self, *args):
        menu = self.progparams['n_angles']
        n = menu.get()
        prevparams = []
        # TODO: add turncycle and jank to prevparams
        if 'angleparams' in self.progparams.keys():
            for box in self.progparams['angleparams']:
                entry = []
                for i, widget in enumerate(box):
                    if i == 0 or i == 2:
                        entry.append(widget.get())
                    widget.grid_forget()
                prevparams.append(entry)

        self.progparams['angleparams'] = []
        if 'turncycle' in self.parameters.keys():
            self.parameters['turncycle'].grid_forget()
        if 'jank' in self.parameters.keys():
            self.parameters['jank'].grid_forget()

        for i in range(n):
            anglevar = StringVar()
            # anglevar.trace('w', self.set_angles)
            anglebox = Entry(self.spacedarea, width=5, textvariable=anglevar)
            label1 = Label(self.spacedarea, text=f"angle {str(i + 1)}")

            curvevar = StringVar()
            # curvevar.trace('w', self.set_angles)
            curvebox = Entry(self.spacedarea, width=5, textvariable=curvevar)
            label2 = Label(self.spacedarea, text=f"curve {str(i + 1)}")
            if len(prevparams) > i:
                anglevar.set(prevparams[i][0])
                curvevar.set(prevparams[i][1])
            else:
                if i == 0:
                    anglevar.set(125)
                    curvevar.set(5)
                else:
                    anglevar.set(0)
                    curvevar.set(0)
            if i == 1:
                turncycle = Scale(self.spacedarea, orient='horizontal', from_=0, to=5, label='turn cycle')
                turncycle.grid(row=9, column=100, rowspan=3)
                jank = Scale(self.spacedarea, orient='horizontal', from_=0, to=600, label="jank")
                jank.grid(row=12, column=100, rowspan=3)
                self.parameters['turncycle'] = turncycle
                self.parameters['jank'] = jank

            col = 20 * (i + 1)  # just so that I have flexibility in positioning things later if I make changes
            label1.grid(row=9, column=col, pady=10)
            anglebox.grid(row=10, column=col, padx=20)
            label2.grid(row=12, column=col, padx=20)
            curvebox.grid(row=14, column=col)
            self.progparams['angleparams'].append(
                [anglebox, label1, curvebox, label2]
            )
            # self.progparams['curveboxes'].append([curvebox, label2])

    def set_angles(self, *args):
        angleparams = self.progparams['angleparams']
        angles = [[i[0].get(), i[2].get()] for i in angleparams]

        for i in range(len(angles)):
            angle = angles[i]
            # print('angle', angle)
            for j in range(len(angle)):
                val = angle[j]
                try:
                    angles[i][j] = float(val)
                except ValueError:
                    angles[i][j] = len(val)
                    print("angle values should be numerical. Using length of input as angle")
        self.parameters['angles'] = [i for i in angles if i[0] != 0]
        print(self.parameters['angles'])

    def set_sin_spiral(self):
        self.clear()

        pady = 5

        n_strands = Parameter(self, label="Number of Waves", from_=1, to=300, row=10, pady=pady)
        length = Parameter(self, label="Length", from_=0, to=50, row=12, pady=pady)
        x_shift = Parameter(self, label="Shift X", from_=0, to=50, row=14, pady=pady)
        y_shift = Parameter(self, label="Shift Y", from_=0, to=50, row=18, pady=pady)
        rotation = Parameter(self, label="Rotation", from_=-18.0, to=18.0, row=22, pady=pady)
        rotaterate = Parameter(self, label="Rotation Multiplier", from_=0, to=10, row=26, resolution=0.1, bigincrement=0.1, pady=pady)
        wavelen = Parameter(self, label="Wavelength", from_=0, to=500, row=30, pady=pady)
        wl_shift = Parameter(self, label="Wavelength Shift", from_=0, to=10, row=34, pady=pady)
        amp = Parameter(self, label="Ampitude", from_=0, to=500, row=38, pady=pady)
        amp_shift = Parameter(self, label="Amplitude Shift", from_=0, to=100, row=42, pady=pady)
        pensize = Parameter(self, label="Pen Size", from_=1, to=40, row=46, pady=pady)

        n_strands.set(100)
        length.set(30)
        x_shift.set(1)
        rotaterate.set(1)
        wavelen.set(50)
        amp.set(100)

        self.parameters = {'strands': n_strands, 'xshift': x_shift,
                           'yshift': y_shift, "rotate": rotation,
                           'rotaterate': rotaterate,
                           'wavelength': wavelen, 'amplitude': amp,
                           'wlshift': wl_shift, 'ampshift':amp_shift,
                           'length': length, 'pensize': pensize}

    def clear(self):
        for p in self.parameters.values():
            if isinstance(p, Widget):
                p.grid_forget()
        self.spacedarea.grid_forget()
        for item in self.progparams.values():
            if isinstance(item, Widget):
                item.grid_forget()

    def run(self, colorscheme):
        # bye()
        reset()
        speed = 10
        drawspeed = 1000
        default_resolution = (1920, 1200)
        smaller_resolution = (1520, 800)
        print('running')
        setup(drawspeed, speed, 'black', hide=True, resolution=default_resolution)
        # parameters = {k: v.get() for k, v in self.parameters.items() if isinstance(v, Widget)}
        parameters = {}
        for param in self.parameters.items():
            label, value = param[0], param[1]
            if not isinstance(value, (int, float, str, list, tuple)):
                parameters[label] = value.get()
            else:
                parameters[label] = value

        if self.patternselection.get() == "layeredflowers":
            LVL2.layered_flowers(**parameters, colors=colorscheme)
        elif self.patternselection.get() == "radialangular":
            self.set_angles()
            RadialAngularPattern(**parameters, colors=colorscheme).drawpath()
        elif self.patternselection.get() == 'sinespiral':
            pensize = parameters.pop('pensize')
            DrawPath(LVL2.sin_spiral(**parameters), colors=colorscheme, pensize=pensize)
        wait()


class ColorSchemeTab(Tab):
    def __init__(self, master):
        super().__init__(master)
        self.debug = False
        self.default = {
            'r': [255, 255, 255, 220, 75, 3, 3, 30, 125, 220, 255],
            'g': [0, 150, 255, 255, 255, 255, 145, 3, 3, 3, 0],
            'b': [0, 0, 0, 3, 3, 240, 255, 255, 255, 255, 0]
        }
        self.resetcolors = True
        # self.colordict = deepcopy(self.default)
        self._colordict = deepcopy(self.default)
        # self.colordict = self.rainbow.copy()
        self.totalcolors = Parameter(self, label="Total Colors (fade smoothness)", from_=1, to=300, command=self.check_ratio_tot, row=5)
        self.totalcolors.set(100)
        self.colorstops = Parameter(self, label="Number of Stops", from_=1, to=11, command=self.update_colorstops, row=10)
        self.colorstops.set(5)
        self.defaultcolors = Button(self, text='Load Default Colors', command=self.reset_colors_to_default)
        self.defaultcolors.grid(row=18, column=3, columnspan=300)

        self.spacedarea.grid(row=20, column=0, columnspan=800)

        self.colorshift = Parameter(self, label="Shift Position", from_=-6, to=6, row=25, command=self.shift_color, bigincrement=1)
        self.previousshift = 0

    @property
    def colorscheme(self):
        scheme = ColorScheme(self.currentcolors, self.totalcolors.get())
        return scheme

    @property
    def currentcolors(self):
        colors = {'r': [], 'g': [], 'b': []}
        for key in colors:
            colors[key] = self.colordict[key][:self.colorstops.get()]
        return colors

    @property
    def colordict(self):
        return self._colordict

    @colordict.setter
    def colordict(self, val):
        self._colordict = val
        # self.update_color_boxes()

    def reset_colors_to_default(self):
        self.resetcolors = True
        print('pre:', self.colordict)
        self.colordict = deepcopy(self.default)
        self.colordict = deepcopy(self.default)
        print('post:', self.colordict)
        self.colorshift.set(0)
        self.update_color_boxes()

    def update_colorstops(self, *args):
        self.check_ratio_stops(*args)
        self.make_color_boxes()

    def shift_color(self, *args):
        # TODO FIX!
        colordict = deepcopy(self.colordict)
        amt = self.colorshift.get()
        # if self.is_default_colors():
        for j in range(abs(amt)):
            for color in colordict:
                for i in range(len(colordict[color])):
                    interval = amt - self.previousshift
                    print('interval', interval)
                    ind = (i - interval) % len(colordict[color])
                    colordict[color][i] = self.colordict[color][ind]
                    # print('regind', i, 'staticind', ind)
                if True:
                    print("shift_color if default:")
                    print("pre:", self.colordict[color])
                    print("post:", colordict[color])
        self.previousshift = amt
        self.colordict = colordict
        self.update_color_boxes()

        # else:
        #     print('Cannot shift, colors are not default')

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

        if self.debug:
            print("is_default_colors:")
            print('r\n', def_r, '\n', r, '\n', r_match, '\n')
            print('g\n', def_g, '\n', g, '\n', g_match, '\n')
            print('b\n', def_b, '\n', b, '\n', b_match, '\n')

        return all([r_match, g_match, b_match])

    def check_ratio_tot(self, tot):
        tot = int(tot)
        if tot < self.colorstops.get():
            self.colorstops.set(tot)

    def check_ratio_stops(self, stops):
        stops = int(stops)
        if stops > self.totalcolors.get():
            self.totalcolors.set(stops)

    def rgb_tk(self, rgb):
        rgb = tuple([int(i) for i in rgb])
        return "#%02x%02x%02x" % rgb

    def make_color_boxes(self):
        n = self.colorstops.get()
        prevparams = []
        if 'colorparams' in self.progparams.keys():
            for group in self.progparams['colorparams']:
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

        self.progparams['colorparams'] = []

        r_row, g_row, b_row = 10, 14, 18

        label_r = Label(self.spacedarea, text="R")
        label_g = Label(self.spacedarea, text="G")
        label_b = Label(self.spacedarea, text="B")

        label_r.grid(row=r_row, column=0, padx=(0, 10))
        label_g.grid(row=g_row, column=0, padx=(0, 10))
        label_b.grid(row=b_row, column=0, padx=(0, 10))

        for i in range(n):
            col_label = Label(self.spacedarea, text=str(i + 1))

            red = StringVar()
            red.trace('w', lambda *x: self.update_color_dict(x, index=i, key='r'))
            redbox = Entry(self.spacedarea, width=3, textvariable=red)

            green = StringVar()
            green.trace('w', lambda *x: self.update_color_dict(x, index=i, key='g'))
            greenbox = Entry(self.spacedarea, width=3, textvariable=green)

            blue = StringVar()
            blue.trace('w', lambda *x: self.update_color_dict(x, index=i, key='b'))
            bluebox = Entry(self.spacedarea, width=3, textvariable=blue)

            # if len(prevparams) > i and not self.resetcolors:
            #     red.set(prevparams[i][0])
            #     green.set(prevparams[i][1])
            #     blue.set(prevparams[i][2])
            # else:
            red.set(self.colordict['r'][i])
            green.set(self.colordict['g'][i])
            blue.set(self.colordict['b'][i])

            color = self.rgb_tk((red.get(), green.get(), blue.get()))
            examplebox = Frame(self.spacedarea, width=20, height=15, bg=color)

            col = 20 * (i + 1)  # just so that I have flexibility in positioning things later if I make changes
            col_label.grid(row=8, column=col, pady=10, padx=1)
            redbox.grid(row=r_row, column=col)
            greenbox.grid(row=g_row, column=col)
            bluebox.grid(row=b_row, column=col)

            examplebox.grid(row=20, column=col, pady=10)

            self.progparams['colorparams'].append(
                {'boxes': {'r': redbox, 'g': greenbox,'b': bluebox},
                 'vals': {'r': red, 'g': green, 'b': blue},
                 'label': col_label,
                 'example': examplebox})
            # self.resetcolors = False
            # pass
            # self.progparams['curveboxes'].append([curvebox, label2])

    def update_color_dict(self, *args, index, key):
        # pass
        # print(key, index)
        colparams = self.progparams['colorparams']
        values = [i['vals'] for i in colparams]
        examples = [i['example'] for i in colparams]
        newcols = deepcopy(self.colordict)
        for i in range(len(values)):  # for index of values (tk StringVar objects):
            group = values[i]  # group =  {'r': rVar, 'g': gVar, 'b': bVar)
            rgb = []
            for key in group:  # for 'r', 'g', and 'b':
                shift = self.colorshift.get()  # get the value of the shift parameter
                ind = (i - 1) % len(self.colordict[key])  # set the index to edit, based on remainder of the index - shift amount
                # print(ind)
                strval = group[key].get()
                if strval != '':
                    val = int(strval)
                    self.colordict[key][ind] = val
                    newcols[key][i] = val
                    rgb.append(val)
            if len(rgb) == 3:
                examples[i].configure(bg=self.rgb_tk(rgb))
        # for k in self.colordict:
        #     print(k, self.colordict[k])
        # print('\n')
        # print('static', self.colordict)
        # print('coldict', newcols)
        self.colordict = newcols
        # self.update_color_boxes()

    def update_color_boxes(self):
        self.make_color_boxes()
        for i in range(len(self.progparams['colorparams'])):
            group = self.progparams['colorparams'][i]
            rgb = []
            for key in group['vals']:
                val = self.colordict[key][i]
                rgb.append(val)
                group['vals'][key].set(val)
        self.make_color_boxes()






rainbow1 = Colors.rainbow(50)
rainbow2 = Colors.rainbow(30)
hot1 = Colors.hot1(100)

grayscale1 = Colors.grayscale1(1000)
darkgrays = ColorScheme({'r': [0, 60], 'g': [0, 60], 'b': [0, 60]}, 20)
whiteish = ColorScheme({'r': [50, 220], 'g': [50, 220], 'b': [50, 220]}, 30)
# darkgrays.shiftlightness(0)

# defaultpattern = partial(LVL2.layered_flowers(60, 8, innerdepth=1, rotate=1, colors=rainbow1))
# pattern = None
#
# def assign_to_RAP():
#     global pattern
#     pattern = LVL2.layered_flowers(60, 8, innerdepth=1, rotate=1, colors=rainbow1)



# RadialAngularPattern(200, [90, 70], 0)
# func()
# wait()


def main():
    root = Tk()
    root.geometry("600x950")
    app = Application(master=root)



    # speed = 10
    # drawspeed = 1000
    default_resolution = (1920, 1200)
    # setup(drawspeed, speed, 'black', hide=True, resolution=(1520, 800))
    #
    # # Do stuff here
    # LVL2.layered_flowers(60, 8, innerdepth=1, rotate=1, colors=rainbow1)
    #
    # wait()
    root.mainloop()


if __name__ == "__main__":
    main()
