from n28 import *
import struct

def sha_pad(data, exist=0):
    mbl = exist + len(data) # message_byte_len
    pad = b'\x80'
    pad += b'\x00' * (((56 - (mbl+1)) % 64) % 64)
    pad += struct.pack(b'>Q', mbl * 8)
    return pad

if __name__ == '__main__':
    normal = b"comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon"
    evil = b";admin=true"
    given = auth(normal)
    states = (int(given[:8], 16), int(given[8:16], 16), int(given[16:24], 16), int(given[24:32], 16), int(given[32:], 16))

    for keylen in range(100):
        given = sha_pad(normal, exist=keylen)
        ans = auth(normal + given + evil)
        
        msg = evil
        mbl = keylen + len(normal) + len(given)
        msg += sha_pad(msg, exist=mbl)
        h = process_chunk(msg[:64], *states)
        guess = '%08x%08x%08x%08x%08x' % h
        
        print(f"{keylen}  {ans} {guess}")

        if ans == guess:
            print(f"Key length is {keylen} and the correct hash is {guess}")
            break
