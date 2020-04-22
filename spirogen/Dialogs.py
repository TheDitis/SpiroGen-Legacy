from tkinter import Frame, Toplevel, StringVar, Label, Entry, Button, IntVar, Radiobutton, Listbox
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
        # self.frame = Frame(self, width=800, height=200)
        self.pack(padx=20, pady=20)

        # for i in range(self.rows):
        #     self.grid_rowconfigure(i, minsize=1 / 8000, weight=1)
        # for i in range(self.columns):
        #     self.grid_columnconfigure(i, minsize=1 / 8000, weight=1)

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
        leftbutton = Radiobutton(self, text='Left', width=8, indicatoron=False, value=0, variable=self._direction)
        rightbutton = Radiobutton(self, text='Right', width=8, indicatoron=False, value=1, variable=self._direction)
        gotolabel = Label(self, text='Go To %:')
        gotobox = Entry(self, width=5, textvariable=self._goto)
        applybtn = Button(self, text="Apply", command=self.apply)

        # ramplightlabel.grid(row=35, column=3, columnspan=180, pady=(20, 0))
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
        session = Radiobutton(self, text="Session", width=8, indicatoron=False, value="sessions", variable=mode)
        pattern = Radiobutton(self, text="Pattern", width=8, indicatoron=False, value='patterns', variable=mode)
        colors = Radiobutton(self, text="Colors", width=8, indicatoron=False, value='colors', variable=mode)

        name = StringVar()
        namelabel = Label(self, text="Name:")
        namebox = Entry(self, textvariable=name)

        savebtn = Button(self, text="Save", command=lambda: func(mode.get(), name.get()))

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

        mode = StringVar()
        mode.set('sessions')
        session = Radiobutton(self, text="Session", width=8, indicatoron=False, value="sessions", variable=mode)
        pattern = Radiobutton(self, text="Pattern", width=8, indicatoron=False, value='patterns', variable=mode)
        colors = Radiobutton(self, text="Colors", width=8, indicatoron=False, value='colors', variable=mode)
        self._pick = None

        self._name = StringVar()
        namelabel = Label(self, text="Name:")
        namebox = Entry(self, textvariable=self._name)

        listbtn = Button(
            self,
            text="List Available",
            command=lambda: self.list_dialog(mode)
        )
        self._choosedlg = None

        loadbtn = Button(self, text="Load", command=lambda: func(mode.get(), self._name.get()))

        session.grid(row=10, column=9, columnspan=100)
        pattern.grid(row=10, column=120, columnspan=100, padx=20)
        colors.grid(row=10, column=230, columnspan=100)

        namelabel.grid(row=13, column=37, columnspan=100, pady=(20, 0))
        namebox.grid(row=15, column=10, columnspan=300, pady=(0, 20))
        listbtn.grid(row=20, column=9, columnspan=50, sticky='sw')
        loadbtn.grid(row=20, column=250, columnspan=50, sticky='se')

    def list_dialog(self, mode):
        self._choosedlg = ListAvailableDialog(self._name, mode.get())


class ListAvailableDialog(Frame):
    def __init__(self, var, type='sessions'):
        super().__init__(Toplevel())
        self.var = var
        self.master.title(f"Loadable {type.capitalize()[:-1]} Names")
        # self.master.geometry("300x400")
        self.pack(padx=30, pady=30)

        files = os.listdir(f'./SpiroGenSettings/{type}')
        lbox = Listbox(self)
        for i, file in enumerate(files):
            lbox.insert(i, file.replace('.json', ''))
        # self.list.grid(row=10, column=10, columnspan=90)
        lbox.pack(fill="both")
        lbox.bind('<<ListboxSelect>>', self.get_value)

    def get_value(self, event):
        w = event.widget
        ind = int(w.curselection()[0])
        self.var.set(w.get(ind))
