from secrets import token_bytes

with open("flag.txt", "r") as f:
    FLAG = f.read().strip()

KEY = b"DetHerErEnLangNoegleTiHi"

class CODEBOOK:
    def next():
        return token_bytes(16)
