#Sophia Carlone
#Peter Lef and Evan Lira
#Cryptography assignment 3

#client side (client)
import zmq

def encrypt(message):
    return message

def decrypt(message):
    return message

context = zmq.Context()

#  Socket to talk to server
print("Connecting to server…")
socket = context.socket(zmq.SUB)
socket.setsockopt(zmq.SUBSCRIBE) #is this needed 
socket.connect("tcp://localhost:5555")

keys = 1, 2

socket.send(keys)
while True:
    sendMessage = input()
    sendMessage = encrypt(sendMessage)
    socket.send("%s", sendMessage)

    recvMessage = socket.recv()
    print(decrypt(recvMessage))
    


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