from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont
from tkinter import Entry, Button
import random
import os


class Main:
    def __init__(self, parent):
        self.parent = parent
        self.img = None
        self.image = StringVar()
        self.flagCU = BooleanVar()
        self.flagPU = BooleanVar()
        self.flagTU = BooleanVar()

        self.cuArray = []
        self.puArray = []
        self.tuArray = []

        self.createWidgets()
        self.readFiles()

    def createWidgets(self):
        self.mainFrame = Frame(self.parent)

        frame = Frame(self.mainFrame)
        Label(frame, text='Image').grid(sticky=W)
        Entry(frame, textvariable=self.image, width=50).grid(
            row=0, column=1, pady=10, padx=10)
        Button(frame, text='Aç', command=self.browse).grid(
            row=0, column=2, pady=10, padx=10)
        frame.pack(padx=10, pady=10)

        checkboxes = Frame(self.mainFrame)
        Checkbutton(checkboxes, text="CU", variable=self.flagCU, command=self.start).grid(row=0, column=1,
                                                                                          sticky=W, padx=15)
        Checkbutton(checkboxes, text="PU", variable=self.flagPU, command=self.start).grid(row=0, column=2,
                                                                                          sticky=W, padx=15)
        Checkbutton(checkboxes, text="TU", variable=self.flagTU, command=self.start).grid(row=0, column=3,
                                                                                          sticky=W, padx=15)
        checkboxes.pack(padx=10, pady=10)

        Button(self.mainFrame, text='Göster',
               command=self.start).pack(padx=10, pady=10)

        self.mainFrame.pack()

    def browse(self):
        self.image.set(filedialog.askopenfilename(title='Please select one (any) frame from your set of images.',
                                                  filetypes=[('Image Files', ['.jpeg', '.jpg', '.png', '.gif',
                                                                              '.tiff', '.tif', '.bmp'])]))

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
            height = int(cu.split(",")[3].split("height= ")[1].split("\n")[0])
            self.cuArray.append((x, y, width, height))
        for pu in pus:
            x = int(pu.split(",")[0].split("x= ")[1])
            y = int(pu.split(",")[1].split("y= ")[1])
            width = int(pu.split(",")[2].split("width= ")[1])
            height = int(pu.split(",")[3].split("height= ")[1].split("\n")[0])
            self.puArray.append((x, y, width, height))
        for tu in tus:
            x = int(tu.split(",")[0].split("x= ")[1])
            y = int(tu.split(",")[1].split("y= ")[1])
            width = int(tu.split(",")[2].split("width= ")[1])
            height = int(tu.split(",")[3].split("height= ")[1].split("\n")[0])
            self.tuArray.append((x, y, width, height))

    def start(self):
        imagePath = self.image.get()
        if os.path.exists(imagePath):
            if self.img:
                self.img.destroy()

            openImg = self.show_lines()
            imageTK = ImageTk.PhotoImage(openImg)
            self.img = Label(self.mainFrame, image=imageTK,
                             borderwidth=2, height=352, width=228, relief="raised")
            self.img.image = imageTK
            self.img.pack(side="bottom", fill="both", expand="yes")

    def show_lines(self):
        original_image = Image.open(self.image.get()).convert("RGBA")
        if self.flagCU.get():
            self.drive_rectangle(self.cuArray, original_image, "black")
        if self.flagPU.get():
            self.drive_rectangle(self.puArray, original_image, "red")
        if self.flagTU.get():
            self.drive_rectangle(self.tuArray, original_image, "green")

        return original_image

    def drive_rectangle(self, array, image, color):
        for rec in array:
            drawCU = ImageDraw.Draw(image)
            drawCU.rectangle(
                ((rec[0], rec[1]), (rec[0]+rec[2], rec[1]+rec[3])), outline=color)


if __name__ == "__main__":
    root = Tk()
    root.title("SAYISAL VIDEO")
    Main(root)
    root.mainloop()
