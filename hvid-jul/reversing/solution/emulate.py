import sys

STACK = [0] * 1024
HEAP = [0] * 1024
SP = 0

def push(num):
    global SP
    STACK[SP] = num
    SP += 1

def pop() -> int:
    global SP
    SP -= 1
    return STACK[SP]

def store():
    val, addr = pop(), pop()
    assert addr < len(HEAP)
    print(f"STORE HEAP[{addr}] = {val}")
    HEAP[addr] = val

def retrieve():
    addr = pop()
    assert addr < len(HEAP)
    print(f"RETRIEVE HEAP[{addr}] (= {HEAP[addr]})")
    push(HEAP[addr])

def in_ascii():
    addr = pop()
    assert addr < len(HEAP)
    ch = sys.stdin.read(1)
    print(f"HEAP[{addr}] = {ch}")
    HEAP[addr] = ord(ch)

def in_num():
    addr = pop()
    assert addr < len(HEAP)
    n = ""
    while (ch := sys.stdin.read(1)).isdigit():
        n += ch
    print(f"HEAP[{addr}] = {n}")
    HEAP[addr] = int(n)

def out_ascii():
    n = pop()
    sys.stdout.write(chr(n))
    sys.stdout.flush()

def out_num():
    n = pop()
    sys.stdout.write(str(n))
    sys.stdout.flush()

def dup():
    print("DUP")
    push(STACK[SP - 1])

def swap():
    print("SUB")
    STACK[SP - 1], STACK[SP - 2] = STACK[SP - 2], STACK[SP - 1]

def add():
    a, b = pop(), pop()
    print(f"{b} + {a} = {a + b}")
    push(b + a)

def sub():
    a, b = pop(), pop()
    print(f"{b} - {a} = {a - b}")
    push(b - a)

def mult():
    a, b = pop(), pop()
    print(f"{b} * {a} = {a * b}")
    push(b * a)

def div():
    a, b = pop(), pop()
    print(f"{b} / {a} = {a // b}")
    push(b // a)

def mod():
    a, b = pop(), pop()
    print(f"{b} % {a} = {a % b}")
    push(b % a)

def xor():
    a, b = pop(), pop()
    print(f"{b} ^ {a} = {a ^ b}")
    push(b ^ a)

def end():
    exit()


OP_CODES = {
    "\t\t ": store,
    "\t\t\t": retrieve,
    "\t\n\t ": in_ascii,
    "\t\n\t\t": in_num,
    "\t\n  ": out_ascii,
    "\t\n \t": out_num,
    "  ": push,
    " \n ": dup,
    " \n\t": swap, 
    " \n\n": pop,
    "\t   ": add,
    "\t  \t": sub,
    "\t  \n": mult,
    "\t \t ": div,
    "\t \t\t": mod,
    "\t \t\n": xor,
    "\n\n\n": end,
}


with open("../src/program.ws") as f:
    code = f.read()

while code:
    for pattern, func in OP_CODES.items():
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
            code = code[len(bits) + 2:]

            func(int(n))
        else:
            func()

        break
    else:
        print("SOMETHING WENT WRONG")
        exit()
