#!/usr/bin/python3
from sympy.utilities.iterables import multiset_permutations

def find_j(vec, s):
    len_s = len(s)
    ind = s.index(list(vec))
    bs = format(len(s), "b")
    bi = format(ind, "b")
    bi = "0"*(len(bs) - len(bi)) + bi
    print(bs, bi, ind)
    j = 0
    while j < len(bi):
        if bi[j] != bs[j]:
            break
        j += 1
    return (j, bi)


def encode(u, secret):
    s = sorted(list(multiset_permutations(u)))
    ind = s.index(list(u))
    print(s)
    j, bi = find_j(u, s)
    if (j == len(u)):
        return (u, 0)
    nb = len(bi) - j - 1
    bi = bi[:j+1]
    print(bi)
    bi += secret[0:nb]
    print(bi, j)
    v = s[int(bi, 2)]
    print(v, secret)
    return (v, nb)

def hamming2(s1, s2):
    """Calculate the Hamming distance between two bit strings"""
    assert len(s1) == len(s2)
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))

def decode(v): 
    s = sorted(list(multiset_permutations(v)))
    ind = s.index(list(v))
    j, bi = find_j(v, s)
    secret = bi[j+1:]
    return secret

def main():

    seq = input("Input seq: ")
    n = int(input("Input n: "))
    sec = input("Input secret: ")
    sumh = 0
    sumbytes = 0
    i = n
    j = 0
    outseq = []

    while (i <= len(seq) and j <= len(sec)):
        u = seq[i-n:i]
        enc = encode(u, sec[j:])
        print("Encoded = ", enc[0])
        outseq += enc[0]
        print("Inserted bytes = ", enc[1])
        sumbytes += enc[1]
        h = hamming2(u, enc[0])
        sumh += h
        print("Hamming distance: ", h)
        i += n
        j += enc[1]
    
    if j <= len(sec):
        outseq += seq[len(outseq):]

    outs = ''.join(outseq)
    print("Total: ")
    print("Sum inserted bytes: ", sumbytes)
    print("Sum modifyed bytes: ", sumh)
    print("Efficiency: ", sumbytes / sumh)
    print("Output sequence: ", outs)

    #dec = decode(enc[0])
    #print("Decoded = ", dec)

main()
