from tkinter import *
from tkinter import ttk
import math


tk = Tk()
 #X
tk.title('Calculator')


def callback(r, c):
    entry.insert(END, (btn[r][c]['text']))
    
def show_quad():
    tk_q = Tk()
    tk_q.title('Quadratic Calculator')
    
    Label(tk_q, text='a:', ).grid(row=0, column=0)
    e_a = ttk.Entry(tk_q)
    e_a.grid(row=0, column=1)
    
    Label(tk_q, text='b:').grid(row=1, column=0)
    e_b = ttk.Entry(tk_q)
    e_b.grid(row=1, column=1)
    
    Label(tk_q, text='c:').grid(row=2, column=0)
    e_c = ttk.Entry(tk_q)
    e_c.grid(row=2, column=1)
    
    result = Label(tk_q, text='', font=('Garamond',15))
    result.grid(row=3, column=1)
    
    def quad():
        try:
            a = eval(e_a.get())
            b = eval(e_b.get())
            c = eval(e_c.get())
            s1 = (-b + math.sqrt(b**2 -4*a*c))/2*a
            s2 = (-b - math.sqrt(b**2 -4*a*c))/2*a
            ans = 'x1 : {:.1f}\nx2 : {:.1f}'.format(s1, s2)
            color = 'black'
        except SyntaxError:
            ans = 'Syntax Error'
            color = 'red'
        except ZeroDivisionError:
            ans = 'Cannnot divide by zero'
            color = 'red'
        except NameError:
            ans = 'Enter Numbers only'
            color = 'red'
            
        result.configure(text= ans, fg=color)

    btn = ttk.Button(tk_q, text='Calculate',  command=quad)
    btn.grid(row=4, column=1)

def show_temp():
    tk_con = Tk()
    
    
    def calculate(event):
        try:
            temp = int(entry.get())
            temp = 9/5*temp+32
            output_label.configure(text = 'Converted: {:.1f} fahrenheit'.format(temp))
            entry.delete(0,END)
        except:
            output_label.configure(text = 'Syntax Error')
        
    
    message_label = Label(tk_con, text='Enter a temperature',font=('Verdana', 16))
    output_label = Label(tk_con, font=('Verdana', 16))
    
    entry = ttk.Entry(tk_con, font=('Verdana', 16), width=4)
    entry.bind('<Return>', calculate)
    
    
    message_label.grid(row=0, column=0)
    entry.grid(row=0, column=1)
    output_label.grid(row=1, column=0, columnspan=3, sticky = W) # sticky means align left

    
def calculate(e):
    operator = entry.get()
    try:
        ans = eval(operator)
        color = 'white'
    except SyntaxError:
        ans = 'Syntax Error'
        color = 'red'
    except ZeroDivisionError:
        ans = 'Cannnot divide by zero'
        color = 'red'
    except NameError:
        ans = 'Enter Numbers only'
        color = 'red'
    entry.delete(0, END)
    entry.insert(0, ans)
    entry.configure(bg=color)
    
def clear():
    entry.delete(0, END)
    entry.configure(bg='white')
    
n = [[7,8,9,'+'],
     [4,5,6,'-'],
     [1,2,3,'*'],
     [0,'.','//','/']]

btn = [[0,0,0,0],
       [0,0,0,0],
       [0,0,0,0],
       [0,0,0,0]]

entry = Entry(font=('Arial', 12), width=20, bd=4)
entry.grid(row=0, column=1, columnspan=3)
tk.bind('<Return>', calculate)

def hover(btn):
    btn.configure(fg='white', bg='black')
def leave(btn):
    btn.configure(fg='black', bg='SystemButtonFace')
def hover_effect(b,r,c):
    b[r][c].configure(fg='white', bg='black')
def leave_effect(b,r,c):
    b[r][c].configure(fg='black', bg='SystemButtonFace')
    
btn_frame = Frame()
btn_frame.grid(row=1, column=1)
for r in range(4):
    for c in range(4):
        btn[r][c] = Button(btn_frame, bd=4, padx=14, pady=14, text=str(n[r][c]), 
           font=('Verdana',16), command=lambda r=r,c=c: callback(r, c ))
        btn[r][c].grid(row=r, column=c)
        btn[r][c].bind('<Enter>', lambda b=btn, r=r, c=c: hover_effect(btn,r,c))
        btn[r][c].bind('<Leave>', lambda b=btn, r=r, c=c: leave_effect(btn,r,c))
        
clear_btn = Button(tk, text='CE', bd=4, padx=14, pady=134,
                   command=clear)
clear_btn.grid(row=1, column=3)
clear_btn.bind('<Enter>', lambda dummy=0: hover(clear_btn))
clear_btn.bind('<Leave>', lambda dummy=0: leave(clear_btn))


eql_btn = Button(tk, text='=', bd=4, padx=150, pady=14,command=lambda a=0:calculate(a))
eql_btn.grid(row=4, column=0, columnspan=4)
eql_btn.bind('<Enter>', lambda dummy=0: hover(eql_btn))
eql_btn.bind('<Leave>', lambda dummy=0: leave(eql_btn))


menubar = Menu(tk)
tk.config(menu=menubar)

scimenu = Menu(menubar, tearoff=0)
scimenu.add_command(label='Quadratic Calculator', command=show_quad)
scimenu.add_command(label='Temperature Converter', command=show_temp)
menubar.add_cascade(label='Other Calculators', menu=scimenu)


tk.mainloop()
