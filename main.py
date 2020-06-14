import tkinter as tk
import random
import os
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont
from tkinter import Button, Entry


class Limiter(ttk.Scale):
    def __init__(self, *args, **kwargs):
        self.precision = kwargs.pop('precision')
        self.chain = kwargs.pop('command', lambda *a: None)
        super(Limiter, self).__init__(
            *args, command=self._value_changed, **kwargs)

    def _value_changed(self, newvalue):
        newvalue = round(float(newvalue), self.precision)
        self.winfo_toplevel().globalsetvar(self.cget('variable'), (newvalue))
        self.chain(newvalue)


class Main(ttk.Frame):

    def __init__(self, mainframe):
        self.imagePath = 'output-1.png'
        self.whichFrame = 1
        self.flagCU = BooleanVar()
        self.flagPU = BooleanVar()
        self.flagTU = BooleanVar()

        self.cuArray = []
        self.puArray = []
        self.tuArray = []

        self.readFiles()

        ttk.Frame.__init__(self, master=mainframe)

        input_var = tk.IntVar(value=1)
        slide = Limiter(mainframe, variable=input_var, orient='horizontal', length=24,
                        command=self.callback, precision=4)
        slide['to'] = 24
        slide['from'] = 1
        slide.pack(fill=X, padx=10, pady=10)

        checkboxes = ttk.Frame(self.master)
        ttk.Checkbutton(checkboxes, text="CU", variable=self.flagCU, command=self.show_lines).grid(row=0, column=1,
                                                                                                   sticky=W, padx=15)
        ttk.Checkbutton(checkboxes, text="PU", variable=self.flagPU, command=self.show_lines).grid(row=0, column=2,
                                                                                                   sticky=W, padx=15)
        ttk.Checkbutton(checkboxes, text="TU", variable=self.flagTU, command=self.show_lines).grid(row=0, column=3,
                                                                                                   sticky=W, padx=15)
        checkboxes.pack(padx=10, pady=10)

        self.image = Image.open(self.imagePath)

        cFrame = ttk.Frame(self.master, height=600)
        cFrame.pack(expand=1, pady=10, padx=5)

        self.canvas = tk.Canvas(cFrame, highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky='nswe')
        self.canvas.pack()

        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)

        self.canvas.bind('<ButtonPress-1>', self.move_from)
        self.canvas.bind('<B1-Motion>',     self.move_to)
        # Windows and MacOS
        self.canvas.bind('<MouseWheel>', self.wheel)
        # Linux, wheel scroll down
        self.canvas.bind('<Button-5>',   self.wheel)
        # Linux, wheel scroll up
        self.canvas.bind('<Button-4>',   self.wheel)

        self.imscale = 1.0
        self.imageid = None
        self.delta = 0.75
        self.show_image()
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def move_from(self, event):
        self.canvas.scan_mark(event.x, event.y)

    def move_to(self, event):
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def wheel(self, event):
        ''' Zoom with mouse wheel '''
        scale = 1.0
        # Respond to Linux (event.num) or Windows (event.delta) wheel event
        if event.num == 5 or event.delta == -120:
            scale *= self.delta
            self.imscale *= self.delta
        if event.num == 4 or event.delta == 120:
            scale /= self.delta
            self.imscale /= self.delta
        # Rescale all canvas objects
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        self.canvas.scale('all', x, y, scale, scale)
        self.show_image()
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def readFiles(self):
        file1 = open("cus.txt", "r+")
        file2 = open("pus.txt", "r+")
        file3 = open("tus.txt", "r+")
        cus = file1.readlines()
        pus = file2.readlines()
        tus = file3.readlines()

        for cu in cus:
            x = int(cu.split(",")[0].split("x= ")[1])
            y = int(cu.split(",")[1].split("y= ")[1])
            width = int(cu.split(",")[2].split("width= ")[1])
            height = int(cu.split(",")[3].split(
                "height= ")[1].split("\n")[0])
            self.cuArray.append((x, y, width, height))
        for pu in pus:
            x = int(pu.split(",")[0].split("x= ")[1])
            y = int(pu.split(",")[1].split("y= ")[1])
            width = int(pu.split(",")[2].split("width= ")[1])
            height = int(pu.split(",")[3].split(
                "height= ")[1].split("\n")[0])
            self.puArray.append((x, y, width, height))
        for tu in tus:
            x = int(tu.split(",")[0].split("x= ")[1])
            y = int(tu.split(",")[1].split("y= ")[1])
            width = int(tu.split(",")[2].split("width= ")[1])
            height = int(tu.split(",")[3].split(
                "height= ")[1].split("\n")[0])
            self.tuArray.append((x, y, width, height))

    def show_image(self):
        ''' Show image on the Canvas '''
        if self.imageid:
            self.canvas.delete(self.imageid)
            self.imageid = None
            self.canvas.imagetk = None  # delete previous image from the canvas
        width, height = self.image.size
        new_size = int(self.imscale * width), int(self.imscale * height)
        imagetk = ImageTk.PhotoImage(self.image.resize(new_size))
        # Use self.text object to set proper coordinates
        self.imageid = self.canvas.create_image(0, 0,
                                                anchor='nw', image=imagetk)
        self.canvas.lower(self.imageid)  # set it into background
        self.canvas.imagetk = imagetk

    def show_lines(self):
        original_image = Image.open(self.imagePath)
        if self.flagTU.get():
            self.draw_lines(self.tuArray, original_image, "green")
        if self.flagCU.get():
            self.draw_lines(self.cuArray, original_image, "black")
        if self.flagPU.get():
            self.draw_lines(self.puArray, original_image, "red")
        self.image = original_image
        self.show_image()

    def draw_lines(self, array, image, color):
        for rec in array:
            drawCU = ImageDraw.Draw(image)
            drawCU.rectangle(
                ((rec[0], rec[1]), (rec[0]+rec[2], rec[1]+rec[3])), outline=color)

    def callback(self, newvalue):
        print('callback({!r})'.format(newvalue))


if __name__ == "__main__":
    root = tk.Tk()
    root.title("SAYISAL VIDEO")
    root.state('zoomed')
    Main(root)
    root.mainloop()
