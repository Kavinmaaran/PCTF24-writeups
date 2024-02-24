#!/usr/local/bin/python3

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

key = open("key", "rb").read()
    
cipher = AES.new(key, AES.MODE_ECB)

def generate(pt):
    ct = cipher.encrypt(pad(pt.encode(), 16)).hex()
    return ct

if __name__ == '__main__':
    print("Welcome to PassionFruit Inc.'s premium service to encrypt text using AES-128 in ECB mode\n")

    for _ in range(2000000):
        pts = [ x.strip() for x in input("Enter text to encrypt using PASSION as a separator:\n").split("PASSION")]

        if len(pts) > 100:
            print("Only 100 inputs at once")
            continue
        
        for pt in pts:
            print(generate(pt))