import marshal
import time


def xor(*args):
    # Copy pasted from challenge
    args = [bytearray([s]) if isinstance(s, int) else bytearray(s) for s in args]

    def xor_(n):
        xored = 0
        for s in args:
            xored ^= s[n % len(s)]
        return xored

    length = max(len(s) for s in args)
    return bytes(map(xor_, range(length)))


# Load encoded string from challenge
with open("wrappinator.py") as f:
    data = f.read()
    start = data.find("check = b'") + 8
    end = data.find("try:", start) - 2
    encoded = eval(data[start:end])

# Continuously extract the next marshalled, encrypted bytecode, get the key byte (flag char), and decrypt
check = encoded
flag = ""
while not flag.endswith("}"):
    code = marshal.loads(check)
    new = max(code.co_consts, key=lambda x: len(str(x)))
    c = new[0] ^ 0xe3
    flag += chr(c)
    check = xor(new, range(256), c)
    print(flag)

print("\nFound flag, running code to verify...\n")

# Verify found flag by running challenge with this as user input
code = marshal.loads(encoded)
user_input = flag.encode()
exec(code)
