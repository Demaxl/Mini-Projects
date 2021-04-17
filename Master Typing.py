""" Master Typing using Tkinter"""

from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter.messagebox import askquestion, showinfo
from tkinter import ttk
from time import sleep
from os import urandom
from math import log
from random import shuffle
from itertools import cycle
import _thread

#Xx
class Type:
     
    def __init__(self, master, essay, tips):
        self.master = master
        self.essay = essay
        shuffle(tips)
        self.tips = iter(cycle(tips))
        self.temp = self.essay[1]
        self.passage = Label(self.master, text = self.essay[0], padx = 45, pady=50, bg='#ffffbb',
                            font=('Verdana', 15), relief = RAISED, justify = LEFT, wraplength=1269)
        self.passage.pack(side=TOP, fill = X)
        
        self.textinput = ScrolledText(self.master, width=90,height=18, bd=10,
                                      font=('Garamond', 15), state = NORMAL, wrap=WORD)
        self.textinput.place(x=290, y=290)
        
        self.timer_clicked = False
        minutes = self.temp // 60
        seconds = self.temp % 60
        self.countdown = Label(text='{}:{:02d}'.format(minutes, (seconds)), font=('Arial', 19),
                               bg='yellow', relief=GROOVE)
        self.countdown.place(x=620, y=250)
        self.countdown.bind('<Button-1>', self.count)
        self.textinput.bind('<Control-Return>', lambda dummy=0: self.submit())
        self.submitted = False

        self.draw()
        
    def draw(self):
        self.result = Label(text='', font=('Arial', 18, 'bold'))
        self.result.place(x=50, y=350)
        self.remark = Label(text='', font=('Arial', 18, 'bold'))
        self.remark.place(x=65, y=550)
        self.random_tip = Button(self.master, text='Tips', font=('Arial',12,'bold'), fg='black', bg='powder blue',
                                 relief=GROOVE, width=10, command=self.show_tips)
        self.random_tip.place(x=1180, y=370)
        self.exit_btn = Button(self.master, text='Quit', font=('Arial',12,'bold'), fg='black', bg='powder blue', relief=GROOVE,
                               width=10, command=lambda : self.master.destroy())
        self.exit_btn.place(x=1180, y=420)
        self.restart_btn = Button(self.master, text='Restart', font=('Arial',12,'bold'), fg='black', bg='powder blue',
                                  width=10, relief=GROOVE, command=self.restart)
        self.restart_btn.place(x=1180, y=550)
        
        level = ['Easy', 'Normal', 'Hard']
        self.level_var = StringVar()
        self.level_var.set('Normal')
        self.difficulty_easy = ttk.Radiobutton(self.master, text='Easy', variable = self.level_var, value='Easy', command=self.level_change)
        self.difficulty_easy.place(x=1280, y=280)
        self.difficulty_normal = ttk.Radiobutton(self.master, text='Normal', variable = self.level_var, value='Normal', command=self.level_change)
        self.difficulty_normal.place(x=1280, y=300)
        self.difficulty_hard = ttk.Radiobutton(self.master, text='Hard', variable = self.level_var, value='Hard', command=self.level_change)
        self.difficulty_hard.place(x=1280, y=320)
        self.difficulty = Label(self.master, text=f'Difficulty: Normal', font=('Times', 14), fg='orange')
        self.difficulty.place(x=1190, y=230)
        
        self.start_text = Label(self.master, text='Click the Timer to Start!', font=('Courier', 13, 'bold underline'))
        self.start_text.place(x=530, y= 220)
        
    
    def submit(self):
        self.submitted = True
        
    def calculate(self):
        total = self.essay[0].split()
        typed_words = self.textinput.get(1.0, END).split()
        
        correct = []
        incorrect = []
        wrong_case = []
        excess_words = []
        if len(typed_words) == len(total):
            for i in range(len(total)):
                if total[i] == typed_words[i]:
                    correct.append(total[i])
                else:
                    incorrect.append(typed_words[i])
                    if typed_words[i].lower() == total[i].lower():
                        wrong_case.append(typed_words[i])
        
        elif len(typed_words) < len(total):
            diff = len(total) - len(typed_words)
            for i in range(len(typed_words)):
                if typed_words[i] == total[i]:
                    correct.append(typed_words[i])
                else:
                    incorrect.append(typed_words[i])
                    if typed_words[i].lower() == total[i].lower():
                        wrong_case.append(typed_words[i])
                    
            empty = ['space'] * diff
            for e in empty: 
                incorrect.append(e)
        else:
            for i in range(len(total)):
                if typed_words[i] == total[i]:
                    correct.append(typed_words[i])
                else:
                    incorrect.append(typed_words[i])
                    if typed_words[i].lower() == total[i].lower():
                        wrong_case.append(typed_words[i])
            for i in range(1, len(typed_words) - len(total)):
                excess_words.append(typed_words[-i])
            for i in excess_words:
                incorrect.append(i)
            
        score = 100 - ((len(incorrect)/len(total))*100) 
        self.result.configure(text=f'Accuracy: {round(score) if score > 0 else 0}%\n\n' + 
                                                f'Wrong Case: {len(wrong_case)}\n\n Excess Words: {len(excess_words)}')
        if score >= 70:
            color = 'green'
            word = 'PASS'
        else:
            color = 'red'
            word = 'FAIL'
        self.remark.configure(text=f"Remark: {word}", fg=color)
        return True
    
    def run(self, name, temp):
        self.start_text.destroy()
        self.timer_clicked = True
        self.textinput.delete(1.0, END)
        self.textinput.focus()
        
        try:           
            while 1:
                mins,secs = divmod(temp, 60)
                self.countdown.configure(text='{}:{:02d}'.format(mins, secs))
                if temp == 0:
                    self.countdown.configure(text='Time UP')
                    self.textinput.configure(state=DISABLED)
                    self.calculate()
                    return
        
                elif temp <= 10:
                    self.countdown.configure(bg='red', fg= 'white')
                if self.submitted == True:
                    self.calculate()
                    return

                temp -= 1
                sleep(0.1)
                self.master.update()
        except RuntimeError:
            print('MASTER TYPING HAS BEEN CLOSED')
        except TclError:
            print('MASTER TYPING HAS BEEN CLOSED')

    def count(self, event):
        if not self.timer_clicked:
            _thread.start_new_thread(self.run, ('Timer', self.temp))

        
    def restart(self):
        self.master.destroy()
        main()
        
    def level_change(self):
        if not self.timer_clicked:
            if self.level_var.get() == 'Easy':
                self.temp = self.temp + 30
                colour = 'green'
            elif self.level_var.get() == 'Normal':
                self.temp = self.essay[1]
                colour = 'orange'
            else:
                self.temp -= 30
                colour = 'red'
            minutes = self.temp // 60
            seconds = self.temp % 60
            self.difficulty.configure(text=f'Difficulty: {self.level_var.get()}', fg=colour)
            self.countdown.configure(text='{}:{:02d}'.format(minutes, (seconds)))
            self.master.update()

    def show_tips(self):
        showinfo(title='Tip', message=next(self.tips))        

    
