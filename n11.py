from os import urandom
from Crypto.Cipher import AES
from random import randint

def ECB_Encrypt(data, key):
    data = pad(data)
    return AES.new(key, AES.MODE_ECB).encrypt(data)

def CBC_Encrypt(data, key, iv=b"\x00" * 16):
    data = pad(data)
    res = b''
    for block in range(len(data) // 16):
        feed = b''.join([bytes([i ^ d]) for i, d in zip(iv, data[block * 16:(block + 1) * 16])])
        iv = ECB_Encrypt(feed, key)
        res += iv
    return res

def pad(data, l=16):
    n = (l - len(data)) % l
    return data + bytes([n]) * n

def guess(data):
    assert len(data) % 16 == 0
    check = set()
    for b in range(len(data) // 16):
        if data[b * 16:(b + 1) * 16] in check:
            return "ECB"
        check.add(data[b * 16:(b + 1) * 16])
    return "CBC"

if __name__ == '__main__':
    corr, n = 0, 5000
    for _ in range(n):
        key = urandom(16)
        plain = b'B' * 50
        plain = urandom(randint(5, 10)) + plain + urandom(randint(5, 10))
        ans = "ECB" if randint(1, 2) == 1 else "CBC"
        enc = CBC_Encrypt(plain, key) if ans == "CBC" else ECB_Encrypt(plain, key)
        if guess(enc) == ans:
            corr += 1
    print("Percent correct: {}".format((corr / n) * 100))

