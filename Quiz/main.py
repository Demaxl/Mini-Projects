from question_bank import Questions
from tkinter import *
from tkinter import ttk

class Quiz:
    def __init__(self, master, questions):
        self.master = master
        self.questions = questions         
        self.result = {}
        self.score = []
        self.previoused = []
        self.count = 0
        self.name = 'Candidate'
        
        self.btn = Button(self.master, text='CLICK TO START', font=('Courier', 25), command=self.start)
        self.btn.pack(fill=BOTH, expand=1)
            
    def start(self):
        self.btn.destroy()
        n = Toplevel()
        n.anchor('s')
        n.focus()
        n.title('Candidate Name')
        Label(n, text='Enter Your Full Name:', font=('Courier', 17)).grid() 
        name = ttk.Entry(n, font=('Garamond', 14), width=30)
        name.focus()
        name.grid()
        def qstart():
           self.name = name.get() if name.get() != '' else '<No Name>'
           n.destroy()
           self.draw()
           self.checks()
        start_btn = ttk.Button(n, text='START', command=qstart)
        start_btn.grid()
        n.bind('<Return>', lambda a: qstart())
        n.mainloop()

    def draw(self):    
        frame = Frame(bg='#ffffbb')
        frame.grid(row=0, column=0)
        self.questions_lbl = Label(frame, text=self.questions[0], bg='#ffffbb',
                                   justify=LEFT, font=('Verdana', 15), wrap=0)
        self.questions_lbl.grid(row=1, column=1)
        self.number = Label(frame, text='Question 1', bg='#ffffbb',
                            font=('Courier', 12, 'bold underline'))
        self.number.grid(row=0, column=0, sticky=W)
        
        Label(self.master, text=f'Candidate: {self.name}', font=('Garamond',15, 'bold'), bg='#ffffbb').place(x=10, y=475)

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
                               bg='powder blue', fg='black', command=self.next_question, width=10)
        self.next_btn.place(x=700, y=350)
       
        self.previous_btn = Button(self.master, text='PREVIOUS', font=('Verdana',15,'bold'),
                               bg='powder blue', fg='black', width=10, relief=GROOVE, command=self.previous)
        self.previous_btn.place(x=200, y=350)
        self.submit_btn = Button(self.master, text='Submit', font=('Verdana',15,'bold'), relief=GROOVE,
                               bg='powder blue', fg='black', command=self.submit, width=10)
        self.submit_btn.place(x=845, y=0)
        self.master.bind('<KeyPress-n>', lambda a: self.next_question())
        self.master.bind('<KeyPress-p>', lambda a: self.previous())
        
    
    def checks(self):
        self.current_ans()
        self.master.update()
        if self.questions_lbl.cget('text') == self.questions[-1]:
            self.next_btn.configure(state=DISABLED)
        else:
            self.next_btn.configure(state=NORMAL)

        if (self.questions.index(self.questions_lbl['text']) + 1) == 1:
            self.previous_btn.configure(state=DISABLED)
        else:
            self.previous_btn.configure(state=NORMAL)
            
    def next_question(self):
        self.count = (self.questions.index(self.questions_lbl['text'])) + 1
        self.questions_lbl.configure(text=self.questions[self.count])
        self.number.configure(text='Question {}:'.format(
            (self.questions.index(self.questions_lbl['text']))+1))
        self.ans.set(0)
        self.checks()
        
    
    def previous(self):
        for current in range(len(self.questions)):
            if self.questions_lbl['text'] == self.questions[current]:
                self.questions_lbl.configure(text=self.questions[current-1])
                self.number.configure(text='Question {}:'.format(
                            (self.questions.index(self.questions_lbl['text']))+1))
                self.previoused.append(self.questions[current])
        self.checks()
    
    def current_ans(self):
        t = self.questions_lbl['text']
        for question, chosen_ans in self.result.items():
            if question == t:
                self.ans.set(chosen_ans)


           
    def answer(self):
        self.result[self.questions_lbl.cget('text')] = self.ans.get() 
            
    def submit(self):
        self.submit_btn.configure(state=DISABLED)
        for question, answer in self.result.items():
            if bank.QnA[question] == answer:
                self.score.append(question)
        self.show_score(len(self.score))

    def show_score(self, score):
        tk = Tk()
        tk.wm_attributes('-topmost', 1)
        tk.title('Result')
        percent = round(score/len(self.questions) * 100)
        remark = 'PASS' if percent >= 70 else 'FAIL'
        calc = percent * 4
        
        canvas = Canvas(tk, width=700, height=500)
        canvas.pack()
        
        canvas.create_text(300, 50, text='RESULT', font=('Garamond', 24, 'bold underline'), anchor='nw')
        canvas.create_text(220, 105, text=f'Candidate Name:    {self.name}', font=('Times', 15), anchor='nw')
        canvas.create_text(220, 145, text=f'Score:   You got {score} out of {len(self.questions)} questions correct ', font=('Times', 15), anchor='nw')
        
        canvas.create_text(10, 200, text='Total Score: ', font=('Courier', 20, 'bold'), anchor='nw')
        total = canvas.create_rectangle(0, 0, 400, 30, fill='blue')
        canvas.move(total, 220, 200)
        
        
        canvas.create_text(25, 250, text='Your Score: ', font=('Courier', 20, 'bold'), anchor='nw')
        my_score = canvas.create_rectangle(0, 0, calc, 30, fill='green')
        fail_score = canvas.create_rectangle(0, 0, 400, 30, fill='', outline='black')
        canvas.move(fail_score, 220, 250)
        canvas.move(my_score, 220, 250)
        
        remark_text = canvas.create_text(350, 350, text=remark, font=('Garamond', 23, 'bold underline'), fill='green', anchor='nw')

        
        if percent < 70:
            canvas.itemconfig(my_score, fill='red')
            canvas.itemconfig(remark_text, fill='red')
        text_pos = canvas.coords(my_score)
        canvas.create_text(text_pos[2]-5, text_pos[3]+5, text=f'{percent}%', anchor='nw', font=('Garamond', 15))

        tk.mainloop()

root = Tk()
root.geometry('1000x500')
root.title('Quiz')
root.config(bg='#ffffbb')
bank = Questions()

quiz = Quiz(root, bank.questions)
root.mainloop()










