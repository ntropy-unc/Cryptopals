from binascii import hexlify

plain = b'''Burning 'em, if you ain't quick and nimble
I go crazy when I hear a cymbal'''
key = b'ICE'

def encrypt(msg):
    ans = ''
    for i, p in enumerate(msg):
        ans += chr(p ^ key[i % len(key)])
    return ans

print(hexlify(bytes(encrypt(plain).encode())))
