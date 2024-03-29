#Creating an RSA setup
import random

_SANITY_CHECKS = False

_BYTE_ORDER = "big" # endian
_DEFAULT_SALT_LEN = 8 # abitrarily chosen

#returns [d, x, y] for a >= b where d = gcd(a,b) = ax + by
def _pulverizer(a,b):
	x1 = 1
	y1 = 0
	x2 = 0
	y2 = 1
	while b != 0:
		q = a//b
		r = a % b
		new_x1 = x2
		new_y1 = y2
		new_x2 = x1 - q*x2
		new_y2 = y1 - q*y2
		a = b
		b = r
		x1 = new_x1
		y1 = new_y1
		x2 = new_x2
		y2 = new_y2
	return [a, x1, y1]

#modular exponentiation for Miller Rabin
def _special_expmod(a,b,m):
	if b == 0:
		return 1
	elif b % 2 == 0:
		y = _special_expmod(a,b//2,m)
		z = pow(y,2,m)
		if z == 1 and y!= 1 and y != -1 and y != (m-1): #since  m-1 = -1 mod p so (m-1)^2 = 1 mod p
			return 0
		else:
			return z
	else:
		y = _special_expmod(a,b-1,m) #if b is prime y will return as 1
		return pow(a*y,1,m)

#Miller-Rabin test
def _isprime(m,iterations):
	while iterations > 0:
		k = random.randrange(1,m)
		if pow(k,m,m) != k:
			return False
		iterations -= 1
	return True

def gen_keys(bit_length, confidence=None):
	# confidence is the number of iterations for the Miller-Rabin test
	if confidence is None: confidence = 100

	# bit lengths of p and q are half the bit length of n
	if bit_length % 2 != 0: raise ValueError("Bit length must be even")
	lower = pow(2, bit_length // 2 - 1) # 0b1000...0000
	upper = pow(2, bit_length // 2) - 1 # 0b1111...1111
	while True:
		p = random.randrange(lower,upper)
		if _isprime(p,confidence):
			break
	while True:
		q = random.randrange(lower,upper)
		if _isprime(q,confidence) and q != p:
			break

	if _SANITY_CHECKS: print("p = ", p)
	if _SANITY_CHECKS: print("q = ", q)

	n = p*q
	phi = (p-1)*(q-1)

	if _SANITY_CHECKS: print("n = ",n)
	if _SANITY_CHECKS: print("phi = ",phi)

	e = 3
	result = _pulverizer(phi,e)
	while result[0] != 1: #since 3 will not be coprime with every phi, but it will always be odd
		e += 2
		result = _pulverizer(phi,e)
	d = result[2]
	while d < 0:
		d += phi

	if _SANITY_CHECKS: print("e = ", e)
	if _SANITY_CHECKS: print("d = ", d)

	check = pow(e*d,1,phi)
	if check == 1:
		if _SANITY_CHECKS: print("Passed sanity check")
		if _SANITY_CHECKS: print(e,"*",d,"=",check)
	else:
		if _SANITY_CHECKS: print("Sanity check:you are insane")
		if _SANITY_CHECKS: print(e,"*",d,"=",check)
	return {"n": n, "p": p, "q": q, "phi": phi, "e": e, "d": d}

def decrypt_int(ciphertext: int,d,n,salt_length) -> int:
	salted_m = pow(int(ciphertext),int(d),int(n))
	return salted_m >> salt_length

def encrypt_int(message: int,e,n,salt_length) -> int:
	lower = pow(2, salt_length-1)
	upper = pow(2, salt_length)- 1
	salt = random.randrange(lower,upper)

	message = message << salt_length
	message += salt
	# We haven't implemented a mechanism to guarantee that the salted message is less than n. For this program
	# it should be fine, since the AES key and seed together are probably under 1024, so we'll just enforce a
	# minimum of 1024 bits for RSA (which is the standard minimum anyway; 512 is insecure). If one of y'all
	# wants to fix this so that it's less jank, feel free, but I don't think it's worth the effort for this
	# assignment.
	if message >= n:
		raise RuntimeError("Salted message too large")

	return pow(int(message),int(e),int(n))

def encrypt_from_bytes(message: bytes, pub_keys: dict, salt_len=_DEFAULT_SALT_LEN) -> int:
	return encrypt_int(int.from_bytes(message, _BYTE_ORDER), pub_keys["e"], pub_keys["n"], salt_len)

def decrypt_to_bytes(ciphertext: int, keys: dict, message_len: int, salt_len=_DEFAULT_SALT_LEN) -> bytes:
	return decrypt_int(ciphertext, keys["d"], keys["n"], salt_len).to_bytes(message_len, _BYTE_ORDER)
