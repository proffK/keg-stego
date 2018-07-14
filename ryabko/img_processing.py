import sys
import cv2
import numpy as np
import ryabko
import random
import os
import lhc_generator as lg


def get_pixels(png_path, color):
    mask = np.uint8(1)

    img = cv2.imread(png_path, cv2.IMREAD_COLOR)
    for row in range(0, img.shape[0]):
        for col in range(0, img.shape[1]):
            yield np.bitwise_and(img[row][col][color], mask)

def set_pixels(png_path, color, bit_sequence):
    mask = np.uint8(254) # b11111110
    input_bit = iter(bit_sequence)

    img = cv2.imread(png_path, cv2.IMREAD_COLOR)
    for row in range(0, img.shape[0]):
        for col in range(0, img.shape[1]):
            cur_bit = np.uint8(next(input_bit))
            value = np.bitwise_and(img[row][col][color], mask)
            img[row][col][color] = np.bitwise_or(value, cur_bit)

    cv2.imwrite(png_path, img)

def ryabko_encode(bit_seq_str, secret_str, chunk):
    i = chunk
    j = 0
    outseq = []

    while (i <= len(bit_seq_str) and j <= len(secret_str)):
        u = bit_seq_str[i-chunk:i]
        
        v, nb = ryabko.encode(u, secret_str[j:])
        #print("Encoded = ", v)
        outseq += v
    
        i += chunk
        j += nb

    if i <= len(bit_seq_str):
        outseq += bit_seq_str[len(outseq):]

    return (''.join(outseq), j)

def ryabko_decode(bit_seq_str, chunk):
    i = chunk
    outseq = []

    while (i <= len(bit_seq_str)):
        u = bit_seq_str[i-chunk:i]
        
        sec_str = ryabko.decode(u)
        #print("Encoded = ", v)
        outseq += sec_str
    
        i += chunk

    if i <= len(bit_seq_str):
        outseq += bit_seq_str[len(outseq):]

    return ''.join(outseq)

def hamming_encode(bit_seq, secret, code_length):
    length = 2**code_length - 1 - code_length
    container_len = 2**code_length - 1
    output_seq = []

    code = lg.LHC(l=length, extended=False)
    H_t = code.H.transpose()

    enc_dict = {}
    for i in range(container_len):
        value = np.array([0] * container_len)
        value[i] = 1
        #print (value)
        key = np.matmul(value, H_t)
        #print (key)
        enc_dict[''.join(str(i) for i in key)] = value

    sec_pos = code_length
    exclude = [0] * container_len
    pos = container_len
    while pos <= len(bit_seq):
        if bit_seq[pos-container_len:pos] == exclude:
            continue
        
        s = np.matmul(bit_seq[pos-container_len:pos], H_t)
        for i in range(len(s)):
            s[i] = s[i] % 2

        res = []
        s_iter = iter(s)
        # m = secret[sec_pos-code_length:sec_pos]
        for j in secret[sec_pos-code_length:sec_pos]:
            res.append(next(s_iter) ^ bool(j))
        # res = s xor m = e x H_t
        e = enc_dict[''.join(str(i) for i in res)]

        for i in range(len(e)):
            output_seq.append(e[i] ^ bit_seq[pos - container_len + i])

        sec_pos += code_length
        pos += container_len

    return output_seq           

def hamming_decode(bit_seq, code_length):
    length = 2**code_length - 1 - code_length
    container_len = 2**code_length - 1
    secret = []

    code = lg.LHC(l=length, extended=False)
    H_t = code.H.transpose()

    pos = container_len
    while pos <= len(bit_seq):
        m = np.matmul(bit_seq[pos-container_len:pos], H_t)
        for i in range(len(m)):
            secret.append(m[i] % 2)

        pos += container_len

    return secret


if __name__ == "__main__":
    pass

'''
    op_type  = sys.argv[1]
    img_path = sys.argv[2]
    chunk    = int(sys.argv[3])
    randBinList = lambda n: [random.randint(0,1) for b in range(1,n+1)]

    r_list = list(get_pixels(img_path, 0))
    r_str = ''.join(str(i) for i in r_list)
        
    if op_type == "-d":
        decoded_seq = ryabko_decode(r_str, chunk)
    elif op_type == "-e":
        secret = ''.join(str(i) for i in randBinList(10000))
        enc_seq, enc_bits = ryabko_encode(r_str, secret, chunk)
        print ("Encoded bits:")
        print (enc_bits)
    else:
        print("Invalid param")
'''