from n21 import Mersenne
import time

u, d = 11, 0xffffffff
s, b = 7, 0x9d2c5680
t, c = 15, 0xefc60000
l = 18
n = 624
mask = 0xffffffff

def temper(y):
    y ^= ((y >> u) & d)
    y ^= ((y << s) & b)
    y ^= ((y << t) & c)
    y ^= (y >> l)
    return y

def numberBits(y):
    ctr = 0
    while y:
        y >>= 1
        ctr += 1
    return ctr

def t1(y, rs, ad):
    # General case of t4, solved separately
    nb = numberBits(y)
    ans = 0
    for x in range(nb):
        if x < rs:
            ans = ans | (((y >> (nb - 1 - x)) & 1) ^ 0)
        else:
            ysb = (ans >> rs) & 1 # y shifted bit
            cp = ((ad >> (nb - 1 - x)) & 1) & ysb # c prime pit
            ans = ans | (cp ^ ((y >> (nb - 1 - x)) & 1))
        ans <<= 1
    return ans >> 1

def t3(y, ls, ad):
    # ls = left shifter
    # ad = ander
    ans = 0xffffffff
    for x in range(32):
        if x < ls:
            test = (y & 1) ^ 0
        else:
            ysb = (ans >> (x - ls)) & 1 # y shifted bit, with offset of ls due to right shift
            cp = ((ad >> x) & 1) & ysb # c prime; ad & ysb = cp
            test = (y & 1) ^ cp # cp ^ ans = y
        if ((ans >> x) & 1) != test:
            ans ^= (1 << x)
        y >>= 1
    return ans

def t4(y):
    # Special case of t1, solved separately
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

def untemper(y):
    y = t4(y)
    y = t3(y, t, c)
    y = t3(y, s, b)
    y = t1(y, u, d)
    return y

if __name__ == '__main__':
    m = Mersenne()
    m.seed_mt(int(time.time()))
    outputs = [m.extract_number() for _ in range(624)]
    state = [untemper(o) for o in outputs]
    m1 = Mersenne()
    m1.seed_mt(69)
    m1.MT = state
    m1.index = 0
    assert m1.MT == state
    for _ in range(624):
        pred = m1.extract_number()
        if outputs[_] != pred:
            print(f"{pred} != {outputs[_]}")
    print("Did I successfully guess everything?")