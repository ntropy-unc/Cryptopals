from n11 import *
from n13 import *
from n17 import pad
from os import urandom
from Crypto.Cipher import AES

key = b"flag" * 4

def userdata():
    global key
    data = b"comment1=cooking%20MCs;userdata=" + b"a" * 16
    cipher = AES.new(key, AES.MODE_CBC, key)
    return cipher.encrypt(pad(data))

def detect_error(data):
    global key
    cipher = AES.new(key, AES.MODE_CBC, key)
    plain = cipher.decrypt(data)
    for p in plain:
        if p > 127:
           return plain 
    return 'Seems all good'

if __name__ == '__main__':
    enc = bytearray(userdata())
    print(enc)
    print(detect_error(enc))
    attack = enc[:16] + bytearray(b"\x00" * 16) + enc[:16]
    mod = detect_error(attack)
    print(mod)
    p1, p3 = mod[:16], mod[32:]
    print(f"Found key: {''.join([chr(i ^ j) for i, j in zip(p1, p3)])}")

