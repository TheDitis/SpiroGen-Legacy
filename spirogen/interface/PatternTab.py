"""
File: PatternTab.py
Author: Ryan McKay
Date: April 13, 2020

Purpose: This a tkinter based tab for the spirogen interface that controls the
    shapes of the pattern
Input: master Notebook
Output:
    save method outputs a dictionary to be saved as json
"""
from tkinter import StringVar, BooleanVar, IntVar, OptionMenu, Label, Entry, \
    Scale, Radiobutton, Widget
from spirogen.interface.Tab import Tab
from spirogen.interface.Parameter import Parameter
from spirogen import spirogen as spiro
from spirogen.spirogen import LVL2, RadialAngularPattern, DrawPath


class PatternTab(Tab):
    def __init__(self, master):
        self._parameters = {}

        super().__init__(master)
        self.name = None
        # Setting dropdown menu for selecting pattern type
        patterns = ['layeredflowers', 'radialangular', 'sinespiral', 'spirals',
                    'iterativerotation']
        self._patternselection = StringVar(self)
        self._patternselection.trace('w', self._setpattern)
        self._patternselection.set(patterns[0])
        self._patternmenu = OptionMenu(self, self._patternselection, *patterns)
        dropdownlabel = Label(self, text="Select a Pattern")
        dropdownlabel.grid(row=0, column=400, pady=(20, 0))
        self._patternmenu.grid(row=1, column=400)
        self._n_angles = None

    def _setpattern(self, *args):
        self.clear()  # clear tab of parameters from any previous pattern

        # get selected pattern type and run the setup method for that type
        patterntype = self._patternselection.get()
        if patterntype == 'layeredflowers':
            self._set_layered_flowers()
        elif patterntype == 'radialangular':
            self._set_radial_angular()
        elif patterntype == 'sinespiral':
            self.set_sin_spiral()
        elif patterntype == 'spirals':
            self.set_spirals()
        elif patterntype == 'iterativerotation':
            self.set_iterative_rotation()

    @property
    def angleparam(self):
        val1 = self._parameters['rotate'].get()
        val2 = self._parameters['rotationfactor'].get()
        return val1 * val2

    def _set_layered_flowers(self):
        # create, set, and grid each parameter:
        layers = Parameter(self, label="layers", from_=10, to=200, row=3)
        layers.set(100)
        angle1 = Parameter(self, label="rotation angle", from_=-18.0, to=18.0,
                           resolution=0.1, bigincrement=0.1, row=5)
        angle2 = Parameter(
            self, label="Rotation Multiplier", from_=0, to=10, resolution=0.1,
            row=10
        )
        angle2.set(1)
        npetals = Parameter(self, label="petals", from_=1.0, to=80,
                            resolution=1, tickinterval=9, row=15)
        npetals.set(2)
        innerdepth = Parameter(self, label="Petal Depth", from_=0, to=6,
                               resolution=0.1, bigincrement=0.1, row=20)
        innerdepth.set(1)
        size = Parameter(
            self, label="size", from_=1, to=10, row=25, resolution=0.1
        )
        pensize = Parameter(self, label="pen size", from_=1, to=40, row=30)

        # add all parameters to the patterntab's master list.
        self._parameters = {
            'layers': layers, "npetals": npetals, "innerdepth": innerdepth,
            "rotate": angle1, "rotationfactor": angle2, "sizefactor": size,
            "pensize": pensize
        }

    def _set_radial_angular(self):
        # creating, adding, & setting parameters:
        size = Parameter(self, label="Size", from_=10, to=1000, row=3)
        size.set(500)
        pensize = Parameter(self, label="Pen Size", from_=1, to=40, row=10)

        self._n_angles = IntVar(self)  # variable for the angle number menu

        self._spacedarea.grid(row=6, column=0, columnspan=800)  # adding the frame from the superclass that allows for even spacing

        self._parameters = {"size": size, 'pensize': pensize}  # for the parameters that feed into the pattern function
        self._progparams = {'n_angles': self._n_angles}  # for the parameters that help create function parameters, but dont feed in directly

        options = [1, 2, 3, 4]  # number of possible angles
        self._n_angles.trace('w', self._make_angle_boxes)  # Making sure that _make_angle_boxes runs every time this control is moved
        self._n_angles.set(options[0])  # setting the default number of angles to 1

        # making, labeling, and adding dropdown menu
        self.n_angles_menu = OptionMenu(self, self._n_angles, *options)
        dropdownlabel = Label(self, text="Number of Angles:")
        dropdownlabel.grid(row=4, column=400, pady=(10, 0))
        self.n_angles_menu.grid(row=5, column=400)

        self._progparams['n_angles'] = self._n_angles
        self._progparams['n_angles_menu'] = self.n_angles_menu
        self._progparams['n_angle_label'] = dropdownlabel

    def _make_angle_boxes(self, *args):
        menu = self._progparams['n_angles']
        n = menu.get()  # this is the value chosen for number of angles
        prevparams = []  # making an empty array for previous options, so you don't lose your settings on re-render
        if 'angleparams' in self._progparams.keys():  # if there are user entered angle settings
            for box in self._progparams['angleparams']:  # for angle box in previous settings
                entry = []  # create entry tosave those settings to
                for i, widget in enumerate(box):  # for each widget in previous settings
                    if i == 0 or i == 2:  # these are the indicies for the angle and curve amount variables
                        entry.append(widget.get())  # add the values to the entry
                    widget.grid_forget()  # remove the old box from the frame
                prevparams.append(entry)  # add the entry to the list of previous parameters

        # doing some cleanup from the last run of this method
        self._progparams['angleparams'] = []
        if 'turncycle' in self._parameters.keys():
            self._parameters['turncycle'].grid_forget()
        if 'jank' in self._parameters.keys():
            self._parameters['jank'].grid_forget()
        self._progparams['anglevariables'] = []

        for i in range(n):  # n is the number of angles we are setting
            anglevar = StringVar()
            anglevar.trace('w', self.set_angles)
            anglebox = Entry(self._spacedarea, width=5, textvariable=anglevar)
            label1 = Label(self._spacedarea, text=f"angle {str(i + 1)}")

            curvevar = StringVar()
            curvevar.trace('w', self.set_angles)
            curvebox = Entry(self._spacedarea, width=5, textvariable=curvevar)
            label2 = Label(self._spacedarea, text=f"curve {str(i + 1)}")
            if len(prevparams) > i:
                anglevar.set(prevparams[i][0])
                curvevar.set(prevparams[i][1])
            else:
                if i == 0:
                    anglevar.set(125)
                    curvevar.set(5)
                else:
                    anglevar.set(0)
                    curvevar.set(0)
            if i == 1:
                turncycle = Scale(self._spacedarea, orient='horizontal',
                                  from_=0, to=5, label='turn cycle')
                turncycle.grid(row=9, column=100, rowspan=3)
                jank = Scale(self._spacedarea, orient='horizontal', from_=0,
                             to=600, label="jank")
                jank.grid(row=12, column=100, rowspan=3)
                self._parameters['turncycle'] = turncycle
                self._parameters['jank'] = jank
            col = 20 * (i + 1)  # just so that I have flexibility in positioning things later if I make changes
            label1.grid(row=9, column=col, pady=10)
            anglebox.grid(row=10, column=col, padx=20)
            label2.grid(row=12, column=col, padx=20)
            curvebox.grid(row=14, column=col)
            self._progparams['angleparams'].append(
                [anglebox, label1, curvebox, label2]
            )
            self._progparams['anglevariables'].append(
                [anglevar, curvevar]
            )
            self.set_angles()

    def set_angles(self, *args):
        angleparams = self._progparams['anglevariables']
        # angles = [[i[0].get(), i[2].get()] for i in angleparams]
        angles = [[i[0].get(), i[1].get()] for i in angleparams]

        for i in range(len(angles)):
            angle = angles[i]
            for j in range(len(angle)):
                val = angle[j]
                try:
                    angles[i][j] = float(val)
                except ValueError:
                    angles[i][j] = len(val)
                    # print("angle values should be numerical. Using length of "
                    #       "input as angle")
        self._parameters['angles'] = [i for i in angles if i[0] != 0]

    def set_sin_spiral(self):
        pady = 3  # the y spacing needed for this particular pattern type

        n_strands = Parameter(
            self, label="Number of Waves", from_=1, to=300, row=10, pady=pady
        )
        length = Parameter(
            self, label="Length", from_=0, to=50, row=12, pady=pady
        )
        x_shift = Parameter(
            self, label="Shift X", from_=0, to=50, row=14, pady=pady,
            resolution=0.1, bigincrement=0.1
        )
        y_shift = Parameter(
            self, label="Shift Y", from_=0, to=50, row=18, pady=pady,
            resolution=0.1, bigincrement=0.1
        )
        rotation = Parameter(
            self, label="Rotation", from_=-18.0, to=18.0, row=22, pady=pady
        )
        rotaterate = Parameter(
            self, label="Rotation Multiplier", from_=0, to=10, row=26,
            resolution=0.1, bigincrement=0.1, pady=pady
        )
        wavelen = Parameter(
            self, label="Wavelength", from_=0, to=500, row=30, pady=pady
        )
        wl_shift = Parameter(
            self, label="Wavelength Shift", from_=0, to=10, row=34, pady=pady,
            resolution=0.1, bigincrement=0.1
        )
        amp = Parameter(
            self, label="Ampitude", from_=0, to=500, row=38, pady=pady
        )
        amp_shift = Parameter(
            self, label="Amplitude Shift", from_=0, to=20, row=42, pady=pady,
            resolution=0.1, bigincrement=0.1
        )
        pensize = Parameter(
            self, label="Pen Size", from_=1, to=40, row=46, pady=pady
        )
        cosine = BooleanVar()
        sinebtn = Radiobutton(
            self, text='Sine', width=5, indicatoron=False, value=False,
            variable=cosine
        )
        cosinebtn = Radiobutton(
            self, text='Cosine', width=5, indicatoron=False, value=True,
            variable=cosine
        )

        sinebtn.grid(row=50, column=50, columnspan=100, pady=20)
        cosinebtn.grid(row=50, column=180, columnspan=100)

        n_strands.set(100)
        length.set(30)
        x_shift.set(1)
        rotaterate.set(1)
        wavelen.set(50)
        amp.set(100)

        self._progparams['cosinebuttons'] = [sinebtn, cosinebtn]

        self._parameters = {
            'strands': n_strands, 'xshift': x_shift, 'yshift': y_shift,
            "rotate": rotation, 'rotaterate': rotaterate, 'wavelength': wavelen,
            'amplitude': amp, 'wlshift': wl_shift, 'ampshift': amp_shift,
            'length': length, 'pensize': pensize,'cosine': cosine
        }

    def set_spirals(self):
        reps = Parameter(
            self, label="Number of Spirals", from_=1, to=600, row=10
        )
        rotation = Parameter(
            self, label="Rotation", from_=-180, to=180, row=20, resolution=0.1,
            bigincrement=0.1
        )
        curve = Parameter(self, label="Scale", from_=1, to=50, row=22)
        diameter = Parameter(self, label="Curve Length", from_=1, to=30, row=25)
        scale = Parameter(
            self, label="Spiral Tightness (Size)", from_=5, to=50, row=27
        )
        poly = Parameter(self, label="Poly", from_=2, to=400, row=30)
        centerdist = Parameter(
            self, label="Distance from Center", from_=0, to=50, row=32
        )
        pensize = Parameter(
            self, label="Pen Size", from_=1, to=60, row=36
        )

        reps.set(60)
        rotation.set(5)
        curve.set(10)
        diameter.set(10)
        scale.set(20)
        poly.set(400)
        centerdist.set(0)

        self._parameters = {
            'reps': reps, 'rotation': rotation, 'curve': curve,
            'diameter': diameter, 'scale': scale, 'poly': poly,
            'centerdist': centerdist, 'pensize': pensize
        }

    def set_iterative_rotation(self):
        pady = 0
        shapeoptions = ['Wave', 'Rectangle', 'Circle']
        shape = StringVar()
        shapemenulabel = Label(self, text="Shape")
        shapemenu = OptionMenu(self, shape, *shapeoptions)
        shapemenulabel.grid(column=10, row=23, columnspan=200)
        shapemenu.grid(column=10, row=25, columnspan=200)
        branches = Parameter(
            self, label="Number of Branches", from_=2, to=60, pady=pady, row=27
        )
        repetitions = Parameter(
            self, label='Repetitions', from_=4, to=80, pady=pady, row=30
        )
        shiftx = Parameter(
            self, label='Shift X', from_=-10, to=10, resolution=0.1, pady=pady,
            row=35
        )
        shifty = Parameter(
            self, label='Shift Y', from_=-10, to=10, resolution=0.1, pady=pady,
            row=40
        )
        rotation = Parameter(
            self, label='Rotation', from_=-30, to=30, resolution=0.1, pady=pady,
            row=42
        )
        stretch = Parameter(
            self, label='Stretch (Wave Only)', from_=0, to=80, pady=pady, row=45
        )
        length = Parameter(
            self, label='Length/Width', from_=1, to=150, pady=pady, row=50
        )
        depth = Parameter(
            self, label='Amplitude/Height', from_=0, to=150, pady=pady, row=55
        )
        stretchshift = Parameter(
            self, label="Stretch Shift (Wave Only)", from_=-3, to=3, pady=pady,
            row=60, resolution=0.1
        )
        lenshift = Parameter(
            self, label="Length/Width Shift", from_=-3, to=3, pady=pady, row=65,
            resolution=0.1
        )
        depthshift = Parameter(
            self, label="Amplitude/Height Shift", from_=-3, to=3, pady=pady,
            row=70, resolution=0.1
        )
        distshift = Parameter(
            self, label="Distance Shift", from_=0, to=0.5, pady=pady, row=75,
            resolution=0.01
        )
        cosine = BooleanVar()
        sinebtn = Radiobutton(
            self, text='Sine', width=5, indicatoron=False, value=False,
            variable=cosine
        )
        cosinebtn = Radiobutton(
            self, text='Cosine', width=5, indicatoron=False, value=True,
            variable=cosine
        )
        sinebtn.grid(row=80, column=50, columnspan=100, pady=20)
        cosinebtn.grid(row=80, column=180, columnspan=100)

        shape.set('Rectangle')
        repetitions.set(30)
        rotation.set(2)
        stretch.set(20)
        length.set(30)
        depth.set(30)
        branches.set(8)

        self._progparams['shapemenu'] = shapemenu
        self._progparams['shapemenulabel'] = shapemenulabel
        self._progparams['cosinebuttons'] = [cosinebtn, sinebtn]

        self._parameters = {
            "function": shape, "reps": repetitions, "xshift": shiftx,
            "yshift": shifty, 'stretch': stretch, "length": length,
            "depth": depth, "stretchshift": stretchshift, "lenshift": lenshift,
            "depthshift": depthshift, "cosine": cosine, "distshift": distshift,
            "individualrotation": rotation, "branches": branches
        }

    def clear(self):
        """
        This method is used to remove all Widgets from the frame when
        switching pattern types
        """
        for p in self._parameters.values():
            if isinstance(p, Widget):
                p.grid_forget()
        self._spacedarea.grid_forget()
        for item in self._progparams.values():
            if isinstance(item, Widget):
                item.grid_forget()
            elif isinstance(item, list):
                for i in item:
                    if isinstance(i, Widget):
                        i.grid_forget()
                    else:
                        for j in i:
                            if isinstance(j, (Widget, Parameter)):
                                j.grid_forget()

    def save(self):
        params = {}
        # converting all widget parameters to their values for save:
        for k, v in self._parameters.items():
            if isinstance(v, (Widget, BooleanVar, IntVar, StringVar)):
                params[k] = v.get()
            else:
                params[k] = v
        # Create new object with all necessary values for save:
        output = {
            'patterntype': self._patternselection.get(),
            'parameters': params
        }
        return self.name, output

    def load(self, name, data):
        """
        Sets parameters to the values in the data retrieved
        Args:
            data: a Dictionary with patterntype, parameters, and progparams if
            the retrieved pattern is of radialangular type

        Returns:
            None
        """
        # Set patternselection to retrieved value, which is bound to the _setpattern method:
        self._patternselection.set(data['patterntype'])
        params = data['parameters']
        # Set the angle boxes if it's a radialangular pattern type
        if data['patterntype'] == 'radialangular':
            angles = data['parameters']['angles']  # get list of angles
            self._n_angles.set(len(params['angles']))  # set number of angle boxes to number of angles in list
            angleparams = self._progparams['anglevariables']  # retrieves the variables for the angle boxes
            for i in range(len(angleparams)):  # for each index in angleparams
                boxes = angleparams[i]  # get the 2 boxes (angle, curve) for each angle
                anglebox, curvebox = boxes[0], boxes[1]  # separate them from eachother
                anglebox.set(angles[i][0])  # set the angle to the retrieved value
                curvebox.set(angles[i][1])  # set the curve to the retrieeved value
        for k in params:  # for each key in the parameter dictionary:
            if k in self._parameters:  # if that parameter already exists in the master parameter dictionary:
                if not isinstance(self._parameters[k], (list, bool)):
                    self._parameters[k].set(params[k])  # set that parameter to the retrieved value for that param
            else:  # if that parameter isn't already in the list:
                self._parameters[k] = params[k]  # add it
        self.name = name

    def run(self, colorscheme):
        """
        This method is called from the the master Application.

        Args:
            colorscheme: a SpiroGen ColorScheme object

        Returns:
            None. Draws pattern
        """
        parameters = {}
        # convert parameter widgets/variables to their values
        for param in self._parameters.items():
            label, value = param[0], param[1]
            if not isinstance(value, (int, float, str, list, tuple)):
                parameters[label] = value.get()
            else:
                parameters[label] = value

        # This is where the patterns are actually drawn based on selection:
        if self._patternselection.get() == "layeredflowers":
            parameters['rotate'] = self.angleparam
            parameters.pop('rotationfactor')
            LVL2.layered_flowers(**parameters, colors=colorscheme)
        elif self._patternselection.get() == "radialangular":
            self.set_angles()
            RadialAngularPattern(**parameters, colors=colorscheme).drawpath()
        elif self._patternselection.get() == 'sinespiral':
            pensize = parameters.pop('pensize')
            DrawPath(
                LVL2.sin_spiral(**parameters),
                colors=colorscheme,
                pensize=pensize,
            )
        elif self._patternselection.get() == 'spirals':
            LVL2.spiral_spiral(**parameters, colors=colorscheme)
        elif self._patternselection.get() == 'iterativerotation':
            LVL2.random_iterative_rotation(
                **parameters, colors=colorscheme, rotationcenter=(0, 0)
            )
        #     LVL2.iterative_rotation(**parameters, colors=colorscheme)

        spiro.wait()  # This keeps the pattern window from closing as soon as it's done drawing
