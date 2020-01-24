from n11 import *
from n13 import *
from os import urandom

key = urandom(16)

def userdata(data):
    global key
    data = data.replace(b';', b'').replace(b'=', b'')
    data = b"comment1=cooking%20MCs;userdata=" + data + b";comment2=%20like%20a%20pound%20of%20bacon"
    return CBC_Encrypt(data, key)

def detect_admin(data):
    global key
    plain = CBC_Decrypt(data, key).split(b';')
    print("Plain: {}".format(plain))
    for pair in plain:
        admin, d = pair.split(b'=')
        if admin == b'admin':
            return True
    return False

if __name__ == '__main__':
    evil = b'*admin*true*'
    enc = bytearray(userdata(evil))
    enc[16] = enc[16] ^ ord('*') ^ ord(';') # Prev block offset ^ curr plain ^ want plain
    enc[22] = enc[22] ^ ord('*') ^ ord('=')
    enc[27] = enc[27] ^ ord('*') ^ ord(';')
    print(detect_admin(bytes(enc)))
