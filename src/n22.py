from n21 import Mersenne
from random import randint
import time

time.sleep(randint(4, 10))
m = Mersenne()
m.seed_mt(int(time.time()))
rng = m.extract_number()
time.sleep(randint(4, 10))

curr = int(time.time())
for _ in range(curr, curr - 12, -1):
    m1 = Mersenne()
    m1.seed_mt(_)
    if rng == m1.extract_number():
        print(f"{_} was the seed")
        break