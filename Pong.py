from tkinter import *
from tkinter.messagebox import *
import random
import time


class Ball:
    'Class that draws and handles the movement and collision of the ball.'
    def __init__(self, canvas, lpad, rpad):
        self.direction = [-1,1]
        self.y = random.choice(self.direction)
        self.x = 2
        self.canvas = canvas
        self.lpad = lpad
        self.rpad = rpad
        self.id = canvas.create_oval(10,10,30,30, fill = 'green', outline='white')
        self.canvas.move(self.id, 231, 185)
        self.running = False
        self.left_win = 0
        self.draw_lwin = self.canvas.create_text(100, 30, text=f'Wins: {self.left_win}',
                                                 fill='red', font=('Verdana', 15))
        self.right_win = 0
        self.draw_rwin = self.canvas.create_text(400, 30, text=f'Wins: {self.right_win}',
                                                 fill='blue', font=('Verdana', 15))
        self.canvas.bind_all('<Button-1>', self.play)
        self.win_label = Label(font = ('Garamond',  20), bg='black')
        self.win_label.place(x=208, y=198)
        self.play_text = self.canvas.create_text(250,100,text='CLICK TO PLAY',
                                                 font=('Verdana',20, 'bold'), fill='green')
        
    def hit_pad_left(self, pos):
        lpad_pos = self.canvas.coords(self.lpad.pad_left)
        if pos[3] >= lpad_pos[1] and pos[3] <= lpad_pos[3]:
            if pos[0] <= lpad_pos[2]:
                return True
        return False
            
    def hit_pad_right(self, pos):
        rpad_pos = self.canvas.coords(self.rpad.pad_right)
        if pos[3] >= rpad_pos[1] and pos[3] <= rpad_pos[3]:
            if pos[2] >= rpad_pos[0]:
                return True
        return False
            
    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        pos = self.canvas.coords(self.id) 
         #[x1,y1,x2,y2]              
        if pos[1] <= 0:                                  
            self.y = abs(self.y)
        if pos[3] >= self.canvas.winfo_height():
            self.y = -self.y
        if pos[0] <= 15 and self.hit_pad_left(pos)==False:
            self.reset()
            self.x = 2
            self.y = random.choice(self.direction)
            self.right_win += 1
            self.canvas.itemconfig(self.draw_rwin, text=f'Wins: {self.right_win}')

        if pos[2] >= 485 and self.hit_pad_right(pos)==False:
            self.reset()
            self.x = -2
            self.y = random.choice(self.direction)
            self.left_win += 1
            self.canvas.itemconfig(self.draw_lwin, text=f'Wins: {self.left_win}')
            
        if self.hit_pad_right(pos) == True:
            self.x = -self.x
            self.x -= 0.1
            if self.y >= 0:
                self.y += 0.1
            else:
                self.y -= 0.1
        if self.hit_pad_left(pos) == True:
            self.x = -self.x
            self.x += 0.1
            if self.y >= 0:
                self.y += 0.1
            else:
                self.y -= 0.1
        self.winner()
        
    def reset(self):
        self.lpad.lreset()
        self.rpad.rreset()
        self.canvas.coords(self.id, 10,10,30,30)
        self.canvas.move(self.id, 231, 185)

    def winner(self):
        if self.left_win == 5:
            self.win_label.configure(text='P1 WINS!!', fg='red', bg='white')
            self.running = False
        if self.right_win == 5:
            self.running = False
            self.win_label.configure(text='P2 WINS!!', fg='blue', bg='white')
            
    def game_restart(self):
        self.left_win = 0
        self.right_win = 0
        self.x = 2
        self.y = random.choice(self.direction)
        self.canvas.itemconfig(self.draw_lwin, text=f'Wins: {self.left_win}')
        self.canvas.itemconfig(self.draw_rwin, text=f'Wins: {self.right_win}')
        self.lpad.lreset()
        self.rpad.rreset()
        self.canvas.coords(self.id, 10,10,30,30)
        self.canvas.move(self.id, 231, 185)
        self.canvas.coords(self.lpad.pad_left, 0, self.lpad.top, 15, self.lpad.bottom)
        self.canvas.coords(self.rpad.pad_right, 485, self.rpad.top, 500, self.rpad.bottom)
        self.win_label.configure(text='', bg='black')
        self.running = False
        self.canvas.itemconfig(self.play_text, text='CLICK TO START')

    def play(self, event):
        self.running = True
        self.canvas.itemconfig(self.play_text, text='')
                
