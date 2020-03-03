class Mersenne:
    def __init__(self):
        self.w, self.n, self.m, self.r = 32, 624, 397, 31
        self.a = 0x9908b0df
        self.u, self.d = 11, 0xffffffff
        self.s, self.b = 7, 0x9d2c5680
        self.t, self.c = 15, 0xefc60000
        self.l = 18
        self.f = 1812433253

        self.MT = [None] * self.n
        self.index = self.n + 1
        self.lower_mask = (1 << self.r) - 1
        self.mask = 0xffffffff
        self.upper_mask = (~self.lower_mask) & self.mask

    def seed_mt(self, seed):
        # Initializes generator, self.MT, from seed
        self.index = self.n
        self.MT[0] = seed
        for i in range(1, self.n):
            self.MT[i] = (self.f * (self.MT[i - 1] ^ (self.MT[i - 1] >> (self.w - 2))) + i) & self.mask

    def twist(self):
        # Generate next n values from series x_i
        for i in range(self.n):
            x = (self.MT[i] & self.upper_mask) + (self.MT[(i + 1) % self.n] & self.lower_mask)
            xA = x >> 1
            if x % 2 != 0:
                xA = xA ^ self.a
            self.MT[i] = self.MT[(i + self.m) % self.n] ^ xA
        self.index = 0

    def extract_number(self):
        # Extracts a tempered value from self.MT[index]
        # calling twist() every n numbers generated
        if self.index >= self.n:
            if self.index > self.n:
                raise Exception("Generator not seeded")
            self.twist()
        
        y = self.MT[self.index]
        y = y ^ ((y >> self.u) & self.d)
        y = y ^ ((y << self.s) & self.b)
        y = y ^ ((y << self.t) & self.c)
        y = y ^ (y >> self.l)
        self.index = (self.index + 1) % self.n

        return y & self.mask

if __name__ == '__main__':
    m = Mersenne()
    m.seed_mt(69)
    print(m.extract_number())