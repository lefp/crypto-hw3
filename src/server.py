#Sophia Carlone
#Peter Lef and Evan Lira
#Cryptography assignment 3

#server side (reciever)

import socket
from pickle import loads as deserialize, dumps as serialize
import rsa
import aes
from chat import chat
from termcolor import cprint

SOCKET_BUFSIZE_BYTES = 2048
PORT = 9999

def input_aes_key_size_bits():
    key_size_str = input(f"AES key size ({aes.KEY_SIZES_BITS}): ")
    while True:
        try:
            key_size = int(key_size_str)
            if key_size in aes.KEY_SIZES_BITS:
                return key_size
            else:
                print(f"Error: key size must be in {aes.KEY_SIZES_BITS}")
        except ValueError:
            print("Invalid key size. Must be an integer")
        key_size_str = input("Try again: ")

if __name__ == "__main__":
    # generate aes setup
    aes_key_size_bits = input_aes_key_size_bits()
    aes_cryptor = aes.Cryptor.generate(aes_key_size_bits)

    # set up socket
    sct = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # to prevent "Address already in use" error, which occurs if the connection is closed by the server
    # instead of the client, and then the server tries to reconnect
    sct.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sct.bind(("", PORT))
    # wait for client to connect
    print("Waiting for chat partner to connect...")
    sct.listen()
    client, add = sct.accept()
    cprint("Connected", "green", attrs=["bold"])

    try:
        # receive rsa public keys
        rsa_pub_keys = deserialize(client.recv(SOCKET_BUFSIZE_BYTES))

        # encrypt and send aes keys
        aes_info = {
            "crypted_key": rsa.encrypt_from_bytes(aes_cryptor.key(), rsa_pub_keys),
            "key_size_bytes": len(aes_cryptor.key()),
            "crypted_seed": rsa.encrypt_from_bytes(aes_cryptor.seed(), rsa_pub_keys),
            "seed_size_bytes": len(aes_cryptor.seed())
        }
        client.send(serialize(aes_info))

        # start chatting
        chat(client, SOCKET_BUFSIZE_BYTES, aes_cryptor)
    except KeyboardInterrupt:
        sct.close()
        exit()
