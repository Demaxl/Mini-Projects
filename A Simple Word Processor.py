from tkinter import *
from tkinter.filedialog import *
from tkinter.scrolledtext import ScrolledText
from tkinter.messagebox import *


tk= Tk()


textbox = ScrolledText(tk, font = ('Garamond', 15))
textbox.grid(row = 0, column = 0)

saved = False
curr_open = None

def open_file():
    global curr_open
    textbox.delete(1.0, END)
    file = askopenfilename(initialdir = 'C:/Users/maxis/Desktop',
                           filetypes = [('Text Files', '.txt'),
                                        ('All Files', '*')])
    curr_open = file
    
    with open(file, 'r') as opened:
        read_file = opened.read()
        textbox.insert(1.0, read_file)
        
    tk.title(curr_open)
    
        
def saveas_file():
    global saved, curr_open

    if saved == False:
        s = asksaveasfilename(filetypes=[('Text Files', '.txt')])
        save = s + '.txt'
        with open(save, 'w+') as savedas:
            savedas.write(textbox.get(1.0, END))
            saved = True
            curr_open = save
            
    
    if saved == True:
        with open(curr_open, 'w') as resave:
            resave.write(textbox.get(1.0, END))
            
    tk.title(curr_open)
    
def save_file():
    pass
    

menubar = Menu(tk)
tk.config(menu = menubar)


filemenu = Menu(menubar, tearoff = 0)
menubar.add_cascade(label='File', menu=filemenu)
filemenu.add_command(label='Open', command=open_file)
filemenu.add_command(label='Save as', command=saveas_file)

filemenu.add_separator()

filemenu.add_command(label='Exit', command=lambda a=tk: a.destroy())

tk.bind('<Control-s>', lambda dummy=0: saveas_file())
tk.bind('<Control-o>', lambda dummy=0: open_file())


def quitter():
    ask = askquestion(title='Quit', message='Are you sure you want to quit?')
    if ask == 'yes':
        tk.destroy()

tk.title('None')     
tk.protocol('WM_DELETE_WINDOW', quitter)
tk.mainloop()