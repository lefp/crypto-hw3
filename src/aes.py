from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers.algorithms import AES as _ALGORITHM
# CFB because a corrupted block doesn't corrupt all subsequent blocks
# also, CFB doesn't require padding
from cryptography.hazmat.primitives.ciphers.modes import CFB as _MODE
from random import getrandbits
from math import ceil
from os import urandom

KEY_SIZES_BITS = {128, 192, 256} # AES might also support 512, but not with CFB
BYTE_ORDER = 'big' # big endian. Chosen arbitrarily

def _generate_key(size: int) -> bytes:
    if size not in KEY_SIZES_BITS: raise ValueError(f"Invalid key size. Must be in {KEY_SIZES_BITS}")
    return getrandbits(size).to_bytes(ceil(size / 8), BYTE_ORDER)

def _generate_seed() -> bytes:
    return urandom(_ALGORITHM.block_size // 8)

# `bytes` objects are immutable, so we don't need to clone them for safety
class Cryptor:
    def __init__(self, key: bytes, seed: bytes):
        self._cipher = Cipher(_ALGORITHM(key), _MODE(seed))
        # saving this info for convenience
        self._key = key
        self._seed = seed
    def generate(key_size: int): # -> Cryptor
        return Cryptor(_generate_key(key_size), _generate_seed())
    
    def key(self) -> bytes:
        return self._key
    def seed(self) -> bytes:
        return self._seed
    
    def encrypt(self, message: bytes) -> bytes:
        encryptor = self._cipher.encryptor()
        return encryptor.update(message) + encryptor.finalize() # not sure how the finalize stuff works
    def decrypt(self, message: bytes) -> bytes:
        decryptor = self._cipher.decryptor()
        return decryptor.update(message) + decryptor.finalize()

# @debug everything below this line is for testing purposes

if __name__ == "__main__":
    C1 = Cryptor.generate(256)
    m = b"Hello, world!"
    c = C1.encrypt(m)

    C2 = Cryptor(C1.key(), C1.seed())
    d = C1.decrypt(c)

    print(f"m = {m}", f"c = {c}", f"d = {d}", sep="\n")