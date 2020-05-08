
from tkinter import *
import tkinter.messagebox as tm
import tkinter as tk
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time
import random
import hashlib



dataQueue = []

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
        global main
        username = self.entry_username.get()
        password = self.entry_password.get()
        if username == "" and password == "":
            self.master.destroy()
            SERVER.listen(5)
            print("Waiting for connection...")
            ACCEPT_THREAD = Thread(target=acceptIncomingConnections)
            ACCEPT_THREAD.start()
            root = tk.Tk()
            main = MainView(root)
            main.pack(side="top", fill="both", expand=True)
            main.master.wm_geometry("400x400")
            #root.mainloop()       
        else:
            tm.showerror("Login error", "Incorrect Credintials")



#page classes
class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
    def show(self):
        self.lift()


class SensorPage(Page):
    def __init__(self, title_label):
        Page.__init__(self)
        self.temperatureText = StringVar()
        self.temperatureText.set("Loading...")
        self.flowrateText = StringVar()
        self.flowrateText.set("Loading...")
        self.pressureText = StringVar()
        self.pressureText.set("Loading...")
        self.title_label = title_label
        labe0 = tk.Label(self, bg = "White", text = self.title_label)
        labe0.pack(side = "top")
        self.labe1 = tk.Label(self, bg = "green", textvariable = self.temperatureText)
        self.labe8 = tk.Label(self, bg = "green", textvariable = self.flowrateText)
        self.labe9 = tk.Label(self, bg = "green", textvariable = self.pressureText)
        
        lbl1 = tk.Label(self, text='LO Param.')
        lbl2 = tk.Label(self, text='HI Param.')
        lbl1.place(x=100, y=50)
        lbl2.place(x=165, y=50)

        self.num1 = StringVar()
        self.num2 = StringVar()
        self.num3 = StringVar()
        self.num4 = StringVar()
        self.num5 = StringVar()
        self.num6 = StringVar()
        self.num1.set("Not Set")
        self.num2.set("Not Set")
        self.num3.set("Not Set")
        self.num4.set("Not Set")
        self.num5.set("Not Set")
        self.num6.set("Not Set")
        
        self.labe4 = tk.Label(self, bg = "White", textvariable = self.num1)
        self.labe4.place(x=100, y = 200)
        self.labe5 = tk.Label(self, bg = "White", textvariable = self.num2)
        self.labe5.place(x= 165, y = 200)
        
        self.labe6 = tk.Label(self, bg = "White", textvariable = self.num3)
        self.labe6.place(x=100, y = 225)
        self.labe7 = tk.Label(self, bg = "White", textvariable = self.num4)
        self.labe7.place(x=165, y = 225)
        
        self.labe11 = tk.Label(self, bg = "White", textvariable = self.num5)
        self.labe11.place(x=100, y = 250)
        self.labe12 = tk.Label(self, bg = "White", textvariable = self.num6)
        self.labe12.place(x=165, y = 250)



        #Temperature Entry
        labe2 = tk.Label(self, bg = "White", text = "Temperature")
        labe2.place(x=10, y = 75)
        self.t1 = Entry(self, width = 10)
        self.t2 = Entry(self, width = 10)
        self.t1.place(x=100, y=75)
        self.t2.place(x=165, y=75)
        #self.labe1.place(x=230, y=75)

        #Flow rate Sensor Entry
        labe3 = tk.Label(self, bg = "White", text = "Flow Rate")
        labe3.place(x=10, y = 100)
        self.t3 = Entry(self, width = 10)
        self.t4 = Entry(self, width = 10)
        self.t3.place(x=100, y=100)
        self.t4.place(x=165, y=100)
        #labe8.place(x=230, y = 100)

        #Pressure Sensor Entry
        labe10 = tk.Label(self, bg = "White", text = "Pressure")
        labe10.place(x=10, y = 125)
        self.t5 = Entry(self, width = 10)
        self.t6 = Entry(self, width = 10)
        self.t5.place(x=100, y=125)
        self.t6.place(x=165, y=125)
        #labe9.place(x=230, y = 125)

        #Button Code
        b1 = Button(self, text='Store', command=self.store)
        b1.place(x=270, y=100)


        lbl3 = tk.Label(self, text='Stored Values')
        lbl3.place(x=140, y=160)
        lbl3 = tk.Label(self, text='Current')
        lbl3.place(x=230, y=175)
        #Temperature Stored Values
        labe2 = tk.Label(self, bg = "White", text = "Temperature")
        labe2.place(x=10, y = 200)
        self.labe1.place(x=230, y=200)
        
        #Flowrate Stored Values
        labe2 = tk.Label(self, bg = "White", text = "Flow Rate")
        labe2.place(x=10, y = 225)
        self.labe8.place(x=230, y=225)
        
        #Pressure Stored Values
        labe2 = tk.Label(self, bg = "White", text = "Pressure")
        labe2.place(x=10, y = 250)
        self.labe9.place(x=230, y=250)
        
        
    def store(self):
        #low temp param
        if (str(self.t1.get()) != ""):
            self.num1.set(str(self.t1.get()))
        #high temp param
        if (str(self.t2.get()) != ""):
            self.num2.set(str(self.t2.get()))
        #low fr param
        if (str(self.t3.get()) != ""):
            self.num3.set(str(self.t3.get()))
        #high fr param
        if (str(self.t4.get()) != ""):
            self.num4.set(str(self.t4.get()))
        #low pressure param
        if (str(self.t5.get()) != ""):
            self.num5.set(str(self.t5.get()))
        if (str(self.t6.get()) != ""):
            #high pressure param
            self.num6.set(str(self.t6.get()))

    def deletePage(self):
        self.pack_forget()

    def updateFlowRate(self, value):
        #print ("updating "+self.title_label+"'s Flowrate to "+str(value))
        self.flowrateText.set(str(value))
        if (self.labe6["text"] != "Not Set" and self.labe7["text"] != "Not Set"):
            delta = 0.05*(float(self.labe7["text"]) - float(self.labe6["text"]))
            if (float(value) > float(self.labe7["text"]) or float(value) < float(self.labe6["text"])):
                self.labe8.config(bg="Red")
            elif (float(value) > (float(self.labe7["text"]) - delta) or float(value) < (float(self.labe6["text"]) + delta)):
                self.labe8.config(bg="Yellow")
            else:
                self.labe8.config(bg="Green")
    def updateTemp(self, value):
        self.temperatureText.set(str(value))
        if (self.labe4["text"] != "Not Set" and self.labe5["text"] != "Not Set"):
            delta = 0.05*(float(self.labe5["text"]) - float(self.labe4["text"]))
            if (float(value) > float(self.labe5["text"]) or float(value) < float(self.labe4["text"])):
                self.labe1.config(bg="Red")
            elif (float(value) > (float(self.labe5["text"]) - delta) or float(value) < (float(self.labe4["text"]) + delta)):
                self.labe1.config(bg="Yellow")
            else:
                self.labe1.config(bg="Green")
        #print ("updating "+self.title_label+"'s Temperature to "+str(value))
    def updatePressure(self, value):
        #print ("updating "+self.title_label+"'s Pressure to "+str(value))
        self.pressureText.set(str(value))
        if (self.labe11["text"] != "Not Set" and self.labe12["text"] != "Not Set"):
            delta = 0.05*(float(self.labe12["text"]) - float(self.labe11["text"]))
            if (float(value) > float(self.labe12["text"]) or float(value) < float(self.labe11["text"])):
                self.labe9.config(bg="Red")
            elif (float(value) > (float(self.labe12["text"]) - delta) or float(value) < (float(self.labe11["text"]) + delta)):
                self.labe9.config(bg="Yellow")
            else:
                self.labe9.config(bg="Green")
        

        
