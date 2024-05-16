from pwn import *
from Crypto.Cipher import DES
import itertools
import string
from joblib import Parallel, delayed

KEY_LEN = 6

def pad(msg):
    block_len = 8
    over = len(msg) % block_len
    pad = block_len - over
    return (msg + " " * pad).encode()

def double_decrypt(m, key1, key2):
    cipher2 = DES.new(key2, DES.MODE_ECB)
    dec_msg = cipher2.decrypt(m)

    cipher1 = DES.new(key1, DES.MODE_ECB)
    return cipher1.decrypt(dec_msg)

def all_possible_keys():
    return itertools.product(string.digits, repeat=KEY_LEN)

r = remote("mercury.picoctf.net", 33425)
r.recvline()
flag = r.recvlineS().strip()
log.info("Encrypted flag: {}".format(flag))

to_encrypt = b'a'
log.info("Trying to encrypt '{}'".format(to_encrypt))
r.sendlineafter("What data would you like to encrypt?", enhex(to_encrypt))
a_enc = r.recvlineS().strip()
print(a_enc)
log.info("Encrypted form: {}".format(a_enc))
a_enc = bytes.fromhex(a_enc)

a_padded = pad(to_encrypt.decode())

d = {}

def encrypt_with_key(k1):
    k1 = pad("".join(k1))
    cipher1 = DES.new(k1, DES.MODE_ECB)
    enc = cipher1.encrypt(a_padded)
    return enc, k1

def decrypt_with_key(k2):
    k2 = pad("".join(k2))
    cipher2 = DES.new(k2, DES.MODE_ECB)
    dec = cipher2.decrypt(a_enc)
    return dec, k2

with log.progress('Encrypting plaintext with all possible keys') as p:
    results_enc = Parallel(n_jobs=-1)(delayed(encrypt_with_key)(k1) for k1 in all_possible_keys())
    for enc, k1 in results_enc:
        d[enc] = k1

with log.progress('Decrypting ciphertext with all possible keys') as p:
    results_dec = Parallel(n_jobs=-1)(delayed(decrypt_with_key)(k2) for k2 in all_possible_keys())
    for dec, k2 in results_dec:
        if dec in d:
            k1 = d[dec]
            log.info("Found match, key1 = {}, key2 = {}".format(k1, k2))
            log.success(double_decrypt(unhex(flag), k1, k2))
            break
