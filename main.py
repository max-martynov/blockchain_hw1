import random
from util import find_large_prime, modinv, get_hash, add_suffix_to_filepath, binary_power, egcd
import argparse
import os

PRIME_L_BOUND = 1e9
PRIME_R_BOUND = 1e10

def generate_keypair():
    p = find_large_prime(PRIME_L_BOUND, (PRIME_L_BOUND + PRIME_R_BOUND) / 2)
    q = find_large_prime((PRIME_L_BOUND + PRIME_R_BOUND) / 2, PRIME_R_BOUND)
    n = p * q
    phi = (p-1) * (q-1)
    e = random.randint(3, phi - 1)
    g = egcd(e, phi)[0]
    while g != 1:
        e = random.randrange(3, phi - 1)
        g = egcd(e, phi)[0]
    d = modinv(e, phi)
    return (e, n, d)

def process_generate(dir):
    keypair = generate_keypair()
    public_key_file = os.path.join(dir, 'key.pub')
    os.makedirs(os.path.dirname(public_key_file), exist_ok=True)
    with open(public_key_file, 'w') as f:
        f.write(str(keypair[0]) + ',' + str(keypair[1]))
    private_key_file = os.path.join(dir, 'key')
    os.makedirs(os.path.dirname(private_key_file), exist_ok=True)
    with open(private_key_file, 'w') as f:
        f.write(str(keypair[2]) + ',' + str(keypair[1]))

def process_sign(private_key_file, text_file):
    with open(private_key_file, 'r') as f:
        line = f.readline().strip()
        d, n = map(int, line.split(','))
        with open(text_file, 'r') as g:
            text = g.read()
            hash = get_hash(text) % n
            hash_encrypt = binary_power(hash, d, n)
            signed_file = add_suffix_to_filepath(text_file, '_signed')
            with open(signed_file, 'w') as w:
                w.write(text + '#' + hex(hash_encrypt))

def process_verify(public_key_file, signed_file):
    with open(public_key_file, 'r') as f:
        line = f.readline().strip()
        e, n = map(int, line.split(','))
        with open(signed_file, 'r') as g:
            parts = g.read().rsplit('#', 1)
            text = parts[0]
            hash_orig = get_hash(text) % n
            hash_hex = parts[1]
            if hash_orig == binary_power(int(hash_hex, 16), e, n):
                print('Verification complete :)')
                verified_file = add_suffix_to_filepath(signed_file, '_verified')
                with open(verified_file, 'w') as w:
                    w.write(text)
            else:
                print('Bad signature :(')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', type=str, help='generate, sign or verify')
    parser.add_argument('keypair_file', type=str, help='directory to store generated keys or file with already generated key')
    parser.add_argument('text_file', nargs='?', default=None, type=str, help='text file to sign/verify')
    args = parser.parse_args()
    if args.mode == 'generate':
        process_generate(args.keypair_file)
    elif args.mode == 'sign':
        process_sign(args.keypair_file, args.text_file)
    elif args.mode == 'verify':
        process_verify(args.keypair_file, args.text_file)

if __name__ == "__main__":
    main()