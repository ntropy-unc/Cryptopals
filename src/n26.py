from Crypto.Cipher import AES
import os

key = os.urandom(16)
end = ";comment2=%20like%20a%20pound%20of%20bacon"
evil = b";admin=true;"

def get(inp):
    prep = "comment1=cooking%20MCs;userdata="
    data = (prep + inp + end).replace(";", "\";\"").replace("=", "\"=\"")
    return ctr(bytearray(data.encode('utf-8')))

def ctr(data):
    cipher = AES.new(key, AES.MODE_CTR, nonce=b"\x00"*8, initial_value=b"\x00"*8)
    return cipher.encrypt(data)

def admin(inp):
    inp = ctr(inp)
    return inp.find(evil) != -1

if __name__ == '__main__':
    assert admin(get("hair")) == False
    intercepted = bytearray(get("hair"))
    for i in range(-12, 0):
        intercepted[i] ^= ord(end[i]) ^ evil[i]
    print(admin(intercepted))
