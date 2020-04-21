from tkinter import StringVar, BooleanVar, IntVar, OptionMenu, Label, Entry, Scale, Radiobutton, Widget
from Tab import Tab
from Parameter import Parameter
import spirogen as spiro
from spirogen import LVL2, RadialAngularPattern, DrawPath


class PatternTab(Tab):
    def __init__(self, master):
        self.parameters = {}

        super().__init__(master)
        # Setting dropdown menu for selecting pattern type
        patterns = ['layeredflowers', 'radialangular', 'sinespiral', 'spirals']
        self._patternselection = StringVar(self)
        self._patternselection.trace('w', self._setpattern)
        self._patternselection.set(patterns[0])  # TODO: Set Startup pattern type here
        self._patternmenu = OptionMenu(self, self._patternselection, *patterns)
        dropdownlabel = Label(self, text="Select a Pattern")
        dropdownlabel.grid(row=0, column=400, pady=(20, 0))
        self._patternmenu.grid(row=1, column=400)
        self._n_angles = None

    def _setpattern(self, *args):
        # self.runbutton['command'] = func
        patterntype = self._patternselection.get()
        if patterntype == 'layeredflowers':
            self._set_layered_flowers()
        elif patterntype == 'radialangular':
            self._set_radial_angular()
        elif patterntype == 'sinespiral':
            self.set_sin_spiral()
        elif patterntype == 'spirals':
            self.set_spirals()

    def _set_layered_flowers(self):
        # self.patterntype = "layeredflowers"
        self.clear()
        layers = Parameter(self, label="layers", from_=10, to=200, row=3)
        layers.set(100)
        angle1 = Parameter(self, label="rotation angle", from_=-20.0, to=20.0, resolution=0.1, bigincrement=0.1, row=4)
        npetals = Parameter(self, label="petals", from_=1.0, to=80, resolution=1, tickinterval=9, row=5)
        npetals.set(2)
        innerdepth = Parameter(self, label="Petal Depth", from_=0, to=6, resolution=0.1, bigincrement=0.1, row=6)
        innerdepth.set(1)
        size = Parameter(self, label="size", from_=1, to=10, row=7)
        pensize = Parameter(self, label="pen size", from_=1, to=40, row=8)

        self.parameters = {'layers': layers, "npetals": npetals, "innerdepth": innerdepth, "rotate": angle1, "sizefactor": size, "pensize": pensize}

    def _set_radial_angular(self):
        self.clear()

        size = Parameter(self, label="Size", from_=10, to=1000, row=3)
        size.set(500)

        self._n_angles = IntVar(self)

        self.spacedarea.grid(row=6, column=0, columnspan=800)

        pensize =  Parameter(self, label="Pen Size", from_=1, to=40, row=10)
        # self.anglearea.grid_columnconfigure(weight=1)

        self.parameters = {"size": size, 'pensize': pensize}  # for the parameters that feed into the pattern function
        self.progparams = {'n_angles': self._n_angles}  # for the parameters that help create function parameters, but dont feed in directly

        options = [1, 2, 3, 4]  # number of possible angles
        self._n_angles.trace('w', self._make_angle_boxes)
        self._n_angles.set(options[0])

        self.n_angles_menu = OptionMenu(self, self._n_angles, *options)
        dropdownlabel = Label(self, text="Number of Angles:")
        dropdownlabel.grid(row=4, column=400, pady=(10, 0))
        self.n_angles_menu.grid(row=5, column=400)

        self.progparams['n_angles'] = self._n_angles
        self.progparams['n_angles_menu'] = self.n_angles_menu
        self.progparams['n_angle_label'] = dropdownlabel

    def _make_angle_boxes(self, *args):
        menu = self.progparams['n_angles']
        n = menu.get()
        prevparams = []
        # TODO: add turncycle and jank to prevparams
        if 'angleparams' in self.progparams.keys():
            for box in self.progparams['angleparams']:
                entry = []
                for i, widget in enumerate(box):
                    if i == 0 or i == 2:
                        entry.append(widget.get())
                    widget.grid_forget()
                prevparams.append(entry)

        self.progparams['angleparams'] = []
        if 'turncycle' in self.parameters.keys():
            self.parameters['turncycle'].grid_forget()
        if 'jank' in self.parameters.keys():
            self.parameters['jank'].grid_forget()
        self.progparams['anglevariables'] = []

        for i in range(n):
            anglevar = StringVar()
            # anglevar.trace('w', self.set_angles)
            anglebox = Entry(self.spacedarea, width=5, textvariable=anglevar)
            label1 = Label(self.spacedarea, text=f"angle {str(i + 1)}")

            curvevar = StringVar()
            # curvevar.trace('w', self.set_angles)
            curvebox = Entry(self.spacedarea, width=5, textvariable=curvevar)
            label2 = Label(self.spacedarea, text=f"curve {str(i + 1)}")
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
                turncycle = Scale(self.spacedarea, orient='horizontal', from_=0, to=5, label='turn cycle')
                turncycle.grid(row=9, column=100, rowspan=3)
                jank = Scale(self.spacedarea, orient='horizontal', from_=0, to=600, label="jank")
                jank.grid(row=12, column=100, rowspan=3)
                self.parameters['turncycle'] = turncycle
                self.parameters['jank'] = jank

            col = 20 * (i + 1)  # just so that I have flexibility in positioning things later if I make changes
            label1.grid(row=9, column=col, pady=10)
            anglebox.grid(row=10, column=col, padx=20)
            label2.grid(row=12, column=col, padx=20)
            curvebox.grid(row=14, column=col)
            self.progparams['angleparams'].append(
                [anglebox, label1, curvebox, label2]
            )
            self.progparams['anglevariables'].append(
                [anglevar, curvevar]
            )
            # self.progparams['curveboxes'].append([curvebox, label2])

    def set_angles(self, *args):
        angleparams = self.progparams['angleparams']
        angles = [[i[0].get(), i[2].get()] for i in angleparams]

        for i in range(len(angles)):
            angle = angles[i]
            for j in range(len(angle)):
                val = angle[j]
                try:
                    angles[i][j] = float(val)
                except ValueError:
                    angles[i][j] = len(val)
                    print("angle values should be numerical. Using length of input as angle")
        self.parameters['angles'] = [i for i in angles if i[0] != 0]

    def set_sin_spiral(self):
        self.clear()

        pady = 3

        n_strands = Parameter(self, label="Number of Waves", from_=1, to=300, row=10, pady=pady)
        length = Parameter(self, label="Length", from_=0, to=50, row=12, pady=pady)
        x_shift = Parameter(self, label="Shift X", from_=0, to=50, row=14, pady=pady)
        y_shift = Parameter(self, label="Shift Y", from_=0, to=50, row=18, pady=pady)
        rotation = Parameter(self, label="Rotation", from_=-18.0, to=18.0, row=22, pady=pady)
        rotaterate = Parameter(self, label="Rotation Multiplier", from_=0, to=10, row=26, resolution=0.1, bigincrement=0.1, pady=pady)
        wavelen = Parameter(self, label="Wavelength", from_=0, to=500, row=30, pady=pady)
        wl_shift = Parameter(self, label="Wavelength Shift", from_=0, to=10, row=34, pady=pady)
        amp = Parameter(self, label="Ampitude", from_=0, to=500, row=38, pady=pady)
        amp_shift = Parameter(self, label="Amplitude Shift", from_=0, to=20, row=42, pady=pady)
        pensize = Parameter(self, label="Pen Size", from_=1, to=40, row=46, pady=pady)
        cosine = BooleanVar()
        sinebtn = Radiobutton(self, text='Sine', width=5, indicatoron=False, value=False, variable=cosine)
        cosinebtn = Radiobutton(self, text='Cosine', width=5, indicatoron=False, value=True, variable=cosine)

        sinebtn.grid(row=50, column=50, columnspan=100, pady=20)
        cosinebtn.grid(row=50, column=180, columnspan=100)

        n_strands.set(100)
        length.set(30)
        x_shift.set(1)
        rotaterate.set(1)
        wavelen.set(50)
        amp.set(100)

        self.progparams['cosinebuttons'] = [sinebtn, cosinebtn]

        self.parameters = {'strands': n_strands, 'xshift': x_shift,
                           'yshift': y_shift, "rotate": rotation,
                           'rotaterate': rotaterate,
                           'wavelength': wavelen, 'amplitude': amp,
                           'wlshift': wl_shift, 'ampshift':amp_shift,
                           'length': length, 'pensize': pensize,
                           'cosine': cosine}

    def set_spirals(self):
        self.clear()

        reps = Parameter(self, label="Number of Spirals", from_=1, to=600, row=10)
        rotation = Parameter(self, label="Rotation", from_=-180, to=180, row=20, resolution=0.1, bigincrement=0.1)
        curve = Parameter(self, label="Curve Amount", from_=1, to=50, row=22)
        diameter = Parameter(self, label="Diameter", from_=1, to=30, row=25)
        scale = Parameter(self, label="Scale", from_=5, to=50, row=27)
        poly = Parameter(self, label="Poly", from_=2, to=400, row=30)
        centerdist = Parameter(self, label="Distance from Center", from_=0, to=50, row=32)

        reps.set(60)
        rotation.set(5)
        curve.set(10)
        diameter.set(10)
        scale.set(20)
        poly.set(400)
        centerdist.set(0)

        self.parameters = {'reps': reps, 'rotation': rotation,
                           'curve': curve, 'diameter': diameter,
                           'scale': scale, 'poly': poly,
                           'centerdist': centerdist}

    def clear(self):
        for p in self.parameters.values():
            if isinstance(p, Widget):
                p.grid_forget()
        self.spacedarea.grid_forget()
        for item in self.progparams.values():
            if isinstance(item, Widget):
                item.grid_forget()
            elif isinstance(item, list):
                for i in item:
                    if isinstance(i, Widget):
                        i.grid_forget()
                    else:
                        for j in i:
                            j.grid_forget()

    def save(self):
        # print(params)
        # params = {k: v.get() for k, v in self.parameters.items()}
        params = {}
        for k, v in self.parameters.items():
            if isinstance(v, (Widget, BooleanVar, IntVar, StringVar)):
                params[k] = v.get()
            else:
                params[k] = v
        output = {'patterntype': self._patternselection.get(),
                  'parameters': params}
        # if self.patternselection.get() == 'radialangular':
        #     print('progparams:', self.progparams)
        #     output['progparams'] = self.progparams
        #     print('here')
        #     print(output)
        return output

    def load(self, data):
        self._patternselection.set(data['patterntype'])
        params = data['parameters']
        # print(data['patterntype'])
        if data['patterntype'] == 'radialangular':
            # progparams = data['progparams']
            angles = data['parameters']['angles']
            self._n_angles.set(len(params['angles']))
            angleparams = self.progparams['anglevariables']
            for i in range(len(angleparams)):
                boxes = angleparams[i]
                anglebox, curvebox = boxes[0], boxes[1]
                anglebox.set(angles[i][0])
                curvebox.set(angles[i][1])
        for k in params:
            if k in self.parameters:
                self.parameters[k].set(params[k])
            else:
                self.parameters[k] = params[k]

    def run(self, colorscheme):
        # bye()
        # parameters = {k: v.get() for k, v in self.parameters.items() if isinstance(v, Widget)}
        parameters = {}
        for param in self.parameters.items():
            label, value = param[0], param[1]
            if not isinstance(value, (int, float, str, list, tuple)):
                parameters[label] = value.get()
            else:
                parameters[label] = value

        if self._patternselection.get() == "layeredflowers":
            LVL2.layered_flowers(**parameters, colors=colorscheme)
        elif self._patternselection.get() == "radialangular":
            self.set_angles()
            RadialAngularPattern(**parameters, colors=colorscheme).drawpath()
        elif self._patternselection.get() == 'sinespiral':
            pensize = parameters.pop('pensize')
            DrawPath(LVL2.sin_spiral(**parameters), colors=colorscheme, pensize=pensize)
        elif self._patternselection.get() == 'spirals':
            LVL2.spiral_spiral(**parameters, colors=colorscheme)
        spiro.wait()