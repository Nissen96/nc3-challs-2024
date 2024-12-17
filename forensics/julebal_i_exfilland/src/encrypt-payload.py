SBOX = [
    114, 228, 149, 181, 83, 158, 132, 91, 168, 219, 53, 223, 196, 1, 227, 205, 
    137, 26, 173, 130, 99, 76, 159, 202, 240, 74, 21, 241, 110, 229, 239, 211, 
    151, 204, 113, 101, 134, 201, 248, 108, 226, 90, 19, 162, 45, 210, 142, 224, 
    216, 70, 105, 186, 78, 160, 13, 220, 55, 107, 217, 46, 10, 7, 243, 47, 
    171, 65, 170, 155, 117, 39, 177, 183, 11, 225, 191, 215, 178, 184, 54, 244, 
    249, 100, 50, 36, 207, 156, 33, 67, 0, 252, 73, 6, 5, 121, 237, 115, 
    59, 32, 161, 198, 58, 82, 206, 12, 31, 172, 195, 143, 66, 85, 187, 138, 
    18, 165, 250, 150, 175, 52, 213, 200, 221, 253, 231, 102, 22, 238, 14, 127, 
    40, 20, 104, 135, 63, 29, 133, 41, 62, 71, 69, 167, 24, 194, 144, 87, 
    111, 49, 254, 96, 3, 242, 199, 176, 9, 34, 148, 30, 147, 81, 222, 212, 
    247, 139, 152, 246, 93, 42, 209, 157, 15, 38, 72, 86, 179, 234, 164, 27, 
    163, 141, 214, 145, 25, 60, 106, 8, 125, 131, 112, 97, 51, 57, 68, 120, 
    166, 126, 129, 197, 146, 255, 123, 124, 94, 251, 84, 89, 230, 235, 189, 103, 
    140, 56, 48, 118, 169, 119, 43, 37, 98, 116, 185, 236, 180, 203, 188, 174, 
    193, 92, 64, 136, 232, 80, 44, 75, 153, 190, 122, 88, 154, 77, 61, 192, 
    182, 35, 23, 233, 79, 245, 16, 28, 95, 109, 2, 4, 218, 208, 17, 128
]

def encrypt(pt):
    ct = []
    for i, x in enumerate(pt):
        x = ~x & 0xff
        x = SBOX.index(x)
        x = ((x & 7) << 5) | (x >> 3)
        x ^= (i % 256) ^ 0x5A
        ct.append(x)
    return ct


with open("exfil-2.ps1", "rb") as f:
    pt = f.read()

blocks = [pt[i:i + 2000] for i in range(0, len(pt), 2000)]
for b in blocks:
    ct = encrypt(b)
    for i, x in enumerate(ct):
        print(x, end=", ")
        if i % 200 == 199:
            print("_")

    print()
    print()