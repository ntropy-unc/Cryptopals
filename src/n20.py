import base64
import os
from Crypto.Cipher import AES
from n6 import freq
from collections import Counter
import numpy

def CTR(ciphertext, key, nonce=bytearray(b'\x00' * 8)):
    counter = bytearray(b'\x00' * 8) # If left as an optional parameter, it will be kept in next call.
    cipher = AES.new(key, AES.MODE_ECB)
    plain = b''

    for level in range(len(ciphertext) // 16):
        next = cipher.encrypt(bytes(nonce + counter))
        block = bytes(ciphertext[level * 16: (level + 1) * 16])
        plain += b''.join([(x ^ y).to_bytes(1, 'little') for x, y in zip(block, next)])
        counter[0] = (counter[0] + 1) % 256

    return plain

with open('20.txt') as f:
    file_lines = f.readlines()
    plains = [base64.b64decode(f.strip('\n')) for f in file_lines]
    key = os.urandom(16)
    ciphers = [CTR(p, key) for p in plains]
    truncate = len(min(ciphers, key=lambda a: len(a)))
    ciphers = [c[:truncate] for c in ciphers]

swapped = []
for x in range(truncate):
    nth = b''.join([c[x].to_bytes(1, 'little') for c in ciphers])
    score = float('inf')
    row = ''
    for y in range(256):
        test = str(b''.join([(n ^ y).to_bytes(1, 'little') for n in nth])).lower()
        curr = sum([abs(v - (Counter(test)[k] / len(test))) for k, v in freq.items()])
        curr += len([t for t in test if t not in freq])
        if curr < score:
            row = test
            score = curr
    swapped.append(row)

transpose = [[''.join([c[x] for c in swapped])] for x in range(truncate)]
print(transpose)