rom base64 import b64decode
from Crypto.Cipher import AES

KEY = "YELLOW SUBMARINE"

with open('7.txt') as f:
    data = ''.join(map(lambda a: a.strip(), f.readlines()))
    data = b64decode(data)
    # print(data)
    cipher = AES.new(KEY, AES.MODE_ECB)
    print(cipher.decrypt(data))
