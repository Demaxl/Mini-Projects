"""
A Simple Encryptor
"""
from tkinter import *
from tkinter.filedialog import *
from tkinter.scrolledtext import ScrolledText
import random

tk = Tk()

def open_file():
    """ Opens the file """
    textbox.delete(1.0, END)
    file = askopenfilename(filetypes = [('Text Files', '.txt'),
                                        ('All Files', '*')])
    try:
        with open(file, 'r') as file_r:
            reading = file_r.read()
            textbox.insert(1.0, reading)
            
    except FileNotFoundError :
        print(f'Error: File Not Found')
        
    tk.title(file)
 
#Creates a list of the first 500 unicode characters.    
cipher = [chr(a) for a in range(500)] 
def encrypt():
    encr_msg = ''
    msg = textbox.get(1.0, END)
    textbox.delete(1.0, END)
    
    for i in range(len(msg)):
        new = random.choice(cipher)
        encr_msg += new
    textbox.insert(1.0, encr_msg)












textbox = ScrolledText()
btn = Button(text='Encrypt', font = ('Garamond', 25), bg='brown', fg='white',command=encrypt)
textbox.grid(row=1)
btn.grid(row=0)

menubar = Menu(tk)
tk.config(menu=menubar)

filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label='Open', command=open_file)
filemenu.add_separator()
filemenu.add_command(label='Exit', command=lambda a=tk: a.destroy())
menubar.add_cascade(label='File', menu=filemenu)

    
open_file()
tk.update()   
tk.mainloop()