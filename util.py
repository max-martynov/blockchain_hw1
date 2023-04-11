import random
import hashlib
import os

def is_prime(n):
    i = 2
    while i * i <= n:
        if n % i == 0:
            return False
        i += 1
    return True

def find_large_prime(l, r):
    while True:
        p = random.randint(l, r)
        if is_prime(p):
            return p

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def get_hash(st):
    hash_object = hashlib.sha256()
    hash_object.update(st.encode())
    return int(hash_object.hexdigest(), 16)

def add_suffix_to_filepath(file_path, suffix):
    directory, filename = os.path.split(file_path)
    new_filename = os.path.splitext(filename)[0] + suffix + os.path.splitext(filename)[1]
    return os.path.join(directory, new_filename)

def binary_power(base, exponent, mod):
    if exponent == 0:
        return 1
    result = 1
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exponent //= 2
    return result
