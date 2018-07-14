import os
import sys

hm_path = os.path.abspath('lhc_generator/lhc_generator')
sys.path.insert(0, hm_path)
print (hm_path)

import ryabko.img_processing as ip


if __name__ == "__main__":
    container = [1, 0, 1, 0, 1, 1, 1]
    secret = [0, 1, 1] 
    seq = ip.hamming_encode(container, secret, 3)
    print (seq)
    sec = ip.hamming_decode(seq, 3)
    print (sec)


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