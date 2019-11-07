from binascii import unhexlify
from collections import Counter

freq = {'e': 12.02, 't': 9.10, 'a': 8.12, 'o': 7.68,
        'i': 7.31, 'n': 6.95, 's': 6.28, 'r': 6.02,
        'h': 5.92, 'd': 4.32, 'l': 3.98, 'u': 2.88,
        'c': 2.71, 'm': 2.61, 'f': 2.30, 'y': 2.11,
        'w': 2.09, 'g': 2.03, 'p': 1.82, 'b': 1.49,
        'v': 1.11, 'k': 0.69, 'x': 0.17, 'q': 0.11,
        'j': 0.10, 'z': 0.07}
score = float('inf')
best = ""

with open('4.txt') as f:
    for l in f.readlines():
        line = unhexlify(l.strip())
        local = float('inf')
        lans = ""
        for _ in range(40, 100):
            test = ''.join([chr(_ ^ i) for i in line]).lower()
            test1 = sum([abs(v - Counter(test)[k] / len(test)) ** 2 for k, v in freq.items()]) / len(test) # MSE
            if test1 < local:
                lans = test
                local = test1
        if local < score:
            score = local
            best = lans

print(best)
