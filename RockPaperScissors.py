import random                                                       
from tkinter import *
import tkinter.messagebox
num = None

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def name_to_num(player):
    if player == 'rock':
        return 0
    elif player == 'paper':
        return 1
    elif player == 'scissors':
        return 2
    else:
        print('Invalid')

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def num_to_name(comp):
    if comp == 0:
        return('rock')
    elif comp == 1:
        return('paper')
    elif comp == 2:
        return('scissors')
    else:
        raise ValueError

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def compare(choice):
    global wins
    comp = random.randrange(0, 3)
    com_attributes(comp)
    player_input = choice
    diff = (player_input - comp) % 3
    comp_output = num_to_name(comp)
    player_output = num_to_name(choice)
    if diff == 1:
        canvas.itemconfig(win_msg, text = 'YOU WIN!!', fill = 'green')

    elif diff == 2:
        canvas.itemconfig(win_msg, text = 'LOSER!!', fill = 'red')
    else:
        canvas.itemconfig(win_msg, text = 'ITS A TIE!', fill = 'orange')

#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#drawing
tk = Tk()
tk.wm_attributes('-topmost', 1)
tk.resizable(0,0)
canvas = Canvas(tk, width = 500, height = 500, bd = 0, highlightthickness = 0)
canvas.pack()

#----------------------------------------------------------------------------------------------
img = PhotoImage(file = 'play_msg.png')
rock_img = PhotoImage(file = 'rock.png')            #image for rock
paper_img = PhotoImage(file = 'paper.png')      #image for paper
scissors_img = PhotoImage(file = 'scissors.png')    #image for scissors
img_view = canvas.create_image(100,250, image = img, anchor = NW)
player_text = canvas.create_text(126, 335, text = '')
#-------------------------------------------------------------------------------------------------
com_rock_img = PhotoImage(file = 'com_rock.png')
com_paper_img = PhotoImage(file = 'com_paper.png')
com_scissors_img = PhotoImage(file = 'com_scissors.png')
com_img_view = canvas.create_image((400, 250), image = img, anchor = NE)
com_text = canvas.create_text(365, 335, text = '')
#------------------------------------------------------------------------------------
win_msg = canvas.create_text(250, 400, text = '', fill = '', font = ('Times', 25, 'bold'))

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def rock():
    global num
    num = name_to_num('rock')
    compare(num)
    canvas.itemconfig(img_view, image = rock_img)
    canvas.itemconfig(player_text, text = 'ROCK')

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def paper():
    global num
    num = name_to_num('paper')
    compare(num)
    canvas.itemconfig(img_view, image = paper_img)
    canvas.itemconfig(player_text, text = 'PAPER')
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def scissors():
    global num
    num = name_to_num('scissors')
    compare(num)
    canvas.itemconfig(img_view, image = scissors_img)
    canvas.itemconfig(player_text, text = 'SCISSORS')
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def  com_attributes(n):
    if n == 0:
        canvas.itemconfig(com_img_view, image = com_rock_img)
        canvas.itemconfig(com_text, text =  (num_to_name(n)).upper())
    elif n == 1:
        canvas.itemconfig(com_img_view, image = com_paper_img)
        canvas.itemconfig(com_text, text = (num_to_name(n)).upper())
    elif n ==2:
        canvas.itemconfig(com_img_view, image = com_scissors_img)
        canvas.itemconfig(com_text, text = (num_to_name(n)).upper())
        




#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
rock_btn = Button(tk, text = 'ROCK', fg = 'white', bg = 'brown', relief = GROOVE, width = 15, command = rock)
rock_btn.place(x = 0, y = 100)

paper_btn = Button(tk, text = 'PAPER', fg = 'white', bg = 'brown', relief = GROOVE, width = 15, command = paper)
paper_btn.place(x = 0, y = 125)

scissors_btn = Button(tk, text = 'SCISSORS', fg = 'white', bg = 'brown', relief = GROOVE, width = 15, command = scissors)
scissors_btn.place(x = 0, y = 150)

canvas.create_text(136, 225, text = 'PLAYER', font = ('Arial', 15, 'bold'))
canvas.create_text(375, 225, text = 'COMPUTER', font = ('Arial', 15, 'bold'))
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def close():
    tk.destroy()
    exit()

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def guide():
    tkinter.messagebox.showinfo("How to Play", "Click the 'ROCK' button to choose rock\nClick the 'PAPER' button to choose paper\nClick the 'SCISSORS' button to choose scissors")
menubar = Menu(tk)
tk.config(menu = menubar)

filemenu = Menu(menubar, tearoff = 0)
menubar.add_cascade(label = 'File', menu = filemenu)
filemenu.add_command(label = 'Exit', command = close)

helpmenu = Menu(menubar, tearoff = 0)
menubar.add_cascade(label = 'Help', menu = helpmenu)
helpmenu.add_command(label = 'How to Play', command = guide)


















    
    
 
