import hashlib
import random
from Crypto.Cipher import AES

def modDivisionOverAPrimeField(numerator, denominator, field):
    if (numerator > field):
        numerator = numerator % field
    if (denominator > field):
        denominator = denominator % field
    for i in range (1, field):
        if (((denominator * i) % field) == numerator):
            return i

class FiniteEllipticCurve():
    def __init__(self, prime):
        #Generate random private large number 
        self.n = random.randint(10000,99999)
        #Generate random large numbers a and b to define the elliptical curve
        self.a = random.randint(100, 600)
        self.b = random.randint(100, 600)
        #Generate random large Finite Prime Field
        self.fieldPrime = prime
    def getRandomPoint(self):
        startingPoint = Point('inf','inf')
        for x in range (0, self.fieldPrime):
            y_square = x**3 + self.a*x + self.b
            for y in range (0, self.fieldPrime):
                if ((y**2) % self.fieldPrime == y_square % self.fieldPrime):
                    startingPoint = Point(x, y)
        randomPoint = startingPoint.addToSelfNTimes(random.randint(0,10), self.a, self.fieldPrime)
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

class Client():
    def __init__(self):
        self.msg = "Hello World!    "
        self.msg = self.msg.encode('utf-8')
        privateSharedKeyInt = random.randint(0,999999)
        self.k = random.randint(0,90)
    def encryptData(self, prime, Ep, P, Qa,iv):
        self.privateSharedKey = Ep.getRandomPoint()
        self.privateSharedAESKey = hashlib.md5(str(self.privateSharedKey.x).encode('utf-8')).digest()
        C1 = P.addToSelfNTimes(self.k, Ep.a, prime)
        C2 = self.privateSharedKey.add(Qa.addToSelfNTimes(self.k, Ep.a, prime), Ep.a, prime)
        aes = AES.new(self.privateSharedAESKey, AES.MODE_CBC, iv)
        encryptedMsg = aes.encrypt(self.msg)
        return C1, C2, encryptedMsg
        

class Server():
    def __init__(self):
        self.iv = '1234567890123456'.encode('utf-8')
        self.prime = 13
        self.Ep = FiniteEllipticCurve(self.prime)
        self.P = self.Ep.getRandomPoint()
        self.private_key = random.randint(0,999999)
        self.Qa = self.P.addToSelfNTimes(self.private_key, self.Ep.a, self.prime)
    def sendPublicData(self):
        return self.prime, self.Ep, self.P, self.Qa, self.iv
    def getSharedKey(self, C1, C2, encryptedMsg):
        privateSharedKey = C2.add(C1.addToSelfNTimes(self.private_key, self.Ep.a, self.prime).negate(), self.Ep.a, self.prime)
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

