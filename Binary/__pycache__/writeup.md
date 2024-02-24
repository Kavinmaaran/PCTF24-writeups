# \_\_pycache__
Typically, Python caches the bytecode for a file to improve performance for subsequent executions. So what we have is the compiled for the deleted file. We can even run the bytecode directly:
```
$ python3.7 prog.cpython-37.pyc
Enter key> something!     
Enter valid key!
```
We will use a [bytecode decompiler](https://github.com/rocky/python-decompile3) to decompile the bytecode. Thus, running 
```
$ decompyle3 prog.cpython37.pyc > out.py
```
The decompiled code is:
```py
# decompyle3 version 3.9.0
# Python bytecode version base 3.7.0 (3394)
# Decompiled from: Python 3.10.6 (main, May 29 2023, 11:10:38) [GCC 11.3.0]
# Embedded file name: ./prog.py
# Compiled at: 2023-12-24 13:44:35
# Size of source mod 2**32: 2695 bytes
import hashlib, base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
ENCRYTPED = '8a+RfXl1pAYnmJrLE0/+sjbqRvE6DLE1ihG8FXxfJx8t1JntQ/nnDRAWhFvJ+gZartzeCQrTLHt1+6aM/EfIAyvKkXLaxLwmeRPti/iEGbALCTD6TqN11PaCaxb6Sdx5BQTjUYzLpkLNxgJmhnL+tg=='
cff = [-6262905035520,449084368656,-12143512680,149297209,-755749,683,1]

def md5(s):
    return hashlib.md5(s.encode('utf-8')).hexdigest()


def encrypt(key, plaintext):
    if len(key) < 24:
        key += '0' * (24 - len(key))
    key = bytes(key, 'utf-8')
    if type(plaintext) == str:
        plaintext = bytes(plaintext, 'utf-8')
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
    raw = cipher.iv + ciphertext
    return base64.b64encode(raw).decode('utf-8')


def decrypt(key):
    if len(key) < 24:
        key += '0' * (24 - len(key))
    key = bytes(key, 'utf-8')
    ciphertext = base64.b64decode(ENCRYTPED)
    iv = ciphertext[:AES.block_size]
    cipher = AES.new(key, (AES.MODE_CBC), iv=iv)
    plaintext = unpad(cipher.decrypt(ciphertext[AES.block_size:]), AES.block_size)
    return plaintext


def pcheck(p):
    t = 0
    for c in p:
        u = 1
        for v in cff:
            t += u * v
            u *= ord(c)

    return t == 0 and ''.join((str(i) for _, i in sorted(((c, x) for x, c in enumerate(p))))) == '1302'


def vcheck(s):
    vals = [ord(c) for c in s]
    if len(vals) != 12:
        return False
    if md5(s[:2]) != '9e28ebf80dbe75e56a4ad72b34454128':
        return False
    if md5(s[-4:]) != 'b9931c29f59a31d1416c001551bda29a':
        return False
    lanes = [0] * 3
    chk = [0] * 6
    blobs = [0] * 4
    indivs = [0] * 6
    for i in range(0, 12, 4):
        for j in range(4):
            k = i // 4
            q = i + j
            lanes[k] ^= vals[i + j]
            lanes[k] = (lanes[k] << 1 | lanes[k] >> 7) & 255
            chk[q % 6] ^= vals[q]
            blobs[q % 4] += vals[q]
            if q < 6:
                indivs[q] = vals[q] + vals[q + 6]

    if lanes != [48, 103, 8]:
        return False
    if chk != [108,10,17,120,113,18]:
        return False
    if blobs != [242, 233, 198, 229]:
        return False
    if indivs != [146,172,173,126,121,164]:
        return False
    return True


def verify(key):
    if md5(key[:4]) != 'e409eb2ba6eb6801f52763ae370c350e':
        return False
    if not pcheck(key[4:8]):
        return False
    if not vcheck(key[8:]):
        return False
    return True


if __name__ == '__main__':
    key = input('Enter key> ').strip()
    if verify(key):
        exec(decrypt(key))
    else:
        print('Enter valid key!')
# okay decompiling prog.cpython-37.pyc
```
In the `verify` function, it checks the first 4 characters against a known md5 hash. Using a md5 hash table we can reverse using [this](http://reversemd5.com/) and [this](https://crackstation.net/) this to get the first 4 characters as `BYTE`.
The next 4 characters are checked using the `pcheck` function. We see that for every character, `u` is initially `1` and then is multiplied by the ASCII value of the character repeatedly, while multiplied by some value from the `cff` array, and then adding them to the total `t`. In essence, it's computing a polynomial with `cff` as its coefficients. Since the sum of all the evaluations of this polynomial is 0, we need to find the roots of the polynomial.
Using Wolfram Alpha, we get the roots that lie in the ASCII range as 48, 51, 67, 68 which are
the characters 0, 3, C, D. When we sort it, we get the order as '1302'. Currently the sorted order is `03CD`. In the final order, the 0th character goes to index 1, the 1st index goes to index 3, the 2nd index goes to index 0 and so on, which means the final order is `C0D3`.
The rest of the key is checked against the `vcheck` function. The first and last parts of the key can be found using reversing the MD5 hash which leads to `_S` and `_KEY`. The rest of the key is run through some bit manipulation logic which is too tedious to reverse manually. Therefore we will use `z3` to find the rest of the key which satisfies the function. A sample script is: 
```py
import z3

s = z3.Solver()
BITWIDTH = 16

vals = [z3.BitVec(f"vals[{i}]", BITWIDTH) for i in range(12)]
lanes = [z3.BitVec(f"lanes[{i}]", BITWIDTH) for i in range(3)]
chk = [z3.BitVec(f"chk[{i}]", BITWIDTH) for i in range(6)]
blobs = [z3.BitVec(f"blobs[{i}]", BITWIDTH) for i in range(4)]
indivs = [z3.BitVec(f"indivs[{i}]", BITWIDTH) for i in range(6)]

for v in vals:
    s.add(z3.UGE(v, 0), z3.ULE(v, 127))

for i in range(0, 12, 4):
    for j in range(4):
        k = i // 4
        q = i+j
        lanes[k] ^= vals[i+j]
        lanes[k] = ((lanes[k] << 1) | (lanes[k] >> 7)) & 0xff
        chk[q%6] ^= vals[q]
        blobs[q%4] += vals[q]

        if q < 6:
            indivs[q] = vals[q] + vals[q+6]
        


# Validate the results
# RESULTS
reslanes = [48, 103, 8]
reschk = [108, 10, 17, 120, 113, 18]
resblobs = [242, 233, 198, 229]
resindivs = [146, 172, 173, 126, 121, 164]
s.add(vals[0] == ord('_'))
s.add(vals[1] == ord('S'))
s.add(vals[-4] == ord('_'))
s.add(vals[-3] == ord('K'))
s.add(vals[-2] == ord('E'))
s.add(vals[-1] == ord('Y'))

for i in range(len(lanes)):
    s.add(lanes[i] == reslanes[i])
for i in range(len(chk)):
    s.add(chk[i] == reschk[i])
for i in range(len(blobs)):
    s.add(blobs[i] == resblobs[i])
for i in range(len(indivs)):
    s.add(indivs[i] == resindivs[i])

def getkey(model):
    key = ""
    ret = []
    for i in range(12):
        v = model[vals[i]].as_long()
        ret.append(v)
        key += chr(v)
    return key, ret


iters = 0
ITERLIMIT = 10
while s.check() == z3.sat:
    print(getkey(s.model()))
    #print(s.model())
    iters += 1
    if iters > ITERLIMIT:
        break
```
Running the script, we get the output as `_SN34K3Y_KEY`. Combining all parts together, we find the final key is `BYTEC0D3_SN34K3Y_KEY`. Using this: 
```
$ python3.7 prog.cpython-37.pyc
Enter key> BYTEC0D3_SN34K3Y_KEY
Congrats! You are indeed a 1337 h4x0r.
p_ctf{byt3c0d3_1s_4w3s0m3}
```
And we get the flag!