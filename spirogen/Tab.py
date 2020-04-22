from tkinter import Frame
from tkinter.font import Font


class Tab(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.h1 = Font(family='TkDefaultFont', size=20, weight='bold')
        self.h2 = Font(family='TkDefaultFont', size=15, weight='bold')
        self._rangewidth = 500
        self.pack(padx=50, pady=50)
        self._rangewidth = 500
        self._columns = 800
        self._rows = 800
        self.bind("<Configure>", self.config)

        self._spacedarea = Frame(self)
        self._progparams = {}

    def config(self, event):
        w, h = event.width, event.height
        for i in range(self._rows):
            self.grid_rowconfigure(i, minsize=h/8000, weight=1)
        for i in range(self._columns):
            self.grid_columnconfigure(i, minsize=w/8000, weight=1)

    @property
    def rangewidth(self):
        return self._rangewidth

    @rangewidth.setter
    def rangewidth(self, val):
        self._rangewidth = val