def main():
    try:
        root = Tk()
        root.title('MASTER TYPING')
        root.geometry('1366x750')
        root.wm_attributes('-topmost', 1)
        
        msg = ["""David and John were walking down the road then David saw something peculiar.
It was a bird with no wings and was flying. He immediately notified John who was very enthusiastic about animals.
The expression David saw on John's face instantly left him paralysed because John who is meant to be dauntless in a situation like this was timid.""", 110]
        
        msg2 = ["""The approach to the University is being restructed to ease the flow of traffic. The works and Services complex is also under construction, and we intend to move into the completed(major) part of it within the next few weeks.
All these projects are being executed with an eye to aesthetics for we recognize the important influence of a beautiful and healthy environment on its habitants. We feel the cluster of building on a small space such as we have, should be so well designed as to have beneficial psychological and sociological effect on all members of the community.""", 165]
        
        msg3 = ["""The banking sector consolidation, which ended in December 2005, came with the realisation that those who understood the market merely plunged into it, notched premium stocks and left the directors of those firms to grapple with the challenges of a hostile business environment.
Many investors who, hitherto, had staked their funds on high risk projects, which offers little or no profit, therefore, found solace in their discovery of the stock market as a potential cash cow.""", 135]
        
        tip = ["""Try your best to type exactly what you see in the passage.""",
"""Correct words that have incorrect case are counted as incorrect words.""",
"""Punctuations are very important, incorrect or no punctuations are wrong.""",
"""Paragraphs are very important.""",
"""In a scenario where you write more words than the passage.
Excess words would be counted as incorrect words.""",
"""Press [Ctrl + Enter] if you done typing the passage.""",
"""70% accuracy is the pass mark """
            ]
        # better random number generator
        def urandint(a,b):
            x = urandom(int(log(b-a+1)/log(256))+1)
            total = 0
            for (i,y) in enumerate(x):
                total += y*(2**i)
            return total%(b-a+1)+a
    
        essays = [msg, msg2, msg3]
        text = Type(root, essays[urandint(0, 2)], tip)
        
        
        def quitter():
            ans = askquestion(title='Quit?', message='Do you want to quit?')
            if ans == 'yes':
                root.destroy()
            
        root.protocol('WM_DELETE_WINDOW', quitter)
        root.mainloop()
    except RuntimeError:
        pass
    
if __name__ == '__main__':
    main()
