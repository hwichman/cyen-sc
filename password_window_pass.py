
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
        test = str(test)
        Page.__init__(self, *args, **kwargs)
        label = tk.Label(self, bg = "green", text = "The Current Temperature is " + test)
        labe8 = tk.Label(self, bg = "green", text = "The Current Flow Rate is " + test)
        labe2 = tk.Label(self, bg = "White", text = "Temperature Sensor")
        label.place(x=30, y=315)
        labe2.place(x=150, y = 20)
        labe8.place(x=200, y = 315)

        #Temperature Entry
        lbl1 = tk.Label(self, text='Low Parameter')
        lbl2 = tk.Label(self, text='High Parameter')
        lbl1.place(x=50, y=50)
        lbl2.place(x=200, y=50)
        self.t1 = Entry(self)
        self.t2 = Entry(self)
        self.t1.place(x=50, y=75)
        self.t2.place(x=200, y=75)

        #PH Sensor Entry
        labe3 = tk.Label(self, bg = "White", text = "Flow Rate Sensor")
        labe3.place(x=150, y = 105)
        lbl3 = tk.Label(self, text='Low Parameter')
        lbl4 = tk.Label(self, text='High Parameter')
        lbl3.place(x=50, y=130)
        lbl4.place(x=200, y=130)
        self.t3 = Entry(self)
        self.t4 = Entry(self)
        self.t3.place(x=50, y=150)
        self.t4.place(x=200, y=150)
        
        #Button Code
        btn1 = Button(self, text='Store')
        b1 = Button(self, text='Store', command=self.store)
        b1.place(x=175, y=200)
  
        
    def store(self):
        num1=str(self.t1.get())
        num2=str(self.t2.get())
        num3=str(self.t3.get())
        num4=str(self.t4.get())
        labe4 = tk.Label(self, bg = "White", text = "Temp Low parameter = " + num1)
        labe4.place(x=50, y = 250)
        labe5 = tk.Label(self, bg = "White", text = "Temp High parameter = " + num2)
        labe5.place(x= 200, y = 250)
        labe6 = tk.Label(self, bg = "White", text = "Flow Rate Low parameter = " + num3)
        labe6.place(x=40, y = 280)
        labe7 = tk.Label(self, bg = "White", text = "Flow Rate High parameter = " + num4)
        labe7.place(x=215, y = 280)
        
        

class Page2(Page):
    def __init__(self, *args, **kwargs):
        test = 0
        test = str(test)
        Page.__init__(self, *args, **kwargs)
        label = tk.Label(self, bg = "green", text = "The Current Temperature is " + test)
        labe8 = tk.Label(self, bg = "green", text = "The Current Flow Rate is " + test)
        labe2 = tk.Label(self, bg = "White", text = "Temperature Sensor")
        label.place(x=30, y=315)
        labe2.place(x=150, y = 20)
        labe8.place(x=200, y = 315)

        #Temperature Entry
        lbl1 = tk.Label(self, text='Low Parameter')
        lbl2 = tk.Label(self, text='High Parameter')
        lbl1.place(x=50, y=50)
        lbl2.place(x=200, y=50)
        self.t1 = Entry(self)
        self.t2 = Entry(self)
        self.t1.place(x=50, y=75)
        self.t2.place(x=200, y=75)

        #PH Sensor Entry
        labe3 = tk.Label(self, bg = "White", text = "Flow Rate Sensor")
        labe3.place(x=150, y = 105)
        lbl3 = tk.Label(self, text='Low Parameter')
        lbl4 = tk.Label(self, text='High Parameter')
        lbl3.place(x=50, y=130)
        lbl4.place(x=200, y=130)
        self.t3 = Entry(self)
        self.t4 = Entry(self)
        self.t3.place(x=50, y=150)
        self.t4.place(x=200, y=150)
        
        #Button Code
        btn1 = Button(self, text='Store')
        b1 = Button(self, text='Store', command=self.store)
        b1.place(x=175, y=200)
  
        
    def store(self):
        num1=str(self.t1.get())
        num2=str(self.t2.get())
        num3=str(self.t3.get())
        num4=str(self.t4.get())
        labe4 = tk.Label(self, bg = "White", text = "Temp Low parameter = " + num1)
        labe4.place(x=50, y = 250)
        labe5 = tk.Label(self, bg = "White", text = "Temp High parameter = " + num2)
        labe5.place(x= 200, y = 250)
        labe6 = tk.Label(self, bg = "White", text = "Flow Rate Low parameter = " + num3)
        labe6.place(x=40, y = 280)
        labe7 = tk.Label(self, bg = "White", text = "Flow Rate High parameter = " + num4)
        labe7.place(x=215, y = 280)



class Page3(Page):
    def __init__(self, *args, **kwargs):
        test = 0
        test = str(test)
        Page.__init__(self, *args, **kwargs)
        label = tk.Label(self, bg = "green", text = "The Current Temperature is " + test)
        labe8 = tk.Label(self, bg = "green", text = "The Current Flow Rate is " + test)
        labe2 = tk.Label(self, bg = "White", text = "Temperature Sensor")
        label.place(x=30, y=315)
        labe2.place(x=150, y = 20)
        labe8.place(x=200, y = 315)

        #Temperature Entry
        lbl1 = tk.Label(self, text='Low Parameter')
        lbl2 = tk.Label(self, text='High Parameter')
        lbl1.place(x=50, y=50)
        lbl2.place(x=200, y=50)
        self.t1 = Entry(self)
        self.t2 = Entry(self)
        self.t1.place(x=50, y=75)
        self.t2.place(x=200, y=75)

        #PH Sensor Entry
        labe3 = tk.Label(self, bg = "White", text = "Flow Rate Sensor")
        labe3.place(x=150, y = 105)
        lbl3 = tk.Label(self, text='Low Parameter')
        lbl4 = tk.Label(self, text='High Parameter')
        lbl3.place(x=50, y=130)
        lbl4.place(x=200, y=130)
        self.t3 = Entry(self)
        self.t4 = Entry(self)
        self.t3.place(x=50, y=150)
        self.t4.place(x=200, y=150)
        
        #Button Code
        btn1 = Button(self, text='Store')
        b1 = Button(self, text='Store', command=self.store)
        b1.place(x=175, y=200)
  
        
    def store(self):
        num1=str(self.t1.get())
        num2=str(self.t2.get())
        num3=str(self.t3.get())
        num4=str(self.t4.get())
        labe4 = tk.Label(self, bg = "White", text = "Temp Low parameter = " + num1)
        labe4.place(x=50, y = 250)
        labe5 = tk.Label(self, bg = "White", text = "Temp High parameter = " + num2)
        labe5.place(x= 200, y = 250)
        labe6 = tk.Label(self, bg = "White", text = "Flow Rate Low parameter = " + num3)
        labe6.place(x=40, y = 280)
        labe7 = tk.Label(self, bg = "White", text = "Flow Rate High parameter = " + num4)
        labe7.place(x=215, y = 280)


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
root.geometry("500x500")

