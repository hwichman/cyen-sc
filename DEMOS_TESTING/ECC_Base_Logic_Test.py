import hashlib
import random
import math
from Crypto.Cipher import AES


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
        randomPoint = startingPoint.addToSelfNTimes(random.randint(0,9999999), self.a, self.fieldPrime)
        while (randomPoint.x == 'inf'):
            randomPoint = randomPoint.add(startingPoint, self.a, self.fieldPrime)
        return randomPoint
    def isOnCurve(self, point):
        if (point.y**2 == point.x**3 + self.a*point.x + self.b):
            return True
        else:
            return False
        
            
        
        
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
                    while (x3 < 0):
                        x3 = (x3+field) % field
                    while (y3 < 0):
                        y3 = (y3+field)%field
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
        print ("Add to self N times")
        q = self
        print ("q = ("+str(q.x)+", "+str(q.y)+")")
        r = Point('inf','inf')
        print ("r = ("+str(r.x)+", "+str(r.y)+")")
        while (n > 0):
            print ("n = "+str(n))
            if (n % 2 == 1):
                r = r.add(q, a, field)
                print ("r = "+"("+str(r.x)+","+str(r.y)+")")
            q = q.add(q, a, field)
            print ("q = "+"("+str(q.x)+","+str(q.y)+")")
            n = int(n/2)
        return r

class Client():
    def __init__(self):
        self.msg = "Hello World!    "
        self.msg = self.msg.encode('utf-8')
        self.k = random.randint(0,90)
        self.k = 76
    def encryptData(self, prime, Ep, P, Qa,iv):
        self.privateSharedKey = Ep.getRandomPoint()
        self.privateSharedKey = Point(0, 2)
        #self.privateSharedKey = Point(2,10)
        print ("Start C1")
        self.privateSharedAESKey = hashlib.md5(str(self.privateSharedKey.x).encode('utf-8')).digest()
        C1 = P.addToSelfNTimes(self.k, Ep.a, prime)
        print ("P = ("+str(P.x)+", "+str(P.y)+')')
        print ("k = "+str(self.k))
        print ("a = "+str(Ep.a))
        print ("prime = "+str(prime))
        print ("C1 = ("+str(C1.x)+", "+str(C1.y)+')')
        print ("Start C2")
        C2 = self.privateSharedKey.add(Qa.addToSelfNTimes(self.k, Ep.a, prime), Ep.a, prime)
        print ("privateSharedKey = ("+str(self.privateSharedKey.x)+", "+str(self.privateSharedKey.y)+')')
        print ("Qa = ("+str(Qa.x)+", "+str(Qa.y)+')')
        print ("C2 = ("+str(C2.x)+", "+str(C2.y)+')')
        aes = AES.new(self.privateSharedAESKey, AES.MODE_CBC, iv)
        encryptedMsg = aes.encrypt(self.msg)
        return C1, C2, encryptedMsg
        

class Server():
    def __init__(self):
        self.iv = '1234567890123456'.encode('utf-8')
        self.prime = 29
        #self.prime = 13
        self.Ep = FiniteEllipticCurve(self.prime)
        self.Ep.a = 151
        self.Ep.b = 223729
        self.P = self.Ep.getRandomPoint()
        self.P = Point(20,9)
        self.private_key = random.randint(100000,999999)
        self.private_key = 39
        self.Qa = self.P.addToSelfNTimes(self.private_key, self.Ep.a, self.prime)
    def sendPublicData(self):
        return self.prime, self.Ep, self.P, self.Qa, self.iv
    def getSharedKey(self, C1, C2, encryptedMsg):
        privateSharedKey = C2.add(C1.addToSelfNTimes(self.private_key, self.Ep.a, self.prime).negate(), self.Ep.a, self.prime)
        print ("Private Shared Key = ("+str(privateSharedKey.x)+", "+str(privateSharedKey.y)+")")
        self.privateSharedAESKey = hashlib.md5(str(privateSharedKey.x).encode('utf-8')).digest()
        aes = AES.new(self.privateSharedAESKey, AES.MODE_CBC, self.iv)
        decryptedMsg = aes.decrypt(encryptedMsg)
        return decryptedMsg

client = Client()
server = Server()
# sends the primefield, the elliptic curve, a random point P on the curve, another random point on the curve obtained by adding adding p to itself a random number of times, and the initializaiton vector for AES
serverPublicData = server.sendPublicData()
#client receives that data and calculates C1 and C2 with it, uses the shared secret key(not yet known by server) and the initialization vector and sent from the server to encrypt the original message, sends C1, C2, and the encrypted message to the server
clientEncryptedMessage = client.encryptData(serverPublicData[0], serverPublicData[1], serverPublicData[2], serverPublicData[3], serverPublicData[4])
#server recieves C1, C2, and the encrypted message, uses C1 and C2 to calculate the shared secret key, uses the shared secret key and initialization vector to decrypt the message (and any following messages)
decryptedMsg = server.getSharedKey(clientEncryptedMessage[0], clientEncryptedMessage[1], clientEncryptedMessage[2])
print (decryptedMsg)
print (decryptedMsg.decode('utf-8'))

#point = Point(2122025572,898178398)
#point2 = Point(1420516887, 21379411)
#prime = 2147483647
#curve = FiniteEllipticCurve(prime)
#curve.a = 226
#curve.b = 31684
#point3 = Point(1506852263,1549946658)
#print (curve.a)
#print(curve.isOnCurve(point3))
#point = ((Point(1,5).addToSelfNTimes(86,3, 13)))
#server.prime = 13
#server.Ep = FiniteEllipticCurve(3, 8, 13)
#server.P = Point(1,5)
#server.private_key = 5
#client.encryptData(13, server.Ep ,server.P, Point(2,10), server.iv)
#server.getSharedKey(Point(9,7),Point(12,2), "asdf")


