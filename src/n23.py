u, d = 11, 0xffffffff
s, b = 7, 0x9d2c5680
# t, c = 15, 0xefc60000
t, c = 4, 1742044
l = 18
n = 624
mask = 0xffffffff

def temper(y):
    y ^= ((y >> u) & d)
    y ^= ((y << s) & b)
    y ^= ((y << t) & c)
    y ^= (y >> l)
    return y

def untemper(y):
    y = t4(y)
    return y

def s3(y):
    return y ^ ((y << t) & c)

def t3(y):
    ans = 0
    return ans

print(s3(7387))
print(t3(s3(7387)))

def numberBits(y):
    ctr = 0
    while y:
        y >>= 1
        ctr += 1
    return ctr

def t4(y):
    # Beginning l bits of ans must be xored by 0, a result of y >> l
    # Next l bits can be xored by a reconstruction of those beginning ans bits
    nb = numberBits(y)
    ans = 0
    for x in range(nb):
        if x < l:
            ans = ans | (((y >> (nb - 1 - x)) & 1) ^ 0)
        else:
            ans = ans | (((y >> (nb - 1 - x)) & 1) ^ ((ans >> l) & 1))
        ans <<= 1
    return ans >> 1