from n21 import Mersenne
import random
import os
import time

def mt_stream(plain, seed):
    m = Mersenne()
    m.seed_mt(seed)
    out = b""
    for p in plain:
        keystream = m.extract_number() & 0xff # Grab last 8 bits
        out += (p ^ keystream).to_bytes(1, 'little')
    return out

if __name__ == '__main__':
    seed = random.randint(1, 65535)
    cip = mt_stream(b"asdfaewfasdf", seed)
    assert mt_stream(cip, seed) == b"asdfaewfasdf"

    seed = random.randint(1, 128) # Cheat for lesser bits (7 bits)
    plain = os.urandom(random.randint(1, 16)) + b'A' * 14
    cip = mt_stream(plain, seed)
    for guess in range(1, 129):
        pg = mt_stream(cip, guess) # plain guess
        if pg[-14:] == b'A' * 14:
            print(f"{seed} == {guess}. Did we guess right?")
            break
    
    plain = os.urandom(32)
    seed = int(time.time())
    token = mt_stream(plain, seed)
    time.sleep(5)
    now = int(time.time())
    for guess in range(now, now - 15, -1):
        pg = mt_stream(token, guess)
        if pg == plain:
            print(f"Token found. Seed is {guess}")