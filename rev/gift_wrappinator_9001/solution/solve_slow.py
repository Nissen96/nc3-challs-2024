from pwn import *

context.log_level = "warn"

flag = "NC3{"
n = 33
alphabet = "}_013457abcdefghijklmnopqrstuvwxyz!2689ABCDEFGHIJKLMNOPQRSTUVWXYZ"

alpha = alphabet
while not (len(flag) == n and flag.endswith("}")):
    for c in alpha:
        attempt = flag + c + "A" * (n - len(flag) - 1)
        print(attempt)

        with process(("/usr/bin/python3", "wrappinator.py")) as io:
            io.sendlineafter(b": ", attempt.encode())
            response = io.recvlines(2 + len(flag) + 1)

        if b"FEJL" in response[-1]:
            continue

        flag += c
        alpha = alphabet
        break
    else:
        # Previous char was apparently not correct anyway
        # Recover and continue from this
        alpha = alphabet[alphabet.index(flag[-1]) + 1:]
        flag = flag[:-1]
