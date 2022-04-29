#Sophia Carlone
#Peter Lef and Evan Lira
#Cryptography assignment 3

#server side (reciever)

import socket
from pickle import loads as deserialize, dumps as serialize
import rsa
import aes

SOCKET_BUFSIZE_BYTES = 2048

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
    sct.bind(("127.0.0.1", 9999))
    # wait for client to connect
    print("Waiting for chat partner to connect...")
    sct.listen()
    client, add = sct.accept()
    print("Connected")

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
        while True:
            recv_message = client.recv(SOCKET_BUFSIZE_BYTES)
            if recv_message == b"":
                print("Chat partner disconnected")
                break
            else: print("Chat partner: " + aes_cryptor.decrypt(recv_message).decode())

            send_message = bytes(input("> "),"utf-8")
            client.send(aes_cryptor.encrypt(send_message))
        sct.close()
    except KeyboardInterrupt:
        sct.close()
        exit()
