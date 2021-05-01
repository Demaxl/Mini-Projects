class Questions:
    def __init__(self):
        self.questions = [
"""
Who is the 45th president of the United States of America?

A. George W. Bush

B. Hillary Clinton

C. Donald Trump

D. Joe Biden 
""",
"""
Who was the first man to land on the moon?

A. Yuri Gagaarin

B. Neil Armstrong

C. Edmund Hillary

D. George Washington
""",
"""
What is the Probability that 6 cats would be picked at random from 12 cats?

A. 1/2

B. 1/4

C. 2/3

D. 5/8
""",
"""
What is the tallest mountain in the world?

A. Mount. Kilimanjaro

B. Mount. Rushmore

C. Mount. Fuji

D. Mount Everest
""",
"""
Who invented the aeroplane?

A. The Wright brothers

B. Albert Einstein

C. Bill Clinton

D. Sir Isaac Newton
"""
]            
        self.answers = ['C', 'B', 'A', 'D', 'A']
        self.QnA = dict(zip(self.questions, self.answers))

def main():
    test = Questions()
    for i,j in test.QnA.items():
        print(i,j, sep=' ')
   
#to test the questions you inputted     
if __name__ == '__main__':
    main()
    
    

"""
from question_bank import Questions
from tkinter import *
from tkinter import ttk
import threading

class Quiz(threading.Thread):
    def __init__(self, master, questions):
        threading.Thread.__init__(self)
        self.master = master
        self.questions = questions #\n
        self.q = iter(self.questions)
        self.result = {}
        self.score = []
        self.draw()
    
    def draw(self):
        
        frame = Frame(bg='#ffffbb')
        frame.grid(row=0, column=0)
        self.questions_lbl = Label(frame, text=next(self.q), bg='#ffffbb',
                                   justify=LEFT, font=('Verdana', 15), wrap=0)
        self.questions_lbl.grid(row=1, column=1)
        self.number = Label(frame, text='Question 1', bg='#ffffbb',
                            font=('Courier', 12, 'bold underline'))
        self.number.grid(row=0, column=0, sticky=W)

        self.ans = StringVar()
        style = ttk.Style()
        style.configure('TRadiobutton', background='#ffffbb')
        self.abtn = ttk.Radiobutton(frame, variable=self.ans, value='A', style='TRadiobutton', command=self.answer)
        self.abtn.place(x=84, y=105)
        self.bbtn = ttk.Radiobutton(frame, variable=self.ans, value='B', style='TRadiobutton', command=self.answer)
        self.bbtn.place(x=84, y=155)
        self.cbtn = ttk.Radiobutton(frame, variable=self.ans, value='C', style='TRadiobutton', command=self.answer)
        self.cbtn.place(x=84, y=205)
        self.dbtn = ttk.Radiobutton(frame, variable=self.ans, value='D', style='TRadiobutton', command=self.answer)
        self.dbtn.place(x=84, y=255)

        self.next_btn = Button(self.master, text='NEXT', font=('Verdana',15,'bold'), relief=GROOVE,
                               bg='powder blue', fg='black', command=self.next_quest, width=10)
        self.next_btn.place(x=700, y=350)
       
        self.previous_btn = Button(self.master, text='PREVIOUS', font=('Verdana',15,'bold'),
                               bg='powder blue', fg='black', width=10, relief=GROOVE)
        self.previous_btn.place(x=200, y=350)
        self.submit_btn = Button(self.master, text='Submit', font=('Verdana',15,'bold'), relief=GROOVE,
                               bg='powder blue', fg='black', command=self.submit, width=10)
        self.submit_btn.place(x=845, y=0)
        self.master.bind('<KeyPress-n>', lambda a: self.next_quest())
        
    
    def run(self):
        try:
            while True:       
                if self.questions_lbl['text'] == self.questions[-1]:
                    self.next_btn.configure(state=DISABLED)
                    return
        except:
            return

    def next_quest(self):
        try: 
            self.questions_lbl.configure(text=next(self.q))
            self.number.configure(text='Question {}:'.format((self.questions.index(self.questions_lbl['text']))+1))
            self.ans.set(0)
            self.master.update()
            
        except StopIteration:
            return
    
    def answer(self):
        self.result[self.questions_lbl.cget('text')] = self.ans.get() 
            
    def submit(self):
        self.submit_btn.configure(state=DISABLED)
        for question, answer in self.result.items():
            if bank.QnA[question] == answer:
                self.score.append(question)
            else:
                pass
        self.show_score()

    def show_score(self):
        print(f'You got {len(self.score)} correct')


root = Tk()
root.geometry('1000x500')
root.title('Quiz')
root.config(bg='#ffffbb')
bank = Questions()

quiz = Quiz(root, bank.questions)
quiz.start()
root.mainloop()
#\n
#score = []
#
#
#
#
#
#for question in bank.questions:
#    ans = (input(question + '\n')).upper()
#    if bank.QnA[question] == ans:
#        score.append(question)
#    

""" 
    
    
    
    
    
    
