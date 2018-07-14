import sys
import cv2
import numpy as np
import ryabko
import random

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

if __name__ == "__main__":
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