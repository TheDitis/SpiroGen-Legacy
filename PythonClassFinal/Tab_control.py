from tkinter import *
from tkinter import ttk


class Root(Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.title("Spirogen")
        self.minsize(640, 640)
        # self.wm_iconbitmap()

        tabcontrol = ttk.Notebook(self)

        patterntab = ttk.Frame(tabcontrol)
        tabcontrol.add(patterntab, text="Pattern")
        colorschemetab = ttk.Frame(tabcontrol)
        tabcontrol.add(colorschemetab, text="Color Scheme")

        tabcontrol.pack(expan=1, fill='both')


if __name__ == "__main__":
    root = Root()
    root.mainloop()