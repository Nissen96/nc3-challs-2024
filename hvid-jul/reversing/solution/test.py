from pwn import xor

HEAP = [0] * 1024
EXPECTED = bytes.fromhex("63 82 1a 09 fe 84 c9 39 d4 ca fa 53 72 05 63 76 9a c5 7c d7 82 a2 82 20 01 6f 00 ab 72 a2 82 76 f7 f2 39 7d 5b 83 34 a4 77 d8 d1 84 d8 d6 27 fc")

# Input
HEAP[:48] = [*(b"A" * 16)]

# Constants stored on heap
HEAP[200:216] = [*b"Nu' det jul igen"]
HEAP[300:556] = [*bytes.fromhex("637c777bf26b6fc53001672bfed7ab76ca82c97dfa5947f0add4a2af9ca472c0b7fd9326363ff7cc34a5e5f171d8311504c723c31896059a071280e2eb27b27509832c1a1b6e5aa0523bd6b329e32f8453d100ed20fcb15b6acbbe394a4c58cfd0efaafb434d338545f9027f503c9fa851a3408f929d38f5bcb6da2110fff3d2cd0c13ec5f974417c4a77e3d645d197360814fdc222a908846eeb814de5e0bdbe0323a0a4906245cc2d3ac629195e479e7c8376d8dd54ea96c56f4ea657aae08ba78252e1ca6b4c6e8dd741f4bbd8b8a703eb5664803f60e613557b986c11d9ee1f8981169d98e949b1e87e9ce5528df8ca1890dbfe6426841992d0fb054bb16")]

# STAGE 1: XORing with 1st constant (XOR key)
HEAP[100:116] = [*xor(HEAP[:16], HEAP[200:216])]
print(bytes(HEAP[100:116]).hex(" "))

# STAGE 2: Substitution
HEAP[120:136] = [HEAP[300 + HEAP[i]] for i in range(100, 116)]
print(bytes(HEAP[120:136]).hex(" "))

# STAGE 3: Swap
swapping = {
    120: 140,
    125: 141,
    130: 142,
    135: 143,
    124: 144,
    129: 145,
    134: 146,
    123: 147,
    128: 148,
    133: 149,
    122: 150,
    127: 151,
    132: 152,
    121: 153,
    126: 154,
    131: 155,
}

for src, dst in swapping.items():
    HEAP[dst] = HEAP[src]

print(bytes(HEAP[140:156]).hex(" "))

# REPEATED FOR TWO MORE CHUNKS - RESULT:
output = bytes.fromhex("76 36 d8 15 3f 18 36 ef f1 f7 33 ef 34 18 96 ef 76 36 d8 15 3f 18 36 ef f1 f7 33 ef 34 18 96 ef 76 36 d8 15 3f 18 36 ef f1 f7 33 ef 34 18 96 ef")  # From own test
output = bytes([99, 130, 26, 9, 254, 132, 201, 57, 212, 202, 250, 83, 114, 5, 99, 118, 154, 197, 124, 215, 130, 162, 130, 32, 1, 111, 0, 171, 114, 162, 130, 118, 247, 242, 57, 125, 91, 131, 52, 164, 119, 216, 209, 132, 216, 214, 39, 252])  # From challenge handout
print("\n" + output.hex(" ") + "\n")


# REVERSING - DECRYPTION
for chunk in range(3):
    HEAP[140:156] = list(output[16 * chunk:16 * (chunk + 1)])
    print(bytes(HEAP[140:156]).hex(" "))

    # STAGE 3: Swap back
    for src, dst in swapping.items():
        HEAP[src] = HEAP[dst]
    print(bytes(HEAP[120:136]).hex(" "))

    # STAGE 2: Substitute back
    HEAP[100:116] = [HEAP[300:300 + 256].index(HEAP[i]) for i in range(120, 136)]
    print(bytes(HEAP[100:116]).hex(" "))

    # STAGE 1: XOR back
    HEAP[16 * chunk:16 * (chunk + 1)] = [*xor(HEAP[100:116], HEAP[200:216])]
    print(bytes(HEAP[16 * chunk:16 * (chunk + 1)]).hex(" ") + "\n")

# Final output
flag = bytes(HEAP[:48])
print(flag.hex(" "))
print(flag.decode())
