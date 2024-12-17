from secrets import token_bytes

with open("flag.txt", "rb") as f:
    FLAG = f.read().strip()

class CODEBOOK:
    def next():
        return token_bytes(16)
