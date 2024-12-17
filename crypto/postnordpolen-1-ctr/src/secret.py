from itertools import cycle
from secrets import token_bytes

with open("flag.txt", "rb") as f:
    FLAG = f.read().strip()

KEY = token_bytes(16)

class CODEBOOK:
    codes = cycle([token_bytes(12) for _ in range(250)])

    def next():
        return next(CODEBOOK.codes)
