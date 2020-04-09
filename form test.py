from tkinter import *
class MyWindow:
    def __init__(self, win):
        self.lbl1=Label(win, text='Low Parameter')
        self.lbl2=Label(win, text='High Parameter')
        self.t1=Entry(bd=3)
        self.t2=Entry()
        self.btn1 = Button(win, text='Store')
        self.lbl1.place(x=100, y=50)
        self.t1.place(x=200, y=50)
        self.lbl2.place(x=100, y=100)
        self.t2.place(x=200, y=100)
        self.b1=Button(win, text='Store', command=self.store)
        self.b1.place(x=200, y=150)
       
    def store(self):
        num1=int(self.t1.get())
        num2=int(self.t2.get())
        print(num1)
        print(num2)
        window.destroy()
   

window=Tk()
mywin=MyWindow(window)
window.title('Water Parameters')
window.geometry("400x300+10+10")
window.mainloop()
