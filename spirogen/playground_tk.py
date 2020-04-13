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
        self.functionalparameters = {}

        super().__init__(master)
        self.anglearea = Frame(self)

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

        size = Parameter(self, label="Size", from_=100, to=1000, row=3)

        n_angles = IntVar(self)

        self.anglearea.grid(row=6, column=0, columnspan=800)
        # self.anglearea.grid_columnconfigure(weight=1)

        self.parameters = {"size": size}
        self.functionalparameters = {'n_angles': n_angles}

        options = [1, 2, 3, 4]
        n_angles.trace('w', self.make_angle_boxes)
        n_angles.set(options[0])

        n_angles_menu = OptionMenu(self, n_angles, *options)
        dropdownlabel = Label(self, text="Number of Angles:")
        dropdownlabel.grid(row=4, column=400, pady=(10, 0))
        n_angles_menu.grid(row=5, column=400)

    def make_angle_boxes(self, *args):
        menu = self.functionalparameters['n_angles']
        n = menu.get()
        if 'angleboxes' in self.functionalparameters.keys():
            for box in self.functionalparameters['angleboxes']:
                box.grid_forget()
        self.functionalparameters['angleboxes'] = []

        deg_label = Label(self.anglearea, text="Turn Angle (deg):", anchor='w', width=40)
        deg_label.grid(row=10, column=0, ipadx=20)

        for i in range(n):
            # inputvar = DoubleVar()
            answerbox = Entry(self.anglearea, width=5)
            label = Label(self.anglearea, text=str(i))

            col = 20 * i
            print(col)
            label.grid(row=9, column=col, pady=10)
            answerbox.grid(row=10, column=col, padx=20)
            self.functionalparameters['angleboxes'].append(answerbox)

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
        parameters = {k: v.get() for k, v in self.parameters.items()}
        if self.patternselection.get() == "layeredflowers":
            LVL2.layered_flowers(**parameters, colors=colorscheme)
        elif self.patternselection.get() == "radialangular":
            RadialAngularPattern(**parameters, angles=[[125, 0], [75, 0], [32], [55]], colors=colorscheme).drawpath()


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



    speed = 10
    drawspeed = 1000
    default_resolution = (1920, 1200)
    setup(drawspeed, speed, 'black', hide=True, resolution=(1520, 800))
    #
    # # Do stuff here
    # LVL2.layered_flowers(60, 8, innerdepth=1, rotate=1, colors=rainbow1)
    #
    wait()
    root.mainloop()


if __name__ == "__main__":
    main()
