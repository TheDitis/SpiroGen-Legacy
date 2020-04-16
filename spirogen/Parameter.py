from tkinter import Scale


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
