"""
File: Tab.py
Author: Ryan McKay
Date: April 13, 2020

Purpose: This is the base class for the pattern and colorscheme tabs for the
    SpiroGen interface
Input: master window
Output:
    None
"""
from tkinter import Frame
from tkinter.font import Font


class Tab(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.h1 = Font(family='TkDefaultFont', size=20, weight='bold')  # Big heading font
        self.h2 = Font(family='TkDefaultFont', size=15, weight='bold')  # Smaller heading font
        self.pack(padx=50, pady=50)
        self._columns = 800
        self._rows = 800
        self.bind("<Configure>", self.config)

        self._spacedarea = Frame(self)
        self._progparams = {}

    def config(self, event):
        """
        This method is bound to window resize, and it keeps the ranges at full
            length of the window.
        Args:
            event: window resize event

        Returns:
            None
        """
        w, h = event.width, event.height
        for i in range(self._rows):
            self.grid_rowconfigure(i, minsize=h/8000, weight=1)
        for i in range(self._columns):
            self.grid_columnconfigure(i, minsize=w/8000, weight=1)
