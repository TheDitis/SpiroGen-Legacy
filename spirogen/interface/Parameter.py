"""
File: Dialogs.py
Author: Ryan McKay
Date: April 13, 2020

Purpose: This is a wrapper around the tkinter Scale widget made to simplify
    creation of them by setting some defaults such as pading and orientation,
    as well as combining instatiation and grid placement into one line.
Input: Takes master widget, desired row location, and optionally, padding, and
    any other arguments that Scale accepts natively
Output: A scale widget is created and placed on the desired window. Values can
    be gotten using the Scale objects native get() method
"""
from tkinter import Scale


class Parameter(Scale):
    def __init__(self, master, row=None, pady=20, width=10000, **kwargs):
        self.rangewidth = width
        if 'activebackground' not in kwargs:
            kwargs['activebackground'] = 'blue'
        super().__init__(
            master, length=self.rangewidth, orient="horizontal", **kwargs
        )  # initializing Scale object
        self.columnspan = 790
        self.row = row
        if 'label' in kwargs:
            self.label = kwargs['label']
        # and adding it to the grid:
        self.grid(column=1, columnspan=self.columnspan, row=self.row, pady=pady)

    def __repr__(self):
        return f"{self.label}: {self.get()}"
