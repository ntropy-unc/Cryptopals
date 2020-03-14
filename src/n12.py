from n11 import *
from base64 import b64decode

key = urandom(16)
unk = b64decode(b'Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK')

def get_block():
    global key
    curr = len(oracle(b'A'))
    for i in range(2, 100):
        test = oracle(b'A' * i)
        # assert guess(test) == "ECB"
        if len(test) != curr:
            return len(test) - curr

def oracle(msg):
    global unk, key
    return ECB_Encrypt(msg + unk, key)

def locate_hidden(block_size):
    out = b''
    length = len(oracle(b''))
    for i in range(length // block_size):
        for j in range(1, block_size + 1):
            test = b'A' * (block_size - j) + out
            ans = oracle(b'A' * (block_size - j))[i * block_size:(i + 1) * block_size]
            for b in range(256):
                if oracle(test + bytes([b]))[i * block_size:(i + 1) * block_size] == ans:
                    out += bytes([b])
                    break
    return out

if __name__ == '__main__':
    block_size = get_block()
    assert block_size == 16
    print(locate_hidden(block_size))
