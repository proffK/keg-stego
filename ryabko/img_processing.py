import sys
import cv2
import numpy as np
import ryabko

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

    return ''.join(outseq)

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
    r_list = list(get_pixels(sys.argv[1], 0))
    g_list = list(get_pixels(sys.argv[1], 2))

    r_str = ''.join(str(i) for i in r_list)

    out = ryabko_encode(r_str, "1010101010101", 8)

    print (ryabko_decode(out, 8))