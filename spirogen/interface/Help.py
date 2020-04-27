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
    It simply displays images and text, page by page.
    """
    def __init__(self):
        super().__init__(Toplevel())
        self.master.title('Tutorial')
        self.pack(padx=20, pady=20)
        self._imagepath = './spirogen/interface/settings/tutorial/images/'
        self.assetpath = ''

        p = './spirogen/interface/settings/tutorial/tutorial_pages.json'
        with open(p, 'r') as file:
            self.tutdata = json.load(file)
        self.h1 = Font(family='TkDefaultFont', size=40, weight='bold')  # Big heading font
        self.h2 = Font(family='TkDefaultFont', size=20, weight='bold')
        self._currentindex = -1
        self._image = None
        self._titletext = None
        self._text = None
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
        return self._imagepath + self.tutdata[self._currentindex]['image']

    @property
    def indexinrange(self):
        return 0 <= self._currentindex < len(self.tutdata)

    def next(self):
        # goes to the next page
        self._currentindex += 1
        if self.indexinrange:
            self.load_page()
        else:
            self.master.destroy()

    def back(self):
        # goes to the previous page
        if not self._currentindex == 0:
            self._currentindex -= 1
            self.load_page()

    def load_page(self):
        image = Image.open(self.path)
        # get the text and image data from the current page:
        currentpage = self.tutdata[self._currentindex]
        # image = resize_img(image)
        photo = ImageTk.PhotoImage(image)
        # cleanup the last page shown:
        if self._image:
            self._image.grid_forget()
        if self._text:
            self._text.grid_forget()
        if self._titletext:
            self._titletext.grid_forget()

        # if the image is a gif:
        if '.gif' in self.path:
            self._image = GifPlayer(self, borderwidth=2, relief="solid")
            # self.image.image = photo  # keep a reference!
            self._image.grid(row=0, column=0, columnspan=205, rowspan=205)
            self._image.load(self.path)
        # if it's just a still image:
        else:
            self._image = Label(self, image=photo, borderwidth=2, relief="solid")
            self._image.image = photo  # keep a reference!
            self._image.grid(row=0, column=0, columnspan=205, rowspan=205)
        # grab the text:
        title = currentpage['title']
        text = currentpage['text']
        self._titletext = Message(
            self, text=title, font=self.h1, width=500, justify='center'
        )
        self._text = Message(
            self, text=text, font=self.h2, width=500, justify='center'
        )
        # if this is the first or last page, we want the text below the image:
        if "Welcome" in self.path:

            self._titletext.grid(row=210, column=0, columnspan=205, pady=20)
            self._text.grid(row=215, column=0, columnspan=205, pady=20)
        # otherwise, we want it to the side:
        else:
            self._titletext.grid(
                row=5, column=300, columnspan=205, pady=60, padx=20
            )
            self._text.grid(row=10, column=300, columnspan=205, pady=60, padx=20)

    def goto(self, page):
        self._currentindex = page - 1
        self.next()


class GifPlayer(Label):
    """a label used to display tutorial gifs"""
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self._delay = 100
        self._loc = 0
        self._frames = []

    def load(self, im):
        im = Image.open(im)
        try:
            for i in count(1):
                self._frames.append(
                    ImageTk.PhotoImage(im.copy())
                )
                im.seek(i)
        except EOFError:
            pass

        try:
            self._delay = im.info['duration']
        except:
            self._delay = 100

        if len(self._frames) == 1:
            self.config(image=self._frames[0])
        else:
            self.next_frame()

    def unload(self):
        self.config(image=None)
        self._frames = None

    def next_frame(self):
        if self._frames:
            self._loc += 1
            self._loc %= len(self._frames)
            self.config(image=self._frames[self._loc])
            self.after(self._delay, self.next_frame)
