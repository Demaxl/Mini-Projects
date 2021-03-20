"""
This program shows a screen noise which is what shows when you have lost the signal e.g  A TV
"""
from random import randint
from tkinter import *
from PIL import Image, ImageTk
import time
root = Tk()

def start():
    global image, photo, started    
    started = True
    while started:
        pix = image.load()
        for w in range(200):
            for h in range(200):
                r = randint(0,255)
                pix[w,h] = (r, r, r)
        
        photo = ImageTk.PhotoImage(image)
        canvas.create_image(0,0,image=photo,anchor=NW)
        root.update()
        time.sleep(0.01)


def stop():
    global started
    started = False
    load_file()


def load_file():
    global image, photo
    image = Image.new(mode='RGB', size=(200,200))

started = False
btn = Button(text='Start',command=start)
btn.grid(row=2, column=0, sticky = W)

btn = Button(text='Stop',command=stop)
btn.grid(row=2, column=1)


canvas = Canvas(width=200, height=200)
canvas.grid(row = 1, column = 0)
load_file()
mainloop()