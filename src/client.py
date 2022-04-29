#Sophia Carlone
#Peter Lef and Evan Lira
#Cryptography assignment 3

#client side (client)
import socket

def encrypt(message):
    return message

def decrypt(message):
    return message

keys = 1
bufsize = 1024
# hostname = 127.0.0.1

sct=socket.socket(socket.AF_INET, socket.SOCK_STREAM) #creating the socket
sct.connect(("127.0.0.1", 9999)) 

sct.send(bytes(keys))

while True:
    #sct.recv(1024).decode()
    sendMessage = input()
    sct.send(bytes(encrypt(sendMessage),'utf-8')) #sending the TCP message
    
    recvMessage = sct.recv(bufsize)
    print(decrypt(recvMessage))
sct.close()


######################################################################3
# import zmq

# def encrypt(message):
#     return message

# def decrypt(message):
#     return message

# context = zmq.Context()

# #  Socket to talk to server
# print("Connecting to server…")
# socket = context.socket(zmq.SUB)
# socket.setsockopt(zmq.SUBSCRIBE) #is this needed 
# socket.connect("tcp://localhost:5555")

# keys = 1, 2

# socket.send(keys)
# while True:
#     sendMessage = input()
#     sendMessage = encrypt(sendMessage)
#     socket.send("%s", sendMessage)

#     recvMessage = socket.recv()
#     print(decrypt(recvMessage))



# for request in range(10):
#     print("Sending request %s …" % request)
#     socket.send(b"Hello")

#     message = socket.recv()
#     print("Received reply %s [ %s ]" % (request, message))




# import socket

# s = socket.socket()
  
# port = 40674
  
# # connect to the server on local computer
# s.connect(('127.0.0.1', port))
  
# # receive data from the server
# print(s.recv(1024))
  
# # close the connection
# s.close()