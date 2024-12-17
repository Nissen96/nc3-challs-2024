instructions = {
    "\t\t ": "store",
    "\t\t\t": "retrieve",
    "\t\n\t ": "in_ascii",
    "\t\n\t\t": "in_num",
    "\t\n  ": "out_ascii",
    "\t\n \t": "out_num",
    "  ": "push",
    " \n ": "dup",
    " \n\t": "swap", 
    " \n\n": "pop",
    "\t   ": "add",
    "\t  \t": "sub",
    "\t  \n": "mult",
    "\t \t ": "div",
    "\t \t\t": "mod",
    "\t \t\n": "xor",
    "\n\n\n": "end",
}

with open("../src/program.ws") as f:
    code = f.read()

disassembly = []
while code:
    for pattern, text in instructions.items():
        if not code.startswith(pattern):
            continue

        code = code[len(pattern):]

        # If push, also read a number
        if pattern == "  ":
            bits = ""
            i = 1
            while (c := code[i]) != "\n":
                bits += "0" if c == " " else "1"
                i += 1
            n = ("-" if code[0] == "\t" else "") + str(int(bits, 2))
            text += f" {n}"
            code = code[len(bits) + 2:]

        disassembly.append(text)
        break
    else:
        print("SOMETHING WENT WRONG")
        exit()

for c in disassembly:
    print(c)
