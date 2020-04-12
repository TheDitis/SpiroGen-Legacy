from spirogen import setup, Transform, Analyze, Colors, ColorScheme, Pattern, PolarPattern, Wave, Rectangle, Circle, RadialAngularPattern, FlowerPattern, FlowerPattern2, DrawPath, TimesTable, CascadeLines, LVL2, wait, reset, bye
from functools import partial
from tkinter import *
from tkinter import ttk


class Application(ttk.Notebook):
    def __init__(self, master):
        ttk.Notebook.__init__(self, master)

        patterntab = PatternTab(self)
        # patterntab = ttk.Frame(tabcontrol)
        self.add(patterntab, text="Pattern")
        colorschemetab = ColorSchemeTab(self)
        self.add(colorschemetab, text="Color Scheme")

        self.pack(expan=1, fill='both')


class Tab(Frame):
    def __init__(self, master):
        super().__init__(master)
        self._rangewidth = 500
        self.parameters = []
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
        print('w', w, 'h', h)
        print(self.parameters)
        # self.update(w)
        # param.update()
        # param.master.grid(column=1, row=param.row, pady=10, columnspan=param.master.grid.columnspan)

        # self.rangewidth = round(w * 0.9)

    # def update(self, w):
    #     for param in self.parameters:
            # param.grid_forget()
            # param.length = w
            # param.grid(column=param.column, row=param.row, columnspan=param.columnspan)
            # pass

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
        self.grid(column=self.column, columnspan=self.columnspan, row=self.row)

    def __repr__(self):
        return f"{self.label}: {self.get()}"


class PatternTab(Tab):
    def __init__(self, master):
        self.rangewidth = 500

        super().__init__(master)

        self.layers = Parameter(self, label="layers", from_=10, to=100, row=1)
        self.layers.set(60)
        self.angle1 = Parameter(self, label="rotation angle", from_=-20.0, to=20.0, resolution=0.1, bigincrement=0.1, row=2)
        self.npetals = Parameter(self, label="petals", from_=1.0, to=80, resolution=1, tickinterval=9, row=3)
        self.innerdepth = Parameter(self, label="Petal Depth", from_=0, to=6, resolution=0.1, bigincrement=0.1, row=4)
        self.size = Parameter(self, label="size", from_=1, to=10, row=5)
        self.pensize = Parameter(self, label="pen size", from_=1, to=10, row=6)

        self.parameters = [self.layers, self.angle1, self.npetals, self.innerdepth, self.size, self.pensize]

        # self.master.bind("<Configure>", self.config)

        self.getbutton = Button(self, text="Load")
        self.savebutton = Button(self, text="Save")
        self.runbutton = Button(self, text="Run", command=self.run)
        #
        # self.layers.grid(column=1, row=1, pady=10, columnspan=790)
        # self.angle1.grid(column=0, row=2, pady=10, columnspan=790)
        # self.npetals.grid(column=1, row=3, pady=10, columnspan=790)
        # self.innerdepth.grid(column=1, row=4, pady=10, columnspan=790)
        # self.size.grid(column=1, row=5, pady=10, columnspan=790)
        # self.pensize.grid(column=1, row=6, pady=10, columnspan=790)

        self.getbutton.grid(column=1, row=10)
        self.savebutton.grid(column=2, row=10)
        self.runbutton.grid(column=10, row=10, pady=10)

        # self.grid_propagate(2)
        # self.createWidgets()
        # self.grid(padx=30, pady=30)

    def setpattern(self, func):
        self.runbutton['command'] = func

    def run(self):
        # bye()
        reset()
        speed = 10
        drawspeed = 1000
        default_resolution = (1920, 1200)
        smaller_resolution = (1520, 800)
        setup(drawspeed, speed, 'black', hide=True, resolution=default_resolution)
        LVL2.layered_flowers(self.layers.get(), self.npetals.get(), self.innerdepth.get(), self.size.get(), self.pensize.get(), self.angle1.get(), colors=rainbow1)


class ColorSchemeTab(Tab):
    def __init__(self, master):
        super().__init__(master)

        self.totalcolors = Scale(self, label="Total Colors (fade smoothness)", orient="horizontal", length=self.rangewidth, from_=1, to=300, command=self.check_ratio_tot)
        self.colorstops = Scale(self, label="Total Colors (fade smoothness)", orient="horizontal", length=self.rangewidth, from_=1, to=15, command=self.check_ratio_stops)

        self.totalcolors.grid(column=1, row=1, pady=10, columnspan=10)
        self.colorstops.grid(column=1, row=2, pady=10, columnspan=10)

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
    root.geometry("600x700")
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
