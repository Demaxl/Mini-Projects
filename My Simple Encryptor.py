"""
A Simple Encryptor
"""
from tkinter import *
from tkinter.filedialog import *
from tkinter.scrolledtext import ScrolledText
import random
import string

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
 
alpha = string.ascii_letters + string.digits + string.punctuation +' ' + '\n'
unicode = [chr(i) for i in range(5000)]


def encrypt():
    global rand_code
    
    rand_code = []
    for i in range(len(alpha)):
        rand_code.append(random.choice(unicode))
    
    cipher = dict(zip(alpha, rand_code))
    encode = str.maketrans(cipher)
    
    msg = textbox.get(1.0, END)
    textbox.delete(1.0, END)
    encr_msg = msg.translate(encode)
    textbox.insert(1.0, encr_msg)
    btn2.configure(state=NORMAL)

def decrypt():
    decipher = dict(zip(rand_code, alpha))
    decode = str.maketrans(decipher)
    msg = textbox.get(1.0, END)
    textbox.delete(1.0, END)
    dmsg = msg.translate(decode)
    textbox.insert(1.0, dmsg)



textbox = ScrolledText()
btn = Button(text='Encrypt', font = ('Garamond', 25), bg='brown', fg='white',command=encrypt)
btn2 = Button(text='Decrypt', font = ('Garamond', 25), bg='brown', fg='white',
              command=decrypt, state=DISABLED)
textbox.grid(row=1)
btn.grid(row=0)
btn2.grid(row=2)

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