# Half Key
We know that the same message has been encrypted 5 times using RSA so we can try the cleartext by finding the 5th root of the ciphertext.
Hastad’s Broadcast Attack works against small public exponent, when the number of ciphertexts is equal to e itself.
In some cases, we can directly find the cleartext by finding the eth root of the ciphertext.
But in other cases, we can use Hastad's Broadcast Attack which uses Chinese Remainder Theorem to calculate the flag..

First we read messages.txt and store the data in lists. We also convert ciphertexts from base64 to long.
```python
from base64 import b64decode
from Crypto.Util.number import bytes_to_long
C=list()
N=list()

e = 5
with open("messages.txt") as f:
    lines = f.readlines()
    for i in range(0,2*e,2):
        _, n = lines[i].split("=")
        print(lines[i+1].split("="))
        _, c = lines[i+1].split("=",1)
        c = bytes_to_long(b64decode(c))
        N.append(int(n))
        C.append(c)
```

We can try finding the 5th root of the ciphertext.
```python
from gmpy2 import iroot
from Crypto.Util.number import long_to_bytes

def eth_root(n):
    m, valid = iroot(n, e)
    if valid:
        print("Cleartext :", long_to_bytes(m))
    else:
        print("Unable to find the eth root of :", n)

e = 5
# trying to find eth root
for c in C:
    eth_root(c)
```

Output:
```bash
Unable to find the eth root of : 90650832816073126329812257415347541459766056030366490261727276385751451038516360907727384136758329391892730338792171960505826346220438792307116344502476449552960715240843126441850204668395199414583836234086782878025895957281598694244659476455578666234333150218746722348310050909980004224298861946626913511290
Unable to find the eth root of : 30293520459289814593247035686228987709284204917153794587730683353054091262193928508901022002445069743602814085294693592024458302132376608000865240544585679754875060910854756670391025453741146054837234262460834984696053904394715993594499544685193402200083970956007939453940031090571690828089459429364018966458
Unable to find the eth root of : 91066246147759929937630962106309237266557685934319535869778398104103696657193374780695048073676231233206339729396049439031327685353239053951034885706687190399520161438099411002603660157377325261906375373456178988301987933683598448412284158887283280781115000210481230141843123022735758111829280670910363604041
Unable to find the eth root of : 52622503694781537582045349950152653958472337573257052164598218266249263992076813333026468316344438142214655362853174109660094653102088279301930917211892679518117429523141539215059687757751851276068497945363353049989156193602300618495935209648894829207216455965187973086690829152248952445859861412508709048381
Unable to find the eth root of : 101194572423145990677370302299243446437077754594786215202158388259648397489769327932372286122887473872596207279934181322819959238469867447154483042002264784133487910645009586697656349279247697574662749451429881511997835223788755618936649920710660447899635440940717381402229478227276094192133458788187251747406
```
Since finding 5th root didnt work, we use Hastad's Broadcast attack

```python
from gmpy2 import invert
def mul(lst):
    ret = 1
    for n in lst:
        ret *= n
    return ret

def crt(C, N):
    assert len(C) == len(N)

    total = 0
    modulo = mul(N)

    for n_i, c_i in zip(N, C):
        p = modulo // n_i
        total += c_i * invert(p, n_i) * p
    return total % modulo

x = crt(C, N)
eth_root(x)
```

Output:

```bash
Cleartext : b'p_ctf{p&dd1ngPr3vent$h@stAd$_a%%ack}'
```

The combined program is given below.
```python
from gmpy2 import iroot, invert
from base64 import b64decode
from Crypto.Util.number import bytes_to_long, long_to_bytes

def mul(lst):
    ret = 1
    for n in lst:
        ret *= n
    return ret

def crt(C, N):
    assert len(C) == len(N)

    total = 0
    modulo = mul(N)

    for n_i, c_i in zip(N, C):
        p = modulo // n_i
        total += c_i * invert(p, n_i) * p
    return total % modulo

def eth_root(n):
    m, valid = iroot(n, e)
    if valid:
        print("Cleartext :", long_to_bytes(m))
    else:
        print("Unable to find the eth root of :", n)

# reading file
# assume e =5 based on the number of ciphertexts
e = 5
C=list()
N=list()

with open("messages.txt") as f:
    lines = f.readlines()
    for i in range(0,2*e,2):
        _, n = lines[i].split("=")
        print(lines[i+1].split("="))
        _, c = lines[i+1].split("=",1)
        c = bytes_to_long(b64decode(c))
        N.append(int(n))
        C.append(c)

print(C)
print(N)
# trying to find eth root
for c in C:
    eth_root(c)

x = crt(C, N)
eth_root(x)
```