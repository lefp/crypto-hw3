import aes
import rsa

RSA_KEY_SIZES = {1024, 2048, 4096}

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

def input_rsa_mod_size_bits():
    # TODO implement
    # TODO include a check to ensure it's in RSA_KEY_SIZES
    return 4096 # temporary, remove this line when implementing this function

# this is a local test. We don't have a 2-party socket setup
if __name__ == "__main__":

    # RSA RECEIVER (ALICE) ----------------------------------------------------

    # generate RSA keys
    rsa_mod_size_bits = input_rsa_mod_size_bits()
    rsa_keys = rsa.gen_keys(rsa_mod_size_bits)

    # send RSA public keys
    rsa_pub_keys = {"n": rsa_keys["n"], "e": rsa_keys["e"]}
    # TODO send public keys via sockets

    # RSA SENDER (BOB) --------------------------------------------------------

    # generate AES setup
    aes_key_size_bits = input_aes_key_size_bits()
    # this object does all the AES encryption and decrytion
    aes_cryptor_bob = aes.Cryptor.generate(aes_key_size_bits)

    # receive RSA keys
    # TODO receive RSA public keys via sockets

    # send AES keys
    crypted_aes_key  = rsa.encrypt_from_bytes(aes_cryptor_bob.key(),  rsa_pub_keys)
    crypted_aes_seed = rsa.encrypt_from_bytes(aes_cryptor_bob.seed(), rsa_pub_keys)
    aes_key_size_bytes = len(aes_cryptor_bob.key())
    aes_seed_size_bytes = len(aes_cryptor_bob.seed())
    # TODO send AES key, seed, key size, and seed size via sockets

    # RSA RECEIVER (ALICE) ----------------------------------------------------

    # receive AES keys
    # TODO receive AES keys via sockets
    aes_key  = rsa.decrypt_to_bytes(crypted_aes_key,  rsa_keys, aes_key_size_bytes )
    aes_seed = rsa.decrypt_to_bytes(crypted_aes_seed, rsa_keys, aes_seed_size_bytes)
    aes_cryptor_alice = aes.Cryptor(aes_key, aes_seed)

    # CHAT TEST ---------------------------------------------------------------
    # at this point all setup should be complete

    # alice
    m1 = b"Hey, Bob"
    c1 = aes_cryptor_alice.encrypt(m1)

    # bob
    d1 = aes_cryptor_bob.decrypt(c1)
    assert(d1 == m1) # @debug
    m2 = b"What's up, Alice?"
    c2 = aes_cryptor_bob.encrypt(m2)

    # alice
    d2 = aes_cryptor_alice.decrypt(c2)
    assert(d2 == m2) # @debug

    print("Test passed!")