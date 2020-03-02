from base64 import b64decode
from collections import Counter, OrderedDict

freq = {'e': 12.02, 't': 9.10, 'a': 8.12, 'o': 7.68,
        'i': 7.31, 'n': 6.95, 's': 6.28, 'r': 6.02,
        'h': 5.92, 'd': 4.32, 'l': 3.98, 'u': 2.88,
        'c': 2.71, 'm': 2.61, 'f': 2.30, 'y': 2.11,
        'w': 2.09, 'g': 2.03, 'p': 1.82, 'b': 1.49,
        'v': 1.11, 'k': 0.69, 'x': 0.17, 'q': 0.11,
        'j': 0.10, 'z': 0.07}

def hamming(a, b):
    assert len(a) == len(b)
    ans = 0
    for x, y in zip(a, b):
        # x = ord(x)
        # y = ord(y)
        while x or y:
            ans += (x & 1) ^ (y & 1) # Get whether last bits of x and y differ
            x >>= 1
            y >>= 1
    return ans

if __name__ == '__main__':
    print(hamming(b'this is a test', b'wokka wokka!!!'))

    with open('6.txt') as f:
        data = ''.join(map(lambda a: a.strip(), f.readlines())) # Remove newline from each line, and join lines together
        # print(data)
        data = b64decode(data)
        KEYSIZE = range(2, 41)
        
        measure = float('inf')
        sizes = dict()
        for s in KEYSIZE:
            test = sum([hamming(data[i * s:(i + 1) * s], data[(i + 1) * s:(i + 2) * s]) / s for i in range(4)]) / 4 # Get 4 average hamming values of chunks
            sizes[s] = test
        sizes = OrderedDict(sorted(sizes.items(), key=lambda kv: kv[1])) # Orders dictionary based on keys
        
        # Loop through three best sizes
        for i, size in enumerate(sizes):
            if i == 3:
                break
            res = ['a'] * len(data)
            for s in range(size):    
                curr = ''.join([chr(d) for x, d in enumerate(data) if x % size == s]) # We get every 1st char % size, 2nd char % size...
                local = float('inf')
                ans = ""
                for _ in range(256):
                    test = ''.join([chr(_ ^ ord(i)) for i in curr]).lower()
                    test1 = sum([abs(v - Counter(test)[k] / len(test)) ** 2 for k, v in freq.items()]) / len(test) # Use MSE as a metric again
                    if test1 < local:
                        ans = test
                        local = test1
                for _, a in enumerate(ans): # Insert every nth char % size back into ans
                    res[size * _ + s] = a
        
            res = ''.join(res)
            print(res)
