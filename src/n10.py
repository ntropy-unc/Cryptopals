from base64 import b64decode
from Crypto.Cipher import AES

def ECB_Decrypt(data, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(data)

def ECB_Encrypt(data, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(data)

def padder(text, size=16):
    times = (size - len(text)) % size
    return text + bytes([times]) * times

def xor(res, plain):
    return ''.join([chr(x ^ y) for x, y in zip(res, plain)]).encode('utf-8') # Encoding is weird

def AES_Encrypt(data, key, iv=bytes([0]) * 16):
    cipher = AES.new(key, AES.MODE_ECB)
    data = padder(data)
    prev = iv
    ans = b""
    for i in range(len(data) // 16):
        block = data[i * 16:(i + 1) * 16]
        inp = xor(prev, block)
        prev = ECB_Encrypt(inp, key)
        ans += prev
    return ans

def AES_Decrypt(enc, key, iv=bytes([0]) * 16):
    cipher = AES.new(key, AES.MODE_ECB)
    assert len(enc) % 16 == 0
    prev = iv
    ans = b""
    for i in range(len(enc) // 16):
        block = enc[i * 16:(i + 1) * 16]
        inp = ECB_Decrypt(block, key)
        print(inp, prev)
        ans += xor(inp, prev)
        prev = block
    return ans

with open('7.txt') as f:
    enc = b64decode(''.join(map(lambda a: a.strip(), f.readlines())))
    print(ECB_Decrypt(enc, "YELLOW SUBMARINE"))
    assert enc == ECB_Encrypt(ECB_Decrypt(enc, "YELLOW SUBMARINE"), "YELLOW SUBMARINE")

with open('10.txt') as f:
    dec = b64decode(''.join(map(lambda a: a.strip(), f.readlines())))
    # print(dec)
    print(AES_Decrypt(dec, "YELLOW SUBMARINE"))
