import random
import os
from Crypto.Cipher import AES
import base64

key = os.urandom(16)

def pad(s):
    return s + (16 - len(s) % 16).to_bytes(1, 'little') * (16 - len(s) % 16)

def valid_pad(s):
    if len(s) % 16 != 0 or not s[-1]:
        return False
    return s[len(s) - s[-1]:] == s[-1: len(s)] * s[-1]

def unpad(s):
    if valid_pad(s):
        return s[:len(s) - s[-1]]
    return s

def get_data():
    with open('17.txt') as f:
        for x in range(0, random.randint(0, 9)):
            f.readline()
        plaintext = f.readline().strip('\n').encode()
    iv = os.urandom(16)
    return AES_CBC_encrypt(plaintext, iv), iv

def AES_CBC_encrypt(plaintext, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.encrypt(pad(plaintext))

def check_pad(ciphertext, iv):
    if type(ciphertext) is bytearray:
        ciphertext = bytes(ciphertext)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return valid_pad(cipher.decrypt(ciphertext))

def attack(ciphertext, iv):
    ans = bytearray()
    for level in range(len(ciphertext) // 16):
        curr = bytearray()
        block = ciphertext[16 * level: 16 * (level + 1)]
        prev = iv if level == 0 else ciphertext[16 * (level - 1): 16 * level]
        concat = bytearray(b'\x00' * 16) + block
        for byte in range(15, -1, -1):
            for guess in range(256):
                concat[byte] = guess
                if check_pad(concat, iv):
                    curr.append((16 - byte) ^ guess ^ prev[byte])
                    for last in range(16 - byte):
                        concat[16 - last - 1] = ((16 - byte + 1) ^ prev[16 - last - 1] ^ curr[last])
                    break
        ans += curr[::-1]
    return bytes(ans)

if __name__ == '__main__':
    ciphertext, iv = get_data()
    assert check_pad(ciphertext, iv) == True
    dec = attack(ciphertext, iv)
    print(f'My ans: {base64.b64decode(unpad(dec))}')

