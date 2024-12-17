import marshal
import random

with open("flag.txt", "rb") as f:
    FLAG = f.read().strip()

DELAY = 0.1

def xor(*args):
    args = [bytearray([s]) if isinstance(s, int) else bytearray(s) for s in args]

    def xor_(n):
        xored = 0
        for s in args:
            xored ^= s[n % len(s)]
        return xored

    length = max(len(s) for s in args)
    return bytes(map(xor_, range(length)))



def color(txt, clr):
    return f"\033[38;5;{clr}m{txt}"


# Build Chritmas tree
with open("tree.txt") as f:
    tree = f.read().strip("\n").split("\n")

xmas_tree = [color(line, 226) for line in tree[:3]]

greens = [22, 22, 28, 28, 34]
colors = [1, 9, 11, 15, 45, 87, 118, 154, 155, 165, 193, 196, 198, 208, 226]
i = 4
spaces = 100
for line in tree[3:-3]:
    if line.count(" ") > spaces:
        i = 0
    spaces = line.count(" ")
    green = greens[min(i, len(greens) - 1)]
    new_line = color(line, green)
    new_line = new_line.replace("o", color("o", random.choice(colors)) + color("", green))
    new_line = new_line.replace("O", color("O", random.choice(colors)) + color("", green))
    xmas_tree.append(new_line + "\033[0m")
    i += 1
xmas_tree.extend([color(line, 94) + "\033[0m" for line in tree[-3:]])

# Generate challenge code
code = ""
for line in xmas_tree[-3:]:
    code += f"time.sleep({DELAY})\n"
    code += f"print(\"{line}\033[0m\")\n"

code += f"time.sleep({DELAY})\n"
code += "print(\"\\nHurraaa, alle lag gavepapir er nu pakket op!\")"


for i in range(len(FLAG) - 1, -1, -1):
    compiled = compile(code, "", "exec")
    marshalled = marshal.dumps(compiled)
    xored = xor(marshalled, range(min(len(marshalled), 256)), FLAG[i])

    code = f"""
marshalled = xor({xored}, range({min(len(xored), 256)}), user_input[{i}])
compiled = marshal.loads(marshalled)
time.sleep({DELAY})
print("{xmas_tree[3 + i]}")
exec(compiled)
"""

preamble = "import time\n\n"
for line in xmas_tree[:3]:
    preamble += f"time.sleep({DELAY})\n"
    preamble += f"print(\"{line}\")\n"

code = f"{preamble}\n{code}"

compiled = compile(code, "", "exec")
marshalled = marshal.dumps(compiled)

# Write challenge to chal.py
chall = f"""#!/usr/bin/env python3

import marshal


def xor(*args):
    # Smart XOR implementation based on pwntools:
    # https://github.com/Gallopsled/pwntools/blob/db98e5edfb/pwnlib/util/fiddling.py#L299-L351
    args = [bytearray([s]) if isinstance(s, int) else bytearray(s) for s in args]

    def xor_(n):
        xored = 0
        for s in args:
            xored ^= s[n % len(s)]
        return xored

    length = max(len(s) for s in args)
    return bytes(map(xor_, range(length)))


user_input = input("Indtast kodeord til Gift Wrappinator 9001: ").encode()
assert len(user_input) == {len(FLAG)}, "Kodeordets længde passer ikke med antal lag!"

check = {marshalled}

try:
    exec(marshal.loads(check))
except (ValueError, EOFError, TypeError, SyntaxError):
    print(\"""" + color('FEJL: Koden matcher ikke gaveindpakningen!', 1) + "\033[0m" + '")'

with open("wrappinator.py", "w") as f:
    f.write(chall)


# Test challenge
user_input = FLAG
exec(compiled)