class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.pageList = []
        self.buttonframe = tk.Frame(self)
        self.container = tk.Frame(self)
        self.buttonframe.pack(side="top", fill="x", expand=False)
        self.container.pack(side="top", fill="both", expand=True)

        self.refresh()

        for page in self.pageList:
            page.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)
            button = Button(self.buttonframe, text=page.title_label, command=page.lift)
            button.pack(side="left")
    def addPage(self, ip):
        newPage = SensorPage(str(ip))
        self.pageList.append(newPage)
        newPage.place(in_=self.container, x=0, y=0, relwidth=1, relheight=1)
        button = tk.Button(self.buttonframe, text=newPage.title_label, command=newPage.lift)
        button.pack(side="left")
    def refresh(self):
        global dataQueue
        for item in dataQueue:
            protocol, info = parseData(item)
            if (protocol == "NewClient"):
                self.addPage(str(info))
            elif (protocol == "UpdateTemp"):
                client, temperature = parseData(str(info))
                #print ("client = " + str(client))
                #print ("temperature = "+ str(temperature))
                for page in self.pageList:
                    if (page.title_label == client):
                        page.updateTemp(temperature)
            elif (protocol == "UpdateFR"):
                client, flowrate = parseData(str(info))
                for page in self.pageList:
                    if (page.title_label == client):
                        page.updateFlowRate(flowrate)
            elif (protocol == "UpdatePr"):
                #print ("here")
                client, pressure = parseData(str(info))
                for page in self.pageList:
                    if (page.title_label == client):
                        page.updatePressure(pressure)
        dataQueue = []
        self.master.after(1, self.refresh)


