# SWANS

This is a READ ME file for our Senior Capstone project at LA Tech University - Spring 2020. 
The project consists of a Secure Wireless Network System using a Python-based App, multiple sensors and ECC Encryption. 

SWANS has been designed as a secure and cost effective alternative to the already existing monitoring systems in industrial companies. 
The purpose of the project is to monitor some sort of chemmical in a reservoir, gather data, parse and encrypt the data and send it to the App to be monitored. 

SWANS uses Elliptic Curve Cryptography along with the Elgamal Public Key Cryptosystem to get a symmetric key between the client and server, upon which it uses the XOR cipher for encrypting and decrypting further messages.

On the App, the user is require to add a username and a password which in this case is adminpass. On the App, the user is able to specify parameteres depending on the chemical's properties. 
These parameteres will be divided into 3 categories:
1. Green -- data is within the parameters
2. Yellow -- data is close to surpassing the paramters
3. Red -- data is out of the parameters

After having successfully received the data on the App, the user will be able to see data in real time and monitor different properties at once. If there are any errors the user will receive constant notification every 10 seconds until is fixed. 

 
Team Members:  
Haley Wichman, Team Leader  
Andrew Theodos  
Paul De Soler  
Zachary Guillot  
Alexandra Duran Chicas   
