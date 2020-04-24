"""
File: ColorSwatch.py
Author: Ryan McKay
Date: April 24, 2020

Purpose: This class is a subclass of frame, used to preview the color of an rgb
    value set. I created it initially once I added the ColorSwatchDialog used to
    edit values in a more intuitive way. Upon clicking the frame, the dialog is
    opened, and any changes made update the color in real time.
Input: master frame, and the tkinter variable objects for each of the three
    colors tied to the entry boxes that control them, and then any other args
    that Frame takes natively
Output:
    Just displays a color
"""
from tkinter import Frame
from spirogen.interface.Dialogs import ColorSwatchDialog


class ColorSwatch(Frame):
    def __init__(self, master, rvar, gvar, bvar, **kwargs):
        targets = {'r': rvar, 'g': gvar, 'b': bvar}
        if 'color' in kwargs:
            self.color = kwargs.pop('color')
        else:
            self.color = []
            for var in targets.values():
                try:
                    strval = var.get()
                    if strval == '':
                        val = 0
                    else:
                        val = round(float(strval))
                except:
                    print(
                        'color values must be numeric values between 0 and 255.')
                    val = 0
                self.color.append(val)
            self.color = self.rgb_tk(self.color)
        defaults = {'height': 15, 'width': 20}
        for key in defaults:
            if key not in kwargs:
                kwargs[key] = defaults[key]
        super().__init__(master, **kwargs, bg=self.color)

        self.bind("<Button-1>", lambda *x: ColorSwatchDialog(self, targets))

    def updatecolor(self, rgb):
        self.configure(bg=rgb)
        self.color = rgb

    @staticmethod
    def rgb_tk(rgb):
        rgb = tuple([round(float(i)) for i in rgb])
        output = "#%02x%02x%02x" % rgb
        return output
