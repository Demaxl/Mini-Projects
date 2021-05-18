from tkinter import *
import random


b = [[0,0,0],
     [0,0,0],
     [0,0,0]]

states = [[0,0,0],
          [0,0,0],
          [0,0,0]]

X_ATTR = {'text':'X', 'fg':'blue', 'bg':'white'} # attributes of X
O_ATTR = {'text':'O', 'fg':'orange', 'bg':'black'} # attributes of O
#------------------------------------------------------------------------------------------------------------------

def callback(r,c):
    if states[r][c] == 0 and stop_game == False:
        b[r][c].configure(**X_ATTR)
        states[r][c] = 'X'
        check_for_winner()
        
        # Computer's Move
        if not stop_game:
            if not check('O', O_ATTR) and not check('X', O_ATTR):
                random_move()      
            check_for_winner()
#------------------------------------------------------------------------------------------------------------------------------

def random_move():
    r = random.randrange(0, 3)
    c = random.randrange(0, 3)
    if states[r][c] == 0:
        b[r][c].configure(**O_ATTR)
        states[r][c] = 'O'
    else:
        if all(states[0])==all(states[1])==all(states[2])==True: # Checks if board is full
            for r in range(3):
                for c in range(3):
                    b[r][c].configure(bg='grey')
        else:
            random_move()
#----------------------------------------------------------------------------------------------------------------------------

def check(option, action):
    # check rows 
    for r in range(3):
        if states[r][0]==states[r][1]==option and states[r][2]==0:
            b[r][2].configure(**action)
            states[r][2] = 'O'
            return True
        elif states[r][0]==states[r][2]==option and states[r][1]==0:
            b[r][1].configure(**action)
            states[r][1] = 'O'
            return True
        elif states[r][1]==states[r][2]==option and states[r][0]==0:
            b[r][0].configure(**action)
            states[r][0] = 'O'
            return True
    
    # check columns 
    for c in range(3):
        if states[0][c]==states[1][c]==option and states[2][c]==0:
            b[2][c].configure(**action)
            states[2][c] = 'O'
            return True
        elif states[0][c]==states[2][c]==option and states[1][c]==0:
            b[1][c].configure(**action)
            states[1][c] = 'O'
            return True
        elif states[1][c]==states[2][c]==option and states[0][c]==0:
            b[0][c].configure(**action)
            states[0][c] = 'O'
            return True
    
    # Checking diagonal left to right 
    if states[0][0]==states[1][1]==option and states[2][2]==0:
        b[2][2].configure(**action)
        states[2][2] = 'O'
        return True
    elif states[0][0]==states[2][2]==option and states[1][1]==0:
        b[1][1].configure(**action)
        states[1][1] = 'O'
        return True
    elif states[1][1]==states[2][2]==option and states[0][0]==0:
        b[0][0].configure(**action)
        states[0][0] = 'O'
        return True
    
    # Checking diagonal right to left 
    if states[2][0]==states[1][1]==option and states[0][2]==0:
        b[0][2].configure(**action)
        states[0][2] = 'O'
        return True
    elif states[0][2]==states[1][1]==option and states[2][0]==0:
        b[2][0].configure(**action)
        states[2][0] = 'O'
        return True
    elif states[2][0]==states[0][2]==option and states[1][1]==0:
        b[1][1].configure(**action)
        states[1][1] = 'O'
        return True
    return False
#----------------------------------------------------------------------------------------------------------------
    
def check_for_winner():
    global stop_game
    for i in range(3):
        if states[i][0]==states[i][1]==states[i][2]!=0:
            b[i][0].configure(bg='grey')
            b[i][1].configure(bg='grey')
            b[i][2].configure(bg='grey')
            stop_game = True
            
    for i in range(3):
        if states[0][i]==states[1][i]==states[2][i]!=0:
            b[0][i].configure(bg='grey')
            b[1][i].configure(bg='grey')
            b[2][i].configure(bg='grey')
            stop_game = True
            
    if states[0][0]==states[1][1]==states[2][2]!=0:
        b[0][0].configure(bg='grey')
        b[1][1].configure(bg='grey')
        b[2][2].configure(bg='grey')
        stop_game = True
        
    if states[2][0]==states[1][1]==states[0][2]!=0:
        b[2][0].configure(bg='grey')
        b[1][1].configure(bg='grey')
        b[0][2].configure(bg='grey')
        stop_game = True
#-------------------------------------------------------------------------------------------------------------
        
def restart():
    global stop_game, player, b, states, full
    stop_game = False
    player = 'X'
    full = []
    for i in range(3):
        for j in range(3):
            b[i][j].configure(text = '',font=('Verdana', 56), width=3, bg='yellow', state=NORMAL)
            states[i][j] = 0
#---------------------------------------------------------------------------------------------------------------
            
tk = Tk()
tk.wm_attributes('-topmost', 1)
for i in range(3):
    for j in range(3):
        b[i][j] = Button(font=('Verdana', 56), width=3, bg='yellow',
        command = lambda r=i,c=j: callback(r,c))
        b[i][j].grid(row = i, column = j)
        
player = 'X'
stop_game = False

menubar = Menu(tk)
tk.config(menu = menubar)
menubar.add_radiobutton(label = 'RESTART', command = restart)
menubar.add_radiobutton(label = 'QUIT', command = lambda a=tk: a.destroy())


tk.mainloop()
