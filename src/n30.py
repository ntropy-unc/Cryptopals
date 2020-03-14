# https://raw.githubusercontent.com/FiloSottile/crypto.py/master/3/md4.py

import struct
import binascii

lrot = lambda x, n: (x << n) | (x >> (32 - n))


class MD4():

    A, B, C, D = (0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476)

    _F = lambda self, x, y, z: ((x & y) | (~x & z))
    _G = lambda self, x, y, z: ((x & y) | (x & z) | (y & z))
    _H = lambda self, x, y, z: (x ^ y ^ z)

    def __init__(self, message):
        length = struct.pack('<Q', len(message) * 8)
        while len(message) > 64:
            self._handle(message[:64])
            message = message[64:]
        message += b'\x80'
        message += bytes((56 - len(message) % 64) % 64)
        message += length
        while len(message):
            self._handle(message[:64])
            message = message[64:]
    
    def _handle(self, chunk):
        X = list(struct.unpack('<' + 'I' * 16, chunk))
        A, B, C, D = self.A, self.B, self.C, self.D

        for i in range(16):
            k = i
            if i % 4 == 0:
                A = lrot((A + self._F(B, C, D) + X[k]) & 0xffffffff, 3)
            elif i % 4 == 1:
                D = lrot((D + self._F(A, B, C) + X[k]) & 0xffffffff, 7)
            elif i % 4 == 2:
                C = lrot((C + self._F(D, A, B) + X[k]) & 0xffffffff, 11)
            elif i % 4 == 3:
                B = lrot((B + self._F(C, D, A) + X[k]) & 0xffffffff, 19)

        for i in range(16):
            k = (i // 4) + (i % 4) * 4
            if i % 4 == 0:
                A = lrot((A + self._G(B, C, D) + X[k] + 0x5a827999) & 0xffffffff, 3)
            elif i % 4 == 1:
                D = lrot((D + self._G(A, B, C) + X[k] + 0x5a827999) & 0xffffffff, 5)
            elif i % 4 == 2:
                C = lrot((C + self._G(D, A, B) + X[k] + 0x5a827999) & 0xffffffff, 9)
            elif i % 4 == 3:
                B = lrot((B + self._G(C, D, A) + X[k] + 0x5a827999) & 0xffffffff, 13)

        order = [0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15]
        for i in range(16):
            k = order[i]
            if i % 4 == 0:
                A = lrot((A + self._H(B, C, D) + X[k] + 0x6ed9eba1) & 0xffffffff, 3)
            elif i % 4 == 1:
                D = lrot((D + self._H(A, B, C) + X[k] + 0x6ed9eba1) & 0xffffffff, 9)
            elif i % 4 == 2:
                C = lrot((C + self._H(D, A, B) + X[k] + 0x6ed9eba1) & 0xffffffff, 11)
            elif i % 4 == 3:
                B = lrot((B + self._H(C, D, A) + X[k] + 0x6ed9eba1) & 0xffffffff, 15)

        self.A = (self.A + A) & 0xffffffff
        self.B = (self.B + B) & 0xffffffff
        self.C = (self.C + C) & 0xffffffff
        self.D = (self.D + D) & 0xffffffff

    def digest(self):
        return struct.pack('<IIII', self.A, self.B, self.C, self.D)

    def hexdigest(self):
        return binascii.hexlify(self.digest()).decode()

class SpecialMD4(MD4):
    def __init__(self, pre, message, A, B, C, D): # Pad already considered
        self.A = A
        self.B = B
        self.C = C
        self.D = D
        while len(message) > 64:
            self._handle(message[:64])
            message = message[64:]
        combined = len(message) + len(pre)
        length = struct.pack('<Q', combined * 8)
        message += b'\x80'
        message += bytes((56 - combined % 64) % 64)
        message += length
        while len(message):
            self._handle(message[:64])
            message = message[64:]

key = b'goodkey'

def auth(msg):
    m = MD4(key + msg)
    return m.hexdigest()

def md4_pad(message, exist=0):
    length = len(message) + exist
    pad = b'\x80'
    pad += bytes((56 - length % 64) % 64)
    pad += struct.pack('<Q', length * 8)
    return pad

if __name__ == '__main__':
    normal = b"comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon"
    evil = b";admin=true"
    given = auth(normal)
    A, B, C, D = int(given[:8], 16), int(given[8:16], 16), int(given[16:24], 16), int(given[24:], 16)
    
    # Not sure why this doesnt work but should be same idea as n29
    for keylen in range(10):
        glue = md4_pad(normal, exist=keylen)
        ans = auth(normal + glue + evil)
        
        m = SpecialMD4(normal + b'a' * keylen + glue, evil, A, B, C, D)
        guess = m.hexdigest()
        
        print(f"{keylen}  {ans} {guess}")

        if ans == guess:
            print(f"Key length is {keylen} and the correct hash is {guess}")
            break
