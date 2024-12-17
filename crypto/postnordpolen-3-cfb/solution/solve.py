# https://github.com/blaufish/cfb8-vulnerable
# For some keys, an all-zero initialization vector may generate some block cipher modes (CFB-8, OFB-8) to get the internal state stuck at all-zero.
# For CFB-8, an all-zero IV and an all-zero plaintext, causes 1/256 of keys to generate no encryption, plaintext is returned as ciphertext.
from Crypto.Cipher import AES
from pwn import *
from tqdm import trange

#io = process("postnordpolen-3.py")
io = remote("127.0.0.1", 1337)


def decrypt(pt, key, iv):
    cipher = AES.new(key, mode=AES.MODE_CFB, iv=iv)
    return cipher.decrypt(pt)

# Keep sending pure null bytes for pt and IV - for 1/256 this generates null ct
# The ct is used as encryption key for flag, so then key is known
payload = b"\x00" * 16
for _ in trange(300):
    io.sendlineafter(b"> ", b"1")
    io.sendlineafter(b": ", (payload * 2).hex().encode())

    io.recvuntil(b": ")
    flag_ct = bytes.fromhex(io.recvline().decode())

    io.recvuntil(b": ")
    iv = bytes.fromhex(io.recvline().decode())

    flag = decrypt(flag_ct, payload, iv)
    if flag.startswith(b"NC3{"):
        break
else:
    print("Didn't get a null key, run again")
    exit()

log.info("Got encryption with null key")
log.success(f"Flag: {flag.decode()}")

io.sendlineafter(b"> ", b"3")
