from pwn import *
from tqdm import trange

#io = process("postnordpolen-1.py")
io = remote("127.0.0.1", 1337)

def get_encrypted(msg=None, addr=b""):
    if msg is None:
        io.sendlineafter(b"> ", b"1")
    else:
        io.sendlineafter(b"> ", b"2")
        io.sendlineafter(b": ", msg)
        io.sendlineafter(b": ", addr)

    io.recvuntil(b": ")
    return bytes.fromhex(io.recvline().decode())


# Leak nonce length
nonce_len = len(get_encrypted(b""))

# Get encrypted flag
flag_enc = get_encrypted()
flag_nonce, flag_ct = flag_enc[:nonce_len], flag_enc[nonce_len:]

log.info(f"Flag nonce: {flag_nonce.hex()}")
log.info(f"Flag ct: {flag_ct.hex()}")

# Bruteforce encryptions until nonce reuse
msg = b"A" * 100
for _ in trange(300):
    enc = get_encrypted(msg)
    nonce, ct = enc[:nonce_len], enc[nonce_len:]
    if nonce == flag_nonce:
        break
else:
    print("Something went wrong!")
    exit()

log.success("Nonce reused!")

# Recover reused keystream and leak flag
ks = xor(msg, ct)
flag = xor(flag_ct, ks)
log.success(f"Flag: {flag[:flag.index(b'}') + 1].decode()}")

io.sendlineafter(b"> ", b"3")
