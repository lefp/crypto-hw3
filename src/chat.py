from socket import socket
from aes import Cryptor
from threading import Thread
from termcolor import cprint

class Disconnect:
    def __init__(self, disconnect: bool):
        self.disconnect = disconnect

def _send_messages(sct: socket, cryptor: Cryptor, dc: Disconnect):
    try:
        while True:
            if dc.disconnect: return
            send_message = bytes(input(), "utf-8")
            sct.send(cryptor.encrypt(send_message))
    except KeyboardInterrupt:
        dc.disconnect = True
        cprint("Disconnecting...", "red", attrs=["bold"])
        return

def _recv_messages(sct: socket, sct_bufsize_bytes: int, cryptor: Cryptor, dc: Disconnect):
    while True:
        recv_message = sct.recv(sct_bufsize_bytes)
        if recv_message == b"":
            dc.disconnect = True
            cprint("Chat partner disconnected", "red", attrs=["bold"])
            return
        else: cprint("Chat partner: " + cryptor.decrypt(recv_message).decode(), "yellow")

def chat(sct: socket, sct_bufsize_bytes: int, cryptor: Cryptor):
    # passing an object allows the threads to access the inner value by reference
    # arguent passing in Python is stupid as hell
    dc = Disconnect(False)

    # daemon=True so that the thread doesn't block the program from exiting. Exiting is controlled by
    # send_messages()
    recv_thread = Thread(target=_recv_messages, args=(sct, sct_bufsize_bytes, cryptor, dc), daemon=True)
    recv_thread.start()
    _send_messages(sct, cryptor, dc)
