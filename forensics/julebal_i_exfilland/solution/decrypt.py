from base64 import b64decode
from Crypto.Cipher import ARC4

with open("outputs.txt") as f:
    outputs = f.read().strip().split("\n")

key = b"Jul3b4lI3xf1ll4nd!"
for output in outputs:
    cipher = ARC4.new(key)
    ct = b64decode(output)
    pt = cipher.decrypt(ct)
    print(pt.decode())
    print()
