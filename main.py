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
        Entry(frame, textvariable=self.image, width=50).grid(row=0, column=1, pady=10, padx=10)
        Button(frame, text='Aç', command=self.browse).grid(row=0, column=2, pady=10, padx=10)
        frame.pack(padx=10, pady=10)

        checkboxes = Frame(self.mainFrame)
        Checkbutton(checkboxes, text="CU", variable=self.flagCU, command=self.show_lines).grid(row=0, column=1,
                                                                                               sticky=W, padx=15)
        Checkbutton(checkboxes, text="PU", variable=self.flagPU, command=self.show_lines).grid(row=0, column=2,
                                                                                               sticky=W, padx=15)
        Checkbutton(checkboxes, text="TU", variable=self.flagTU, command=self.show_lines).grid(row=0, column=3,
                                                                                               sticky=W, padx=15)
        checkboxes.pack(padx=10, pady=10)

        Button(self.mainFrame, text='Göster', command=self.start).pack(padx=10, pady=10)
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
            x = cu.split(",")[0].split("x= ")[1]
            y = cu.split(",")[1].split("y= ")[1]
            width = cu.split(",")[2].split("width= ")[1]
            height = cu.split(",")[3].split("height= ")[1].split("\n")[0]
            self.cuArray.append((x, y, width, height))
        for pu in pus:
            x = pu.split(",")[0].split("x= ")[1]
            y = pu.split(",")[1].split("y= ")[1]
            width = pu.split(",")[2].split("width= ")[1]
            height = pu.split(",")[3].split("height= ")[1].split("\n")[0]
            self.puArray.append((x, y, width, height))
        for tu in tus:
            x = tu.split(",")[0].split("x= ")[1]
            y = tu.split(",")[1].split("y= ")[1]
            width = tu.split(",")[2].split("width= ")[1]
            height = tu.split(",")[3].split("height= ")[1].split("\n")[0]
            self.tuArray.append((x, y, width, height))


    def start(self, array, color):
        imagePath = self.image.get()
        if os.path.exists(imagePath):
            openImg = Image.open(imagePath).convert("RGBA")
            
            imageTK = ImageTk.PhotoImage(openImg)
            img = Label(self.mainFrame, image=imageTK, borderwidth=2, relief="raised")
            img.image = imageTK
            img.pack(side="bottom", fill="both", expand="yes")

            draw = ImageDraw.Draw(openImg)
            draw.line(((0, 0), (10, 10)))

    def show_lines(self):
        if self.flagCU.get():
            self.start(self.cuArray, "red")
        if self.flagPU.get():
            self.start(self.cuArray, "blue")
        if self.flagTU.get():
            self.start(self.cuArray, "green")



if __name__ == "__main__":
    root = Tk()
    root.title("SAYISAL VIDEO")
    Main(root)
    root.mainloop()