#allows new connections to be made
def acceptIncomingConnections():
    global dataQueue
    global numClients
    while True:
        #accept the connection
        client, clientAddress = SERVER.accept()
        addresses[client] = clientAddress
        clients.append(client)
        dataQueue.append("NewClient:"+str(clientAddress[0]))
        #send the current time data to the client
        print("%s:%s has connected." % clientAddress)
        Thread(target=handleClient, args=(client,)).start()

def getData(instruction, datadecode):
        endIndex = datadecode.find("[",datadecode.find(instruction)+3)
        if (endIndex == -1):
            endIndex = len(datadecode)
        return datadecode[datadecode.find(instruction)+3:endIndex]

#removes the client from the server, note that this does not remove the teams score
def removeClient(client):
    print("%s:%s has left." % addresses[client])
    clients.remove(client)
    del addresses[client]
    client.close()
 
#handles a single clients packets
def handleClient(client):
    #send(client)
    while True:
        try:
            data = client.recv(BUFSIZ)
            if (data == b''):
                removeClient(client)
                break
            else:
                prop, propData = parseData(data)
                if (prop == "T"):
                    dataQueue.append("UpdateTemp:"+str(addresses[client][0])+":"+str(propData))
                elif (prop == "F"):
                    dataQueue.append("UpdateFR:"+str(addresses[client][0])+":"+str(propData))
                elif (prop == "P"):
                    dataQueue.append("UpdatePr:"+str(addresses[client][0])+":"+str(propData))
                    
        except:
            removeClient(client)
            break
        #the raw string of data sent from the client
        datadecode = data.decode()
        
def send(client, msg):
    client.send(bytes(msg, "utf8")) 
        
def parseData(data):
    prop = ""
    propData = ""
    propFlag = True
    for c in data:
        if (not isinstance(c, str)):
            c = chr(c)
        if (c != ":" and propFlag):
            prop += c
        elif (propFlag == False):
            propData += c
        else:
            propFlag = False
    return str(prop), str(propData)

addresses = {} #keeps track of the ip address and port corresponding to the client, exists for informative(printing) purpose only, actual functional config happens with the clients array
clients = [] #keeps track of all the clients

HOST = "0.0.0.0"

PORT = 23435
BUFSIZ = 4096
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)        
#main function
root = Tk()
lf = LoginFrame(root)
#root.mainloop()

