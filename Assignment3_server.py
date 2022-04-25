#Sophia Carlone
#Peter Lef and Evan Lira
#Cryptography assignment 3

#server side (reciever)

import time
import zmq

def encrypt(message):
    return message

def decrypt(message):
    return message


context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5555") #local (on same machine)

keys = socket.recv() #receive keys

while True: #probably have some sort of break later
    recvMessage = socket.recv()
    print(decrypt(recvMessage))

    #time.sleep(1)
    sendMessage = input()
    socket.send("%s", sendMessage)

# import socketserver
# import socket
# import sys
# import time

# s = socket.socket

# port = 40674
# s.bind("tcp://*:5555", port)

# while True:
#     message = s.recv()
#     print(message)
#     time.sleep()
#     data = "hi"
#     s.send(self, data)
