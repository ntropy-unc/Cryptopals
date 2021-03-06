from binascii import unhexlify
from collections import Counter

inp = b"1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
inp = unhexlify(inp)
print(inp)

freq = {'e': 12.02, 't': 9.10, 'a': 8.12, 'o': 7.68,
        'i': 7.31, 'n': 6.95, 's': 6.28, 'r': 6.02,
        'h': 5.92, 'd': 4.32, 'l': 3.98, 'u': 2.88,
        'c': 2.71, 'm': 2.61, 'f': 2.30, 'y': 2.11,
        'w': 2.09, 'g': 2.03, 'p': 1.82, 'b': 1.49,
        'v': 1.11, 'k': 0.69, 'x': 0.17, 'q': 0.11,
        'j': 0.10, 'z': 0.07}

ans = ""
score = float('inf')

for _ in range(60, 100):
    test = ''.join([chr(_ ^ i) for i in inp]).lower() # Grab XORed result like from previous exercise
    test1 = sum([abs(v - Counter(test)[k] / len(test)) for k, v in freq.items()])
    if test1 < score:
        ans = test
        score = test1

print(ans)
