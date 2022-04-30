#Sophia Carlone
#Peter Lef and Evan Lira
#Cryptography assignment 3

#client side (client)

import socket
from pickle import loads as deserialize, dumps as serialize
import rsa
import aes

RSA_MOD_SIZES_BITS = {1024, 2048, 4096}
SOCKET_BUFSIZE_BYTES = 2048
PORT = 9999

def input_rsa_mod_size_bits():
    mod_size_str = input(f"RSA mod size ({RSA_MOD_SIZES_BITS}): ")
    while True:
        try:
            mod_size = int(mod_size_str)
            if mod_size in RSA_MOD_SIZES_BITS:
                return mod_size
            else:
                print(f"Error: mod size must be in {RSA_MOD_SIZES_BITS}")
        except ValueError:
            print("Invalid mod size. Must be an integer")
        mod_size_str = input("Try again: ")

if __name__ == "__main__":
    # generate rsa keys
    rsa_mod_size_bits = input_rsa_mod_size_bits()
    print("Generating RSA keys...")
    rsa_keys = rsa.gen_keys(rsa_mod_size_bits)
    rsa_pub_keys = {"n": rsa_keys["n"], "e": rsa_keys["e"]}

    # set up socket
    server_addr = input("Chat partner address: ")
    print("Connecting...")
    sct = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sct.connect((server_addr, PORT))
    print("Connected")

    try:
        # send rsa public keys
        sct.send(serialize(rsa_pub_keys))

        # receive and decrypt aes keys
        # we expect aes_info to be a dict({'crypted_key', 'key_size_bytes', 'crypted_seed', 'seed_size_bytes'})
        aes_info = deserialize(sct.recv(SOCKET_BUFSIZE_BYTES))
        aes_key = rsa.decrypt_to_bytes(aes_info["crypted_key"], rsa_keys, aes_info["key_size_bytes"])
        aes_seed = rsa.decrypt_to_bytes(aes_info["crypted_seed"], rsa_keys, aes_info["seed_size_bytes"])

        # set up aes cryptor
        aes_cryptor = aes.Cryptor(aes_key, aes_seed)

        # start chatting
        while True:
            send_message = bytes(input("> "), "utf-8")
            sct.send(aes_cryptor.encrypt(send_message))
            
            recv_message = sct.recv(SOCKET_BUFSIZE_BYTES)
            if recv_message == b"":
                print("Chat partner disconnected")
                break
            else: print("Chat partner: " + aes_cryptor.decrypt(recv_message).decode())
        sct.close()
    except KeyboardInterrupt:
        sct.close()
        exit()
