#!/usr/bin/python2
from __future__ import print_function
from sympy import Symbol, Rational, binomial, expand_func
from sympy.utilities.iterables import multiset_permutations

def find_j(vec, s):
    len_s = len(s)
    ind = s.index(list(vec))
    bs = format(len(s), "b")
    bi = format(ind, "b")
    bi = "0"*(len(bs) - len(bi)) + bi
    j = 0
    while j < len(bi):
        if bi[j] != bs[j]:
            break
        j += 1
    return (j, bi)

def med_nb(n, k):
    l = binomial(n, k)
    bs = format(int(l), "b")
    res = 0
    sb = bs[::-1]
    i = 0
    while i < len(sb):
        res += int(sb[i])*(2**i)*i
        i += 1
    res /= l
    return res

def hamming2(s1, s2):
    """Calculate the Hamming distance between two bit strings"""
    assert len(s1) == len(s2)
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))

def med_hamm2(n, k):
    u = '1' * k + '0' * (n-k)
    s = sorted(list(multiset_permutations(u)))
    res = 0
    for v in s:
        res += hamming2(u, ''.join(v))
    return (res / binomial(n, k))

def med_eff(n, k):
    u = '1' * k + '0' * (n-k)
    s = sorted(list(multiset_permutations(u)))
    res = 0
    for v in s:
        j, bi = find_j(v, s)
        res += ((len(bi) - j - 1) / hamming2(u, ''.join(v)))
    return (res / binomial(n, k))

def med_hamm1(n, k):
    res = 0
    for i in range(1, k + 1):
        res += 2*i*binomial(k, i)*binomial(n-k,i)
    return (res / binomial(n, k))


def main():
    print('n/k', end='   ')
    for n in range(1, int(40/2)):
        print('%03d' % n, end='   |  ')
    print()
    for n in range(2, 40):
        print('%03d' % n, end='  ')
        for k in range(1, int(n/2 + 1)):
            mnb = med_nb(n, k)
            mhm = med_hamm1(n, k)
            eff = mnb / mhm
            print('%06.3f' % (eff), end=' | ')
            #print('%06.3f = %06.3f / %06.3f' % (eff, mnb, mhm), end=' | ')
        print()
        

main()
