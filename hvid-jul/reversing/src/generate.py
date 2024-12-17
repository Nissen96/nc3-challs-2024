from enum import Enum

from pwn import *


SBOX = [
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16,
]


class I(Enum):
    STORE = "\t\t "
    RETRIEVE = "\t\t\t"
    IN_ASCII = "\t\n\t "
    IN_NUM = "\t\n\t\t"
    OUT_ASCII = "\t\n  "
    OUT_NUM = "\t\n \t"
    PUSH = "  "
    DUP = " \n "
    SWAP = " \n\t"
    POP = " \n\n"
    ADD = "\t   "
    SUB = "\t  \t"
    MULT = "\t  \n"
    DIV = "\t \t "
    MOD = "\t \t\t"
    XOR = "\t \t\n"
    END = "\n\n\n."


def NUMBER(n: int):
    out = " " if n >= 0 else "\t"
    for bit in bin(n)[2:]:
        out += " " if bit == "0" else "\t"

    return out + "\n"


def push(n):
    return [I.PUSH, NUMBER(n)]


def puts(s, newline=True):
    out = []
    if newline:
        s += "\n"
    for c in s:
        out.extend(push(ord(c)))
        out.append(I.OUT_ASCII)

    return out


def heap_store(ls, offset=0):
    out = []
    for n in ls:
        out.extend(push(offset))
        out.extend(push(n))
        out.append(I.STORE)
        offset += 1

    return out


def heap_print(length, offset=0):
    out = []
    for i in range(offset, offset + length):
        out.extend(push(i))
        out.append(I.RETRIEVE)
        out.append(I.OUT_NUM)
        out.extend(puts(" ", newline=False))
    return out


def getc(addr):
    return [*push(addr), I.IN_ASCII]


def gets(length, offset=0):
    out = []
    for addr in range(offset, offset + length):
        out.extend(getc(addr))

    return out


def xor_key(key, state, next_state, length=16):
    out = []
    for i in range(length):
        out.extend(push(next_state + i))
        out.extend(push(key + i))
        out.append(I.RETRIEVE)
        out.extend(push(state + i))
        out.append(I.RETRIEVE)
        out.append(I.XOR)
        out.append(I.STORE)

    return out


def sub_bytes(sbox, state, next_state):
    out = []
    for i in range(16):
        out.extend(push(next_state + i))
        out.extend(push(sbox))
        out.extend(push(state + i))
        out.append(I.RETRIEVE)
        out.append(I.ADD)
        out.append(I.RETRIEVE)
        out.append(I.STORE)

    return out


def shift_rows(state, next_state):
    out = []
    order = [0, 5, 10, 15, 4, 9, 14, 3, 8, 13, 2, 7, 12, 1, 6, 11]
    for i, n in enumerate(order):
        out.extend(push(next_state + i))
        out.extend(push(state + n))
        out.append(I.RETRIEVE)
        out.append(I.STORE)

    return out


def translate(prog: list[I | str]):
    return "".join([x if type(x) is str else x.value for x in prog])


def main():
    key = b"Nu' det jul igen"

    prog = [
        *puts("=====\nJulemandens Kryptomat\n=====\nIndtast besked\n> ", newline=False),
        *gets(48, offset=0),

        *heap_store(key, offset=200),
        *heap_store(SBOX, offset=300),

        *puts("\nKrypteret: ", newline=False),

        *xor_key(key=200, state=0, next_state=100),
        *sub_bytes(sbox=300, state=100, next_state=120),
        *shift_rows(state=120, next_state=140),
        *heap_print(16, offset=140),

        *xor_key(key=200, state=16, next_state=100),
        *sub_bytes(sbox=300, state=100, next_state=120),
        *shift_rows(state=120, next_state=140),
        *heap_print(16, offset=140),

        *xor_key(key=200, state=32, next_state=100),
        *sub_bytes(sbox=300, state=100, next_state=120),
        *shift_rows(state=120, next_state=140),
        *heap_print(16, offset=140),

        *puts(""),
        I.END,
    ]

    translated = translate(prog)
    with open("hvid-jul.ws", "w") as f:
        f.write(translated)


if __name__ == "__main__":
    main()
