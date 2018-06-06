#!/usr/bin/python
from Tkinter import *
import ttk
import numpy as np

density = { "water" :   1.0,
            "gold"  :   19.3,
            "silver":   10.4,
            "vacuum":   0.00,
            "glass" :   2.60,
            "wood"  :   0.67,
            "ice"   :   0.917,
            "oil"   :   0.85,
            "ethanol":  0.79,
            "pmma"  :   1.18}

class Application:

    def __init__(self, main):
        self.rows = 20
        self.columns = 2
        main.rowconfigure(self.rows, weight=1)
        main.columnconfigure(self.columns, weight=1)

        nb = Canvas(main, highlightthickness=0)
        nb.grid(row=1, column=0, columnspan=20, rowspan=20, sticky='NESW')

        self.geometry = StringVar()
        self.geometry.set("sphere")
        self.sphere_radius = StringVar()
        self.sphere_radius.set(str(1.0))
        self.sphere_volume = StringVar()
        self.sphere_volume.set(str(float(self.sphere_radius.get())**3 * np.pi * 4/3.0))

        vcmd = main.register(self.validate)

        self.geometrylf = LabelFrame(nb, text='Geometry')
        self.geometrylf.grid(row=0, column=0, rowspan=2, sticky=NSEW)

        sphere_rb = Radiobutton(self.geometrylf, text="Sphere", variable=self.geometry, value="sphere")
        sphere_rb.grid(row=1, column=0, sticky=NSEW)

        coreshell_rb = Radiobutton(self.geometrylf, text="Core-Shell", variable=self.geometry, value="coreshell")
        coreshell_rb.grid(row=2, column=0, sticky=NSEW)
        coreshell_rb.configure(state = DISABLED)

        cylinder_rb = Radiobutton(self.geometrylf, text="Cylinder", variable=self.geometry, value="cylinder")
        cylinder_rb.grid(row=3, column=0, sticky=NSEW)
        cylinder_rb.configure(state = DISABLED)

        self.parameterslf = LabelFrame(nb, text="Parameters")
        self.parameterslf.grid(row=2, column=0, columnspan=2, sticky=NSEW)

        Label(self.parameterslf, text="radius r = ").grid(row=5, column=0, sticky=NW)

        self.sphere_radius_entry = Entry(self.parameterslf, width=8, justify='right', validate='all', validatecommand=(vcmd, '%P'), textvariable=self.sphere_radius)
        self.sphere_radius_entry.grid(row=5, column=1, sticky=NSEW)
        Label(self.parameterslf, text="m").grid(row=5, column=2, sticky=NSEW)

        Label(self.parameterslf, text="Volume V = ").grid(row=6, column=0, sticky=NW)
        Label(self.parameterslf, textvariable=self.sphere_volume).grid(row=6, column=1, sticky=NSEW)
        Label(self.parameterslf, text="m").grid(row=6, column=2, sticky=NSEW)

        self.materialslf = LabelFrame(nb, text="Particle Material")
        self.materialslf.grid(row=0, column=1, sticky=NSEW)

        self.particlematerial = {"silver", "gold", "vacuum", "glass", "wood", "pmma", "ice"}
        self.pm_selected = StringVar()
        self.pm_selected.set("silver")
        self.pm_selector = OptionMenu(self.materialslf, self.pm_selected, *self.particlematerial)
        self.pm_selector.grid(row=0, column=1, sticky=NSEW)

        self.materialslf = LabelFrame(nb, text="Surrounding Medium")
        self.materialslf.grid(row=1, column=1, sticky=NSEW)

        self.surroundingmedium = {"vacuum", "water", "oil", "ethanol"}
        self.sm_selected = StringVar()
        self.sm_selected.set("water")
        self.sm_selector = OptionMenu(self.materialslf, self.sm_selected, *self.surroundingmedium)
        self.sm_selector.grid(row=3, column=1, sticky=NSEW)

        self.buoyancy_force = StringVar()
        self.calc_force(self.sphere_volume, self.pm_selected, self.sm_selected)

        self.updatebutton = Button(nb, text="Update", command=self.update)
        self.updatebutton.grid(row=4, column=0, sticky=NSEW)

        self.solutionlf = LabelFrame(nb, text='Buoyancy')
        self.solutionlf.grid(row=4, column=1, sticky=NSEW)

        Label(self.solutionlf, textvariable=self.buoyancy_force).grid(row=6, column=1, sticky=NSEW)
        Label(self.solutionlf, text="N").grid(row=6, column=2, sticky=NSEW)

    def validate(self, inp):
        try:
            float(inp)
            return True
        except ValueError:
            return False

    def calc_volume(self, radius):
        r = float(radius.get())
        self.sphere_volume.set(str(r**3 * np.pi * (4/3.0)))
        return self.sphere_volume

    def calc_force(self, volume, material, medium):
        V = float(volume.get())
        rho_particle = float(density[material.get()])
        rho_medium = float(density[medium.get()])
        F = (rho_medium - rho_particle) * V * 9.81
        self.buoyancy_force.set(str(F))
        return self.buoyancy_force

    def update(self):
        self.calc_volume(self.sphere_radius)
        self.calc_force(self.sphere_volume, self.pm_selected, self.sm_selected)
        return True

if __name__ == '__main__':
    main = Tk()
    main.title("Buoyancy Calculator")
    main.geometry("260x230")


    app = Application(main)
    main.attributes("-topmost", True)
    main.mainloop()
