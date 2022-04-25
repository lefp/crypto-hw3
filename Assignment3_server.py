#Sophia Carlone
#Peter Lef and Evan Lira
#Cryptography assignment 3

#server side (reciever)

import socketserver
import socket
import sys
import time

def encrypt(message):
    return message

def decrypt(message):
    return message

bufsize = 1024 #will probably change this later

sct=socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creating the socket 
sct.bind(("127.0.0.1",9999)) #I can make this 6969 if we want to be that childish

sct.listen() #keep your ears open bois

client,add=sct.accept()

keys = client.recv(bufsize)

while True: #probably have some sort of break later
    recvMessage = sct.recv(bufsize)
    print(decrypt(recvMessage))

    #time.sleep(1)
    sendMessage = input()
    sct.send(bytes(sendMessage,'utf-8'))
sct.close()#will have to place when to do this later




######################################################################################3
# while True:
#     message = s.recv()
#     print(message)
#     time.sleep()
#     data = "hi"
#     s.send(self, data)


# import time
# import zmq

# def encrypt(message):
#     return message

# def decrypt(message):
#     return message


# context = zmq.Context()
# socket = context.socket(zmq.PUB)
# socket.bind("tcp://*:5555") #local (on same machine)

# keys = socket.recv() #receive keys

# while True: #probably have some sort of break later
#     recvMessage = socket.recv()
#     print(decrypt(recvMessage))

#     #time.sleep(1)
#     sendMessage = input()
#     socket.send("%s", sendMessage)