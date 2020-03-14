from n20 import CTR
import base64
import os

key = os.urandom(16)

def edit(ciphertext, offset, newtext):
    if offset > len(ciphertext):
        return ciphertext
    plain = CTR(ciphertext, key)
    newtext = plain[:offset] + newtext + plain[offset + len(newtext):]
    return CTR(newtext, key)

if __name__ == '__main__':
    with open('25.txt') as f:
        file_lines = f.readlines()
        plains = [base64.b64decode(f.strip('\n')) for f in file_lines]
        ciphers = [CTR(p, key) for p in plains]
        for i, cipher in enumerate(ciphers):
            print(edit(cipher, 0, cipher) == plains[i])