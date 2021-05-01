from tkinter import *
import tkinter.messagebox
import string
import re
import random


class Hang:
    def __init__(self, master, canvas, words):
        self.master = master
        self.canvas = canvas
        self.words = words
        bank = random.choice(self.words)
        self.word = bank[0]
        self.hint = bank[1]
        self.btn = [0] * 26
        self.out = ['__'] * len(self.word)
        self.label = [0] * len(self.word)
        self.fail_count = 0
        self.drawLayout()
        
        
    def drawLayout(self):
        title = Label(self.master, text='HANGMAN', font='Arial 25 bold italic underline', fg='brown', bg='#ffe7ce')
        title.grid(row=0, column=0, columnspan=26, padx=300)
        self.drawOut()
        self.buttons()
        self.restart_btn = Button(text='Restart', fg='white', bg='#535353', relief=RAISED,
                                  font='Garamond 24 ', command=self.restart)
        self.restart_btn.place(x=650, y=435)
        self.restart_btn.bind('<Enter>', self.hover)
        self.restart_btn.bind('<Leave>', self.leave)
        
        self.hint_btn= Button(text='Hint', fg='white', bg='brown', relief=RAISED,
                              font='Garamond 15', width=5, command=self.show_hint)
        self.hint_btn.place(x=50, y= 460)
        self.master.update()
        
        
    def drawOut(self):
        for i in range(len(self.out)):
            self.label[i] = Label(self.master, text=self.out[i],font='Garamond 25 bold underline', bg='#ffe7ce', justify=LEFT)
            self.label[i].grid(row=5, column=i+9, pady=150)   
            
    def buttons(self):
        L = string.ascii_uppercase
        xpos = 100
        ypos = 300
        for r in range(26):
            self.btn[r] = Button(self.master, text=L[r], font='Verdana 20', width=3, relief=GROOVE,
                            command=lambda r=r: self.callback(r), fg='black', bg='light blue')
            self.btn[r].place(x=xpos, y=ypos, anchor='e')
            self.btn[r].bind('<Enter>', self.hover)
            self.btn[r].bind('<Leave>', self.leave)
            
            xpos += 65
            if xpos >= 800:
                xpos = 165
                ypos = 365
            if xpos > 685 and ypos >= 365:
                    xpos = 230
                    ypos = 430
    
    
    def callback(self, pos):
        self.btn[pos].unbind('<Enter>')
        self.btn[pos].unbind('<Leave>')
        guess = self.btn[pos].cget('text')
        if guess in self.word:
            W = re.sub(guess, '*', self.word)
            for i in range(len(W)):
                if W[i] == '*':
                    self.out[i] = self.word[i]
                    self.btn[pos].configure(bg='white', fg='black', state=DISABLED)
        else:
            self.btn[pos].configure(bg='black', state=DISABLED)
            self.drawMan()
            self.fail_count += 1
            
        for i in range(len(self.out)):
            self.label[i].configure(text=self.out[i])
            self.master.update()
        
        if self.win():
            for i in self.btn:
                i.configure(state=DISABLED)
            self.hint_btn.configure(state=DISABLED)
            tkinter.messagebox.showinfo('Correct', 'YOU WIN!!!')
            
        self.lose()
    def lose(self):
        if self.fail_count == 10:
            for i in self.btn:
                i.configure(state=DISABLED)
            self.hint_btn.configure(state=DISABLED)
            tkinter.messagebox.showinfo('FAILED', f'You failed\nThe word was {self.word}')
                
                    
    def clear(self):
        for i in self.btn:
            i.destroy()
        for i in self.label:
            i.destroy()
        self.canvas.delete(ALL)
        
    def restart(self):
        self.clear()
        bank = random.choice(self.words)
        self.word = bank[0]
        self.hint = bank[1]
        self.btn = [0] * 26
        self.out = ['__'] * len(self.word)
        self.label = [0] * len(self.word)
        self.fail_count = 0
        self.drawLayout()
    
               
    def hover(self, event):
        if event.widget['text'] != 'Restart':
            event.widget.configure(bg='#ffffbb', fg='black')
        else:
            event.widget.configure(bg='black')
                                   
    def leave(self, event):
        if event.widget['text'] != 'Restart':
            event.widget.configure(bg='light blue', fg='black')
        else:
            event.widget.configure(bg='#535353')
        
    def win(self):
        gword = ''
        for i in self.out:
            gword += i
        if gword == self.word:
            return True
    
    
    def drawMan(self):
        f = self.canvas.create_line(10, 200, 60, 200, state='hidden') # floor
        s = self.canvas.create_line(35, 200, 35, 50, state='hidden')  # stand
        p = self.canvas.create_line(35, 50, 85, 50, state='hidden')   # long pole
        
        r = self.canvas.create_line(85, 50, 85, 70, state='hidden')  # rope holder
        
        h = self.canvas.create_oval(75, 70, 95, 90, fill='', outline='black', state='hidden') # head
        
        b = self.canvas.create_line(85, 90, 85, 130, state='hidden') # body

        ra = self.canvas.create_line(85, 100, 100, 115, state='hidden') # right arm
        
        la = self.canvas.create_line(85, 100, 70, 115, state='hidden') # left arm
        
        rl = self.canvas.create_line(85, 130, 100, 145, state='hidden') # right leg
        
        ll = self.canvas.create_line(85, 130, 70, 145, state='hidden') # left leg
        prop = [f, s, p, r, h, b, ra, la, rl, ll]
        self.canvas.itemconfig(prop[self.fail_count], state='normal')
        
    def show_hint(self):
        tkinter.messagebox.showinfo('HINT', self.hint)
        self.drawMan()
        self.fail_count += 1
        self.lose()
        self.drawMan()
        self.fail_count += 1
        self.lose()

root = Tk()
root.minsize(800, 500)
root.resizable(0, 0)
root.title('Hangman')
root.config(bg='#ffe7ce')

# feel free to add more words
words_lst = [('AEROPLANE', 'It carries passengers'),
             ('TABLE', 'You place things on it'),
             ('EARTH', 'A planet in the solar system'),
             ('MATHEMATICS', 'A subject'),
             ('EUROPE', 'A continent'),
             ('INTEGRATION', 'Combining things'),
             ('DYNAMIC', 'Able to Change'),
             ('ROBUST', 'Sturdy and Strong'),
             ('PAKISTAN', 'A south Asian country'),
             ('LANGUAGE', 'A means of communicating'),
             ('PUNCTUATION', 'Used in sentences'),
             ('BITTY', 'Very small'),
             ('CHESS', 'An ancient strategic game'),
             ('MARBLE', 'A crystalline rock'),
             ('SCORES', 'Indicating performance'),
             ('ACID', 'A chemical'),
             ('SNEEZE', 'Sudden expulsion of air'),
             ('AMASS', 'To collect'),
             ('APPLE', 'A fruit'),
             ('RABBIT', 'An Animal'),
             ('ARID', 'Very dry'),
             ('ROBOT', 'A machine that does tasks'),
             ('SPOON', 'Used for eating'),
             ('DOOR', 'Used to enter a place')]

canvas = Canvas(root, width=800, height=500, bg='#ffe7ce')
canvas.place(x=0, y=0)

h = Hang(root, canvas, words_lst)

root.mainloop()


# Hangman by Abdullahi A.A




