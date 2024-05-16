import string

LOWERCASE_OFFSET = ord("a")
ALPHABET = string.ascii_lowercase[:16]

def b16_decode(enc):
    plain = ""
    for i in range(0, len(enc), 2):
        chunk = enc[i:i+2]
        binary = ""
        for c in chunk:
            binary += "{0:04b}".format(ALPHABET.index(c))
        plain += chr(int(binary, 2))
    return plain

def shift_decrypt(c, k):
    t1 = ALPHABET.index(c)
    t2 = ord(k) - LOWERCASE_OFFSET
    return ALPHABET[(t1 - t2) % len(ALPHABET)]

def decrypt(enc, key):
    plain_b16 = ""
    for i, c in enumerate(enc):
        plain_b16 += shift_decrypt(c, key[i % len(key)])
    return b16_decode(plain_b16)

# Encrypted message
enc_message = "mlnklfnknljflfmhjimkmhjhmljhjomhmmjkjpmmjmjkjpjojgjmjpjojojnjojmmkmlmijimhjmmj"

# Try all keys
for possible_key in ALPHABET:
    decrypted_message = decrypt(enc_message, possible_key)
    print(f"Key: {possible_key}, Decrypted message: {decrypted_message}")
