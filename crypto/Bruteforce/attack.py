from pwn import *
import string

chars = string.ascii_letters + string.digits + string.punctuation + " "

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

ct = "3241bb91577091d488a49e81fe6332a6c2580a3241d1289f9e03b0ef02e1bb2b"

first_chars = ["hidinginsaint", "kittsisnotbad"]

conn = remote("brute.ctf.pragyan.org", 50336)
conn.recvuntil(':')

final_blocks = []
batch = []

def get_from_server(pt):
    conn.sendline(pt.encode())
    return conn.recvuntil(":").decode().splitlines()[1:-1]

def bruteforce(ct):
    blocks = list(map(''.join, zip(*[iter(ct)]*32)))
    n = len(blocks)
    for i in range(n):
        print(i)
        def is_same(str, block = blocks[i]):
            batch.append(first_chars[i]+str)

            if len(batch) == 100:
                sentence = "PASSION".join(batch)
                encrypted_blocks = get_from_server(sentence)
                if i!=(n-1):
                    encrypted_blocks = [ encrypted_block[:32] for encrypted_block in encrypted_blocks ]
                    
                if block[:32] in encrypted_blocks:
                    final_blocks.append(batch[encrypted_blocks.index(block[:32])])
                    batch.clear()
                    return True
                batch.clear()
            
        if i==n-1:
            pwnlib.util.iters.bruteforce(is_same, chars, 3, method='upto')
        else:
            pwnlib.util.iters.bruteforce(is_same, chars, 3, method='fixed')

def main():
    bruteforce(ct)
    print(final_blocks)
    print(f"Final password is {final_blocks[0]}{final_blocks[1]} ")
    conn.close()
main()