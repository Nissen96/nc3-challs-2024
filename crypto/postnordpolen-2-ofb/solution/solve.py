from pwn import *
from tqdm import trange

#io = process("postnordpolen-2.py")
io = remote("127.0.0.1", 1337)

# Chosen IV attack on OFB mode
# Problem: Must know first block but knows only 13 bytes (prefix + flag format)

# Solution 1: Bruteforce last three bytes of 1st block - slow, many connections
# Solution 2: Send enough letters (1000+) before getting flag, so letter ID takes up four bytes

def encrypt_msg(msg, iv, addr=b""):
    io.sendlineafter(b"> ", b"2")
    io.sendlineafter(b": ", msg)
    io.sendlineafter(b": ", addr)
    io.sendlineafter(b": ", iv.hex().encode())
    io.recvuntil(b": ")
    return bytes.fromhex(io.recvline().decode())


# Fill up letter ID
for i in trange(999):
    ct = encrypt_msg(b"", b"\x00" * 16)

# Message number 1000 - get flag encryption
io.sendlineafter(b"> ", b"1")
io.recvuntil(b": ")
flag_ct = bytes.fromhex(io.recvline().decode())
log.info(f"Flag ct: {flag_ct.hex()}")

# Flag message will now have prefix "[BREV 1000] NC3{" - a full block!
# Leak first keystream block from known plaintext-ciphertext pair
msg = b"[BREV 1000] NC3{"
ks = xor(msg, flag_ct[:16])
log.info(f"Keystream #1: {ks.hex()}")

# Use ks as IV to leak entire keystream shifted one block
# By encrypting null bytes, the ciphertext is (almost) just the keystream
ct = encrypt_msg(b"\x00" * len(flag_ct), ks)

# Just need to remember the auto-prepended "[BREV 1001]: "
ks += xor(ct[:12], b"[BREV 1001] ") + ct[12:]
log.info(f"Keystream: {ks.hex()}")

msg = xor(flag_ct, ks)[:len(flag_ct)]
log.success(msg.decode())

io.sendlineafter(b"> ", b"3")
