from tkinter import Frame, Listbox, Toplevel, Label, Button, Message, Scrollbar
from tkinter.font import Font
from PIL import Image, ImageTk
from itertools import count
import json


class HelpIndex(Frame):
    """
    This is a navigation for the tutorial. It can be launched from the help menu
    in the top bar.
    """
    def __init__(self):
        super().__init__(Toplevel())
        self.pack(padx=20, pady=20)

        # the labels with the corresponding page numbers
        self.options = {
            'Pattern Tab': 1, 'Color Schemes': 8, 'Loading & Saving': 5,
            'Editing Colors': 16
        }
        self.index = Listbox(self)
        for i, label in enumerate(self.options):
            self.index.insert(i, label)
        self.index.bind('<<ListboxSelect>>', self.launch_help)
        self.index.grid(row=10, column=0)

    def launch_help(self, event):
        w = event.widget
        ind = int(w.curselection()[0])
        value = w.get(ind)
        tut = Tutorial()
        tut.goto(self.options[value])


class Tutorial(Frame):
    """
    This is a simple walkthrough of the functionality of the program.
    """
    def __init__(self):
        super().__init__(Toplevel())
        self.master.title('Tutorial')
        self.pack(padx=20, pady=20)
        self.imagepath = './spirogen/interface/SpiroGenSettings/tutorial/'
        self.assetpath = ''

        p = './spirogen/interface/SpiroGenSettings/tutorial/tutorial_pages.json'
        with open(p, 'r') as file:
            self.tutdata = json.load(file)
        self.h1 = Font(family='TkDefaultFont', size=40,
                       weight='bold')  # Big heading font
        self.h2 = Font(family='TkDefaultFont', size=20, weight='bold')
        self.currentindex = -1
        self.image = None
        self.titletext = None
        self.text = None
        self.next()
        nextbtn = Button(
            self, text="Next", command=self.next, bg='blue', height=4, width=10
        )
        nextbtn.grid(row=220, column=200, padx=30, pady=30)
        backbtn = Button(
            self, text="Back", command=self.back, bg='blue', height=4, width=10
        )
        backbtn.grid(row=220, column=10, padx=30, pady=30)

    @property
    def path(self):
        return self.imagepath + self.tutdata[self.currentindex]['image']

    @property
    def indexinrange(self):
        return 0 <= self.currentindex < len(self.tutdata)

    def next(self):
        self.currentindex += 1
        if self.indexinrange:
            self.load_page()
        else:
            self.master.destroy()

    def back(self):
        if not self.currentindex == 0:
            self.currentindex -= 1
            self.load_page()

    def load_page(self):
        image = Image.open(self.path)
        currentpage = self.tutdata[self.currentindex]
        # image = resize_img(image)
        photo = ImageTk.PhotoImage(image)
        if self.image:
            self.image.grid_forget()
        if self.text:
            self.text.grid_forget()
        if self.titletext:
            self.titletext.grid_forget()
        if '.gif' in self.path:
            self.image = ImageLabel(self, borderwidth=2, relief="solid")
            # self.image.image = photo  # keep a reference!
            self.image.grid(row=0, column=0, columnspan=205, rowspan=205)
            if self.currentindex == 0:
                size = 900
            else:
                size = 400
            self.image.load(self.path, size)
        else:
            self.image = Label(self, image=photo, borderwidth=2, relief="solid")
            self.image.image = photo  # keep a reference!
            self.image.grid(row=0, column=0, columnspan=205, rowspan=205)
        title = currentpage['title']
        text = currentpage['text']
        if "Welcome" in self.path:
            self.titletext = Message(
                self, text=title, font=self.h1, width=500, justify='center'
            )
            self.text = Message(
                self, text=text, font=self.h2, width=500, justify='center'
            )
            self.titletext.grid(row=210, column=0, columnspan=205, pady=20)
            self.text.grid(row=215, column=0, columnspan=205, pady=20)
        else:
            self.titletext = Message(
                self, text=title, font=self.h1, width=500, justify='center'
            )
            self.text = Message(
                self, text=text, font=self.h2, width=500, justify='center'
            )
            self.titletext.grid(
                row=5, column=300, columnspan=205, pady=60, padx=20
            )
            self.text.grid(row=10, column=300, columnspan=205, pady=60, padx=20)

    def goto(self, page):
        self.currentindex = page - 1
        self.next()


class HelpPatternTab(Frame):
    def __init__(self):
        super().__init__(Toplevel())
        self.pack(padx=20, pady=20)


class ImageLabel(Label):
    """a label used to display tutorial gifs"""
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.delay = 100
        self.loc = 0
        self.frames = []

    def load(self, im, size):
        im = Image.open(im)
        try:
            for i in count(1):
                self.frames.append(
                    ImageTk.PhotoImage(im.copy())
                )
                im.seek(i)
        except EOFError:
            pass

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.next_frame()

    def unload(self):
        self.config(image=None)
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.loc += 1
            self.loc %= len(self.frames)
            self.config(image=self.frames[self.loc])
            self.after(self.delay, self.next_frame)


def resize_img(img, basewidth=None):
    if basewidth is None:
        basewidth = 400
    wpercent = (basewidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img = img.resize((basewidth, hsize), Image.ANTIALIAS)
    return img