"""
File: Dialogs.py
Author: Ryan McKay
Date: April 18, 2020

Purpose: These dialogs allow for extra functionality for the SpiroGen interface.
    They are all very simple with only a few widgets each
Input: All of the dialogs take a function to run upon submit except for the
    ListAvailableDialog, which takes the stringvar for the entry box for the
    name of the setting, which is set when a name is clicked on. it also takes
    the type of load/save as a string. This is the folder it is to list from.
Output:
    They all run the function that they are given when submit is clicked.
"""
from tkinter import Frame, Toplevel, StringVar, Label, Entry, Button, IntVar, \
    Radiobutton, Listbox, Scale
from spirogen.interface.Parameter import Parameter
import os


class ShiftLightnessDialog(Frame):
    def __init__(self, func):
        super().__init__(Toplevel())
        self.master.title('Shift Lightness')
        self._func = func
        self.pack(padx=20, pady=20)

        self._amount = StringVar()
        self._amount.set(0)
        amtlabel = Label(self, text="Amount:")
        amtbox = Entry(self, width=5, textvariable=self._amount)
        applybtn = Button(self, text="Apply", command=self.apply)

        amtlabel.grid(row=38, column=3, columnspan=120, pady=10)
        amtbox.grid(row=38, column=125, columnspan=80)
        applybtn.grid(row=50, column=40)

    def apply(self):
        try:
            amt = round(float(self._amount.get()))
            if abs(amt) <= 255:
                self._func(amt)
                self.master.destroy()
            else:
                print("amount must be between -255 and 255.")
        except ValueError as error:
            print("Value must be numerical.")
            raise error


class RampLightnessDialog(Frame):
    def __init__(self, func):
        super().__init__(Toplevel())
        self.master.title('Ramp Lightness')
        self._func = func
        self.pack(padx=20, pady=20)

        self._amount = StringVar()
        self._direction = IntVar()
        self._goto = StringVar()

        self._amount.set(-255)
        self._direction.set(0)
        self._goto.set(50)

        # ramplightlabel = Label(self.rl_window, text='Ramp Lightness:')
        amtlabel = Label(self, text='Amount:')
        amtbox = Entry(self, width=5, textvariable=self._amount)
        directionlabel = Label(self, text='Direction:')
        leftbutton = Radiobutton(
            self, text='Left', width=8, indicatoron=False, value=0,
            variable=self._direction
        )
        rightbutton = Radiobutton(
            self, text='Right', width=8, indicatoron=False, value=1,
            variable=self._direction
        )
        gotolabel = Label(self, text='Go To %:')
        gotobox = Entry(self, width=5, textvariable=self._goto)
        applybtn = Button(self, text="Apply", command=self.apply)

        amtlabel.grid(row=38, column=3, columnspan=120, pady=10)
        amtbox.grid(row=38, column=125, columnspan=80)
        directionlabel.grid(row=42, column=3, columnspan=90, pady=10)
        leftbutton.grid(row=42, column=100, columnspan=70)
        rightbutton.grid(row=42, column=180, columnspan=70)
        gotolabel.grid(row=46, column=3, columnspan=120, pady=10)
        gotobox.grid(row=46, column=130, columnspan=80)
        applybtn.grid(row=50, column=40)

    def apply(self):
        try:
            amt = round(float(self._amount.get()))
            direction = int(self._direction.get())
            goto = round(float(self._goto.get()))
            self._func(amt, direction, goto)
            self.master.destroy()
        except ValueError as error:
            print("one of the parameters in non-numerical.")
            raise error


class SaveDialog(Frame):
    def __init__(self, func):
        super().__init__(Toplevel())
        self.master.title("Save")
        self.pack(padx=30, pady=30)

        mode = StringVar()
        mode.set('sessions')
        session = Radiobutton(
            self, text="Session", width=8, indicatoron=False, value="sessions",
            variable=mode
        )
        pattern = Radiobutton(
            self, text="Pattern", width=8, indicatoron=False, value='patterns',
            variable=mode
        )
        colors = Radiobutton(
            self, text="Colors", width=8, indicatoron=False, value='colors',
            variable=mode
        )

        name = StringVar()
        namelabel = Label(self, text="Name:")
        namebox = Entry(self, textvariable=name)

        savebtn = Button(
            self, text="Save", command=lambda: func(mode.get(), name.get())
        )

        session.grid(row=10, column=9, columnspan=100)
        pattern.grid(row=10, column=120, columnspan=100, padx=20)
        colors.grid(row=10, column=230, columnspan=100)

        namelabel.grid(row=13, column=37, columnspan=100, pady=(20, 0))
        namebox.grid(row=15, column=10, columnspan=300, pady=(0, 20))
        savebtn.grid(row=20, column=250, columnspan=50, sticky='se')


