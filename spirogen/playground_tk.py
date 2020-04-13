from spirogen import setup, Transform, Analyze, Colors, ColorScheme, Pattern, PolarPattern, Wave, Rectangle, Circle, RadialAngularPattern, FlowerPattern, FlowerPattern2, DrawPath, TimesTable, CascadeLines, LVL2, wait, reset, bye
from functools import partial
from tkinter import *
from tkinter import ttk


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
    def __init__(self, master=None, columnspan=700, column=1, row=None, **kwargs):
        self.rangewidth = 10000
        super().__init__(master, length=self.rangewidth, activebackground='green', orient="horizontal", **kwargs)
        self.column = column
        self.columnspan = 790
        self.row = row
        self.label = kwargs['label']
        self.grid(column=self.column, columnspan=self.columnspan, row=self.row, pady=15)

    def __repr__(self):
        return f"{self.label}: {self.get()}"


class PatternTab(Tab):
    def __init__(self, master):
        self.parameters = {}
        self.progparams = {}

        super().__init__(master)
        self.spacedarea = Frame(self)

        # Setting dropdown menu for selecting pattern type
        patterns = ['layeredflowers', 'radialangular']
        self.patternselection = StringVar(self)
        self.patternselection.trace('w', self.setpattern)
        self.patternselection.set(patterns[1])
        self.patternmenu = OptionMenu(self, self.patternselection, *patterns)
        dropdownlabel = Label(self, text="Select a Pattern")
        dropdownlabel.grid(row=0, column=400, pady=(20, 0))
        self.patternmenu.grid(row=1, column=400)

    def set_layered_flowers(self):
        # self.patterntype = "layeredflowers"
        for p in self.parameters.values():
            p.grid_forget()
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
        for p in self.parameters.values():
            p.grid_forget()

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

    def make_angle_boxes(self, *args):
        menu = self.progparams['n_angles']
        n = menu.get()
        prevparams = []
        if 'angleparams' in self.progparams.keys():
            for box in self.progparams['angleparams']:
                entry = []
                for i, widget in enumerate(box):
                    print(i)

                    if i == 0 or i == 2:
                        entry.append(widget.get())
                    widget.grid_forget()
                prevparams.append(entry)
        print(prevparams)

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
                    print("angle values must be numerical!")
        self.parameters['angles'] = [i for i in angles if i[0] != 0]

    def setpattern(self, *args):
        # self.runbutton['command'] = func
        patterntype = self.patternselection.get()
        if patterntype == 'layeredflowers':
            self.set_layered_flowers()
        elif patterntype == 'radialangular':
            self.set_radial_angular()

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
            print(self.parameters)
            RadialAngularPattern(**parameters, colors=colorscheme).drawpath()
        wait()


class ColorSchemeTab(Tab):
    def __init__(self, master):
        super().__init__(master)
        # self.colorscheme = rainbow1
        self.totalcolors = Parameter(self, label="Total Colors (fade smoothness)", from_=1, to=300, command=self.check_ratio_tot, row=1)
        self.totalcolors.set(100)
        self.colorstops = Parameter(self, label="Number of Stops", from_=1, to=15, command=self.check_ratio_stops, row=2)
        self.colordict = {
            'r': [[255, 255], [255, 255], [255, 220], [220, 75], [75, 3], [3, 3], [3, 30], [30, 125], [125, 220], [220, 255]],
            'g': [[0, 150], [150, 255], [255, 255], [255, 255], [255, 255], [255, 145], [145, 3], [3, 3], [3, 3], [3, 0]],
            'b': [[0, 0], [0, 0], [0, 3], [3, 3], [3, 240], [240, 255], [255, 255], [255, 255], [255, 255], [255, 0]]
        }
        # self.totalcolors.grid(column=1, row=1, pady=10, columnspan=10)
        # self.colorstops.grid(column=1, row=2, pady=10, columnspan=10)

    @property
    def colorscheme(self):
        return ColorScheme(self.colordict, self.totalcolors.get())

    def check_ratio_tot(self, tot):
        tot = int(tot)
        if tot < self.colorstops.get():
            self.colorstops.set(tot)

    def check_ratio_stops(self, stops):
        stops = int(stops)
        if stops > self.totalcolors.get():
            self.totalcolors.set(stops)







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
    root.geometry("600x750")
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
