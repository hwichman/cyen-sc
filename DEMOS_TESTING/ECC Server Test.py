from tkinter import *
import tkinter.messagebox as tm
import tkinter as tk
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import time
import random
import hashlib
import math
from Crypto.Cipher import AES
dataQueue = []


# Function to find modulo inverse of b. It returns  
# -1 when inverse doesn't  
# modInverse works for prime m 
def modInverse(b,m): 
    g = math.gcd(b, m)
    if (g != 1): 
        # print("Inverse doesn't exist")  
        return -1
    else:  
        # If b and m are relatively prime,  
        # then modulo inverse is b^(m-2) mode m  
        return pow(b, m - 2, m) 
  
  
# Function to compute a/b under modulo m  
def modDivisionOverAPrimeField(a,b,m): 
    a = a % m 
    inv = modInverse(b,m)
    if(inv == -1):
        print("Division not defined")
        return -1
    else: 
        return (inv*a) % m 
class FiniteEllipticCurve():
    def __init__(self, prime):
        #Generate random private large number 
        self.n = random.randint(10000,99999)
        #Generate random large numbers a and b to define the elliptical curve
        self.a = random.randint(100, 600)
        self.b = random.randint(100, 600) ** 2
        #Generate random large Finite Prime Field
        self.fieldPrime = prime
    def getRandomPoint(self):
        startingPoint = Point('inf','inf')
        for x in range (0, self.fieldPrime):
            y_square = x**3 + self.a*x + self.b
            for y in range (0, self.fieldPrime):
                if ((y**2) % self.fieldPrime == y_square % self.fieldPrime):
                    startingPoint = Point(x, y)
                    break
            if (startingPoint.x != 'inf'):
                break
        randomPoint = startingPoint.addToSelfNTimes(random.randint(0,9999), self.a, self.fieldPrime)
        while (randomPoint.x == 'inf'):
            randomPoint = randomPoint.add(startingPoint, self.a, self.fieldPrime)
        return randomPoint

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def add(self, point, a, field, fallback = True):
        #if (fallback):
            #print ("("+str(self.x)+","+str(self.y)+") + ("+str(point.x)+","+str(point.y)+")")
        if (self.x == 'inf'):
            return point
        elif (point.x == 'inf'):
            return self
        else:
            if (self.x == point.x and self.y == -point.y):
                return Point('inf', 'inf')
            else:
                lamb = 0
                if (self.x == point.x and self.y == point.y):
                    lamb = modDivisionOverAPrimeField((3*self.x**2 + a),(2*self.y),field)
                else:
                    lamb = modDivisionOverAPrimeField((point.y - self.y),(point.x - self.x),field)
                try:
                    x3 = (lamb**2 - self.x - point.x)%field
                    y3 = (lamb*(self.x - x3) - self.y)%field
                except(TypeError):
                    if (fallback):
                        return point.add(self, a, field, False)
                    x3 = 'inf'
                    y3 = 'inf'
                return Point(x3, y3)
    def negate(self):
        if (self.x == 'inf'):
            return Point('inf', 'inf')
        else:
            return Point(self.x, -self.y)
    def addToSelfNTimes(self, n, a, field):
        q = self
        r = Point('inf','inf')
        while (n > 0):
            if (n % 2 == 1):
                r = r.add(q, a, field)
                #print ("r = "+"("+str(r.x)+","+str(r.y)+")")
            q = q.add(q, a, field)
            #print ("q = "+"("+str(q.x)+","+str(q.y)+")")
            #print (n)
            n = int(n/2)
        return r

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

def getData(line):
        instructionQueue = []
        if (line.find('[') >= 0):
            if (line.find(']') >= 0):
                instruction = line[line.find('['):line.find(']') + 1]
                data = line[line.find(']') + 1:]
                if (data.find('[') >= 0):
                    instructionQueue.insert(0, getData(data))
                    data = data[0, data.find('[')]
                instructionQueue.insert(0, (instruction, data))
        return instructionQueue;

#removes the client from the server, note that this does not remove the teams score
def removeClient(client):
    print("%s:%s has left." % addresses[client])
    clients.remove(client)
    del addresses[client]
    client.close()
def send(client, msg):
    client.send(bytes(msg, "utf8"))
    
#handles a single clients packets
def handleClient(client):
    iv = '1234567890123456'.encode('utf-8')
    prime = 4409
    Ep = FiniteEllipticCurve(prime)
    P = Ep.getRandomPoint()
    ####CHANGE THIS
    private_key = random.randint(0,99999)
    print ("private_key = "+str(private_key))
    Qa = P.addToSelfNTimes(private_key, Ep.a, prime)
    msgToClient = ('[ECC0]'+str(iv)+','+str(prime)+','+str(Ep.a)+','+str(Ep.b)+','+str(P.x)+','+str(P.y)+','+str(Qa.x)+','+str(Qa.y))
    send(client, msgToClient)
    state = 0
    hashedKey = ""
    while True:
        #try:
        data = client.recv(BUFSIZ)
        if (data == b''):
            pass
            #removeClient(client)
            #break
        elif (data.decode() == "Hello Serer!"):
            print (data.decode());
            send(client, "Hello Client!")
        elif (state == 0):
            instructionQueue = getData(data.decode())
            for element in instructionQueue:
                if (element[0] == "[C1-2]"):
                    coordinates = element[1].split(",")
                    if (coordinates[0] == "-1"):
                        C1 = Point ('inf', 'inf')
                    else:
                        C1 = Point(int(coordinates[0]),int(coordinates[1]))
                    if (coordinates[2] == "-1"):
                        C2 = Point('inf', 'inf')
                    else:
                        C2 = Point(int(coordinates[2]),int(coordinates[3]))
                    privateSharedKey = C2.add(C1.addToSelfNTimes(private_key, Ep.a, prime).negate(), Ep.a, prime)
                    if (privateSharedKey.x != 'inf'):
                        while (privateSharedKey.x < 0):
                            privateSharedKey.x = (privateSharedKey.x + prime)%prime
                    if (privateSharedKey.y != 'inf'):
                        while (privateSharedKey.y < 0):
                            privateSharedKey.y = (privateSharedKey.y + prime)%prime
                    hashedKey = hashlib.md5(str(privateSharedKey.x).encode('utf-8')).digest()
                    #print ("Hashed Key = "+hashedKey)
                    aes = AES.new(hashedKey, AES.MODE_CBC, iv)
                    state+=1
        else:
            encryptedData = bytes.fromhex((data.decode()))
            decryptedData = [ chr((a) ^ (b)) for (a,b) in zip(encryptedData, hashedKey)]
            decryptedDataString = "".join(decryptedData)
            print (decryptedDataString)
            
            #decryptedMsg = aes.decrypt(data)
            #print (decryptedMsg.decode('utf-8'))
        instructionQueue = []
        #except:
            #removeClient(client)
            #break
        #the raw string of data sent from the client
        #datadecode = data.decode()
        
        
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
SERVER.listen(5)
print("Waiting for connection...")
ACCEPT_THREAD = Thread(target=acceptIncomingConnections)
ACCEPT_THREAD.start()
ACCEPT_THREAD.join()
SERVER.close()
print ("end")