class LoadDialog(Frame):
    def __init__(self, func):
        super().__init__(Toplevel())
        self.master.title("Load")
        self.pack(padx=30, pady=30)

        # self.master.protocol("WM_DELETE_WINDOW", self.on_close)

        mode = StringVar()
        mode.set('sessions')
        session = Radiobutton(
            self, text="Session", width=8, indicatoron=False, value="sessions",
            variable=mode
        )
        pattern = Radiobutton(
            self, text="Pattern", width=8, indicatoron=False, value='patterns',
            variable=mode
        )
        colors = Radiobutton(
            self, text="Colors", width=8, indicatoron=False, value='colors',
            variable=mode
        )
        self._pick = None
        #
        name = StringVar()
        namelabel = Label(self, text="Name:")
        namebox = Entry(self, textvariable=name)

        listbtn = Button(
            self,
            text="List Available",
            command=lambda: self.list_dialog(name, mode)
        )
        self._choosedlg = None

        loadbtn = Button(
            self, text="Load",
            command=lambda: func(mode.get(), name.get())
        )

        session.grid(row=10, column=9, columnspan=100)
        pattern.grid(row=10, column=120, columnspan=100, padx=20)
        colors.grid(row=10, column=230, columnspan=100)

        namelabel.grid(row=13, column=37, columnspan=100, pady=(20, 0))
        namebox.grid(row=15, column=10, columnspan=300, pady=(0, 20))
        listbtn.grid(row=20, column=9, columnspan=50, sticky='sw')
        loadbtn.grid(row=20, column=250, columnspan=50, sticky='se')

    def list_dialog(self, name, mode):
        ListAvailableDialog(name, mode.get())


class ListAvailableDialog(Frame):
    def __init__(self, namevar, type='sessions'):
        super().__init__(Toplevel())
        self.namevar = namevar
        self.master.title(f"Loadable {type.capitalize()[:-1]} Names")
        self.pack(padx=30, pady=30)

        files = os.listdir(f'./SpiroGenSettings/{type}')
        lbox = Listbox(self)
        for i, file in enumerate(files):
            lbox.insert(i, file.replace('.json', ''))
        lbox.pack(fill="both")
        lbox.bind('<<ListboxSelect>>', self.get_value)

    def get_value(self, event):
        w = event.widget
        ind = int(w.curselection()[0])
        print('widget', w)
        self.namevar.set(w.get(ind))


class ColorSwatchDialog(Frame):
    def __init__(self, targetswatch, curcolors, defaultcolors):
        # for k in curcolors:
        #     print(curcolors[k])
        super().__init__(Toplevel())
        self.master.title('Update Color')
        self.pack(padx=10, pady=10)
        self.targetbox = targetswatch
        self.targetvars = targetswatch.targets
        self.curcolors = curcolors
        self.defaultcolors = defaultcolors

        self.colorview = Frame(self, width=200, height=200, bg=targetswatch.color)
        self.colorview.grid(column=5, row=5, rowspan=200, columnspan=200)

        rscale = Parameter(
            self, label='R', width=200, from_=0, to=255, row=210, pady=0,
            troughcolor='red', activebackground='red',
            command=lambda *x: self.update_color('r')
        )
        gscale = Parameter(
            self, label='G', width=200, from_=0, to=255, row=220, pady=0,
            troughcolor='green', activebackground='green',
            command=lambda *x: self.update_color('g')
        )
        bscale = Parameter(
            self, label='B', width=200, from_=0, to=255, row=230, pady=0,
            troughcolor='blue', activebackground='blue',
            command=lambda *x: self.update_color('b')
        )
        self.colorparams = {'r': rscale, 'g': gscale, 'b': bscale}
        for color in self.targetvars:
            try:
                val = round(float(self.targetvars[color].get()))
            except ValueError:
                print('color values must be numeric and between 0 and 255')
                val = 0
            self.colorparams[color].set(val)
        self.swatch_area = Frame(self)
        self.swatch_area.grid(column=0, row=5, padx=10)
        self.setup_swatch_selection()

    def update_color(self, color):
        rgb = []
        indexloc = {'r': 0, 'g': 1, 'b': 2}
        for k in self.colorparams:
            param = self.colorparams[k]
            val = round(float(param.get()))
            if color == k:
                self.targetvars[k].set(val)
                singlecolor = [0, 0, 0]
                singlecolor[indexloc[k]] = val
                singlecolor = self.rgb_tk(singlecolor)
                param.configure(activebackground=singlecolor)
            rgb.append(val)
        rgb = self.rgb_tk(rgb)
        self.colorview.configure(bg=rgb)
        self.targetbox.configure(bg=rgb)

    def setup_swatch_selection(self):
        current = self.curcolors
        defaultcolors = self.defaultcolors
        length = len(self.curcolors['r'])
        print('\n')
        print('\n')
        for k in self.curcolors:
            print(self.curcolors[k])
        for i in range(length):
            rgb = tuple(current[k][i] for k in ['r', 'g', 'b'])
            # print(rgb)
            swatch = SelectableColorSwatch(
                self.swatch_area, color=rgb, func=self.grab_swatch_color
            )
            swatch.grid(column=10*(i+1), row=10, padx=2)

            rgb = tuple(defaultcolors[k][i] for k in ['r', 'g', 'b'])
            swatch = SelectableColorSwatch(self.swatch_area, rgb,
                                           self.grab_swatch_color)
            swatch.grid(column=10 * (i + 1), row=20, padx=2, pady=4)

    def grab_swatch_color(self, color):
        color = {'r': color[0], 'g': color[1], 'b': color[2]}
        for k in color:
            self.colorparams[k].set(color[k])

    @staticmethod
    def rgb_tk(rgb):
        rgb = tuple([round(float(i)) for i in rgb])
        output = "#%02x%02x%02x" % rgb
        return output


class SelectableColorSwatch(Frame):
    def __init__(self, master, color, func):
        self.color = color
        super().__init__(
            master, bg=self.rgb_tk(self.color), height=15, width=20
        )
        self.bind("<Button-1>", lambda *x: func(color))

    @staticmethod
    def rgb_tk(rgb):
        rgb = tuple([round(float(i)) for i in rgb])
        output = "#%02x%02x%02x" % rgb
        return output
