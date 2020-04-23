
from tkinter import *
import tkinter.messagebox as tm
import tkinter as tk
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time
import random
import hashlib

CLIENT1 = "192.168.0.18"

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
        self.temperatureText.set("Temperature = Loading...")
        self.flowrateText = StringVar()
        self.flowrateText.set("Flowrate = Loading...")
        self.title_label = title_label
        labe0 = tk.Label(self, bg = "White", text = self.title_label)
        labe0.pack(side = "top")
        label = tk.Label(self, bg = "green", textvariable = self.temperatureText)
        labe8 = tk.Label(self, bg = "green", textvariable = self.flowrateText)
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

    def deletePage(self):
        self.pack_forget()

    def updateFlowRate(self, value):
        #print ("updating "+self.title_label+"'s Flowrate to "+str(value))
        pass
    def updateTemp(self, value):
        self.temperatureText.set("Temperature = "+str(value))
        #print ("updating "+self.title_label+"'s Temperature to "+str(value))
        
        

        
class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        self.pageList = []
        self.buttonframe = tk.Frame(self)
        self.container = tk.Frame(self)
        self.buttonframe.pack(side="top", fill="x", expand=False)
        self.container.pack(side="top", fill="both", expand=True)

        addPageButton = tk.Button(self.buttonframe, text="New", command=self.addPage)
        addPageButton.pack(side="right")
        
        addPageButton = tk.Button(self.buttonframe, text="Refresh", command=self.refresh)
        addPageButton.pack(side="right")
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
        dataQueue = []
        self.master.after(1, self.refresh)

def saveData():
    f = open("saveData.txt","w")
    f.write(str(monsterHealth)+'\n')
    f.write(str(getLeaderboardString()))
    f.close()

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
    while True:
        try:
            data = client.recv(BUFSIZ)
            if (data == b''):
                removeClient(client)
                break
            else:
                prop, propData = parseData(data)
                if (prop == "Temperature"):
                    dataQueue.append("UpdateTemp:"+str(addresses[client][0])+":"+str(propData))
                elif (prop == "Flowrate"):
                    dataQueue.append("UpdateFR:"+str(addresses[client][0])+":"+str(propData))
                    
        except:
            removeClient(client)
            break
        #the raw string of data sent from the client
        datadecode = data.decode()
        
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