#--------------------------------------------------------------------------------------------------            
class LeftPaddle:
    'Class that handles the attributes of the left paddle'
    def __init__(self, canvas, top=150, bottom=250):
        self.canvas = canvas
        self.top = top
        self.bottom = bottom
        self.y = 0
        self.canvas.create_line(15,0,15,500, fill='white')
        self.pad_left = canvas.create_rectangle(0,self.top,15,self.bottom, fill='red')
        self.canvas.bind_all('<KeyPress-w>', self.up)
        self.canvas.bind_all('<KeyPress-s>', self.down)
        self.canvas.bind_all('<KeyPress-W>', self.up)
        self.canvas.bind_all('<KeyPress-S>', self.down)
        
        
    def draw(self):
        self.canvas.move(self.pad_left, 0, self.y)
        pos = self.canvas.coords(self.pad_left)
        if pos[1] <= 0:
            self.y = 0
        elif pos[3] >= self.canvas.winfo_height():
            self.y = 0
    def up(self, event):
        self.y = -2
    
    def down(self, event):
        self.y = 2

    def lreset(self):
        self.y = 0
        return True
        #self.canvas.coords(self.pad_left,0, self.top,15,self.bottom)

#------------------------------------------------------------------------------------------------------
class RightPaddle:
    'Class that handles the attribute of the right paddle'
    def __init__(self, canvas, top=150, bottom=250):
        self.canvas = canvas
        self.top = top
        self.bottom = bottom
        self.y = 0
        self.canvas.create_line(485,0,485,500, fill='white')

        self.pad_right = self.canvas.create_rectangle(485,self.top,500,self.bottom, fill='blue')
        self.canvas.bind_all('<KeyPress-Up>', self.up)
        self.canvas.bind_all('<KeyPress-Down>', self.down)
        
    def draw(self):
        self.canvas.move(self.pad_right, 0, self.y)
        pos = self.canvas.coords(self.pad_right)
        if pos[1] <= 0:
            self.y = 0
        elif pos[3] >= self.canvas.winfo_height():
            self.y = 0
            
    def up(self, event):
        self.y = -2
    
    def down(self, event):
        self.y = 2
        
    def rreset(self):
        self.y = 0
        #self.canvas.coords(self.pad_right,485,self.top,500,self.bottom)
#----------------------------------------------------------------------------------------        

tk = Tk()
tk.wm_attributes('-topmost', 1)
tk.title('Pong')
tk.resizable(0,0)

canvas = Canvas(tk, width=500, height=400, bd=0, bg='black')
canvas.pack()
canvas.create_line(250,0,250,400 ,fill='white')

lpad = LeftPaddle(canvas)
rpad = RightPaddle(canvas)
ball = Ball(canvas, lpad, rpad)

def start():
    lpad.draw()
    rpad.draw()
    ball.draw()
    
def restart():
    ball.game_restart()

restart = Button(tk, text='RESTART', fg='white', bg='black', font=('Arial', 20),
                 relief=GROOVE, command = restart)
restart.pack(side = BOTTOM, fill = X)

def guide():
    msg="""
        CONTROLS:
        Player 1:  Use "up" and "down" to move the blue paddle.
        Player 2:  Use "w" and "s" to move the red paddle.
        
        OBJECTIVE:
        First to reach 5 is the winner.
        If the ball hits the other players sides you get a point.
        The ball becomes faster as the game progresses.
        """
    showinfo(title='How to play', message=msg)

menubar = Menu(tk)
tk.config(menu=menubar)

menubar.add_radiobutton(label='INFO', command=guide)
menubar.add_separator()
menubar.add_radiobutton(label='EXIT', command=lambda a=tk: a.destroy())

try:
    while 1:
        tk.update()
        tk.update_idletasks()
        time.sleep(0.01)
        if ball.running == True:
            start()
except TclError:
    print('Game has been closed')






tk.mainloop()
