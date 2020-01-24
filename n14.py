from n12 import *
from n13 import ECB_Decrypt, CBC_Decrypt
from random import randint
from os import urandom

pre = urandom(randint(1, 50))

def pre_oracle(msg):
    return oracle(pre + msg)

def get_msg():
    start = pre_oracle(b'A' * 64)
    check, ans = set(), b''
    for x in range(len(start) // 16):
        b = start[x * 16:(x + 1) * 16]
        if b in check:
            ans = b
            break
        check.add(b)

    loc = offset = -1
    for x in range(64, -1, -1):
        data = pre_oracle(b'A' * x)
        if ans not in data:
            offset = x + 1
            break
        else:
            loc = data.find(ans)

    pure = pre_oracle(b'A' * offset)[loc + 16:]
    out = b''
    length = len(pure)
    for i in range(length // 16):
        for j in range(1, 17):
            test = b'A' * (16 - j) + out
            ans = pre_oracle(b'A' * (offset + 16 - j))[loc + 16:][i * 16:(i + 1) * 16]
            for b in range(256):
                if pre_oracle(b'A' * (offset) + test + bytes([b]))[loc + 16:][i * 16:(i + 1) * 16] == ans:
                    out += bytes([b])
                    break
    return out

if __name__ == '__main__':
    print(get_msg())
