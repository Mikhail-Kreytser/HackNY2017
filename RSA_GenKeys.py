import sys
from random import randint
from collections import namedtuple

prime_low_bound = 61
prime_high_bound = 192
key_bound = 31
max_input_message = prime_low_bound * prime_low_bound - 1
RSAKeys = namedtuple("RSAKeys", "enc dec cy")


# Testing whether a number is prime
def test_prime(n):
    t_f = True
    for i in range(2, n, +1):
        if n % i == 0:
            t_f = False
    return t_f


# Randomly generate a prime number roughly in the range of
#   [PRIME_LOW_BOUND, RPIME_HIGH_BOUND).
def gen_prime():
    n = randint(0, prime_high_bound - prime_low_bound) + prime_low_bound
    if n % 2 == 0:
        n -= 1
    while not test_prime(n):
        n -= 2
    return n


# Find the greatest common divisor (gcd) of two positive numbers
def gcd(n1, n2):
    if n1 >= n2:
        greater = n1
        smaller = n2
    else:
        greater = n2
        smaller = n1
    divisor = smaller
    while not(greater % smaller == 0):
        divisor = greater % smaller
        greater = smaller
        smaller = divisor
    return divisor


# Randomly generate a positive integer that is coprime to the given
#   positive integer n and approximately in the range of [KEY_LOW_BOUND, n).
def gen_coprime(n):
    coprime = randint(0, n - key_bound) + key_bound
    if n % 2 == 0:
        if coprime % 2 == 0:
            coprime -= 1
        while not(gcd(n, coprime) == 1):
            coprime -= 2
    else:
        while not (gcd(n, coprime) == 1):
            coprime -= 1
    return coprime


# Generate a public-private key pair and the corresponding modulus cipher.
def gen_keys():
    p = gen_prime()
    q = gen_prime()
    while p == q:
        p = gen_prime()
        q = gen_prime()
    t = (p - 1) * (q - 1)
    e = gen_coprime(t)
    while not(gcd(t, e) == 1):
        e = gen_coprime(t)
    x = 1
    while not((x * t + 1) % e == 0):
        x += 1
    d = (x * t + 1) / e
    if e > 9999 or d >9999:
        rsakey = gen_keys()
    else:
        return RSAKeys(enc=e, dec=d, cy=(p * q))
    return rsakey
