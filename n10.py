from n13 import *
from n11 import *
from base64 import b64decode

with open('10.txt') as f:
    data = b64decode(''.join([l.strip() for l in f.readlines()]))
    ans = CBC_Decrypt(data, b'YELLOW SUBMARINE')
    print(ans)
    assert data == CBC_Encrypt(ans, b'YELLOW SUBMARINE')
