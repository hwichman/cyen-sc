
from tkinter import *
import tkinter.messagebox as tm
import tkinter as tk


class LoginFrame(Frame):
    def __init__(self, master):
        super().__init__(master)

        self.label_username = Label(self, text="Username")
        self.label_password = Label(self, text="Password")

        self.entry_username = Entry(self)
        self.entry_password = Entry(self, show="*")

        self.label_username.grid(row=0, sticky=E)
        self.label_password.grid(row=1, sticky=E)
        self.entry_username.grid(row=0, column=1)
        self.entry_password.grid(row=1, column=1)

        #self.checkbox = Checkbutton(self, text="Keep me logged in")
        #self.checkbox.grid(columnspan=2)

        self.logbtn = Button(self, text="Login", command=self._login_btn_clicked)
        self.logbtn.grid(columnspan=2)

        self.pack()

    def _login_btn_clicked(self):
                
        username = self.entry_username.get()
        password = self.entry_password.get()
        if username == "" and password == "":
            self.master.destroy()
            root = tk.Tk()
            main = MainView(root)
            main.pack(side="top", fill="both", expand=True)
            root.wm_geometry("400x400")
            #root.mainloop()       
        else:
            tm.showerror("Login error", "Incorrect Credintials")



#page classes
class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()


class Page1(Page):
    def __init__(self, *args, **kwargs):
        test = 0
        Page.__init__(self, *args, **kwargs)
        label = tk.Label(self, bg = "green", text = test)
        labe2 = tk.Label(self, bg = "White", text = "Temperature")
        
        lbl1 = tk.Label(self, text='Low Parameter')
        lbl2 = tk.Label(self, text='High Parameter')
        self.t1 = Entry(self)
        self.t2 = Entry(self)
        self.t2.pack(side = "left")
        btn1 = Button(self, text='Store')
        lbl1.place(x=100, y=50)
        self.t1.place(x=200, y=50)
        lbl2.place(x=100, y=100)
        self.t2.place(x=200, y=100)
        b1 = Button(self, text='Store', command=self.store)
        b1.place(x=200, y=150)
        
        label.pack(side = "bottom")
        labe2.pack(side = "top")
        
    def store(self):
        num1=int(self.t1.get())
        num2=int(self.t2.get())
        print(num1)
        print(num2)
        #window.destroy()

class Page2(Page):
    def __init__(self, *args, **kwargs):
        test = 0
        Page.__init__(self, *args, **kwargs)
        label = tk.Label(self, bg = "yellow", text = test)
        labe2 = tk.Label(self, bg = "White", text = "PH")
        
        lbl1 = tk.Label(self, text='Low Parameter')
        lbl2 = tk.Label(self, text='High Parameter')
        self.t1 = Entry(self)
        self.t2 = Entry(self)
        self.t2.pack(side = "left")
        btn1 = Button(self, text='Store')
        lbl1.place(x=100, y=50)
        self.t1.place(x=200, y=50)
        lbl2.place(x=100, y=100)
        self.t2.place(x=200, y=100)
        b1 = Button(self, text='Store', command=self.store)
        b1.place(x=200, y=150)
        
        label.pack(side = "bottom")
        labe2.pack(side = "top")
        
    def store(self):
        num1=int(self.t1.get())
        num2=int(self.t2.get())
        print(num1)
        print(num2)
        #window.destroy()



class Page3(Page):
    def __init__(self, *args, **kwargs):
        test = 0
        Page.__init__(self, *args, **kwargs)
        label = tk.Label(self, bg = "Red", text = test)
        labe2 = tk.Label(self, bg = "White", text = "Pressure")
        
        lbl1 = tk.Label(self, text='Low Parameter')
        lbl2 = tk.Label(self, text='High Parameter')
        self.t1 = Entry(self)
        self.t2 = Entry(self)
        self.t2.pack(side = "left")
        btn1 = Button(self, text='Store')
        lbl1.place(x=100, y=50)
        self.t1.place(x=200, y=50)
        lbl2.place(x=100, y=100)
        self.t2.place(x=200, y=100)
        b1 = Button(self, text='Store', command=self.store)
        b1.place(x=200, y=150)
        
        label.pack(side = "bottom")
        labe2.pack(side = "top")
        
    def store(self):
        num1=int(self.t1.get())
        num2=int(self.t2.get())
        print(num1)
        print(num2)
        #window.destroy()




class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        p1 = Page1(self)
        p2 = Page2(self)
        p3 = Page3(self)

        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        b1 = tk.Button(buttonframe, text="Page 1", command=p1.lift)
        b2 = tk.Button(buttonframe, text="Page 2", command=p2.lift)
        b3 = tk.Button(buttonframe, text="Page 3", command=p3.lift)

        b1.pack(side="left")
        b2.pack(side="left")
        b3.pack(side="left")

        p1.show()
        
#main function
root = Tk()
lf = LoginFrame(root)
root.mainloop()

