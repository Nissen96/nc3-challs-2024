# Writeup

## tl;dr

Kryptering er bare multiplikation med en fast key modulo primtal `P`.
Dvs. dekryptering er blot multiplikation med den inverse key modulo `P`.
Key kan leakes med ét kendt plaintext-ciphertext par, fx første flag char.

## Introduktion

Det udleverede program er relativt simpelt:

```py
from random import randint

# 512-bit prime
P = 13187894026947502600331395231459335882158393410614133036296342117478704820555154018132946245287063906492618556075499328589037764675831105264487871422591331

def encrypt(pt, key):
    ct = []
    for c in pt:
        ct.append((c * key) % P)
    return ct

key = randint(2**510, 2**511)
ct = encrypt(flag, key)
```

Der vælges en tilfældig stor `key`, som benyttes til at kryptere flaget.
Kryptering sker på hver karakter `c` i plaintext individuelt og er modulær multiplikation: $c \cdot key \mod P$, hvor $P$ er et hardcoded stort primtal.

Men hvordan ser dekryptering så ud, når operationen er modulær?

## Modulær Multiplikation

Vi arbejder her med heltal modulo $P$, og her er den modsatte operation af multiplikation ikke division, som vi normalt kender det. Det gælder altså *ikke* at

$$ ct \equiv pt \cdot key \mod P \quad \Leftrightarrow \quad \frac{ct}{key} \equiv pt \mod P $$

i hvert fald ikke, hvis vi forstår $\frac{ct}{key}$ som almindelig division. Vi kan dog også forstå almindelig division som, at vi ganger med det inverse af et tal. Så

$$ \frac{a}{a} = a \cdot a^{-1} $$

og $a^{-1}$ er det tal, der giver $1$, når vi ganger det med $a$:

$$ a \cdot a^{-1} = 1 $$

Det er samme princip vi bruger i modulær aritmetik. Her vil (nogle) tal $a$ have en *modulær multiplikativ invers*, $a^{-1}$, som ligesom før er det tal, der sikrer at

$ a \cdot a^{-1} \equiv 1 \mod p $

For altså at komme fra $pt \cdot key \mod P$ til $$pt$$, skal vi finde $key$s modulære multiplikative invers modulo $P$ og gange med den, da

$$ pt \cdot key \cdot key^{-1} \equiv pt \cdot 1 \equiv pt \mod p $$

Hvordan finder vi den? Til det kan man bruge *Euklids udvidede algoritme*. Forklaringen bliver lidt teknisk skippes her, men i Python er det meget nemt: Det er indbygget i `pow` funktionen, så for at finde $key^{-1} \mod P$ kan du bruge `pow(key, -1, P)`, så klarer Python det bagvedliggende.

## Exploit

Vi kan nu skrive en dekrypteringsalgoritme, der tager et ciphertext array og en `key` og finder den modulære inverse af denne `key`. Denne ganges herefter blot på hvert array element for at dekryptere:

```py
def decrypt(ct, key):
    dec_key = pow(key, -1, P)
    pt = []
    for c in ct:
        pt.append((c * dec_key) % P)
    return bytes(pt)
```

Men hvordan får vi leaket den benyttede `key`?
Vi kan igen se på den modulære multiplikation, specifikt for første karakter vi kender - `'N'`:

$$ ct[0] \equiv \texttt{'N'} \cdot key \mod P \quad \Leftrightarrow \quad key \equiv ct[0] \cdot \texttt{'N'}^{-1} \mod P $$

Dvs. vi kan faktisk få `key` direkte ved at finde den modulære inverse for `'N'` og gange på første ciphertext tal - i Python:

```py
key = (ct[0] * pow(ord("N"), -1, P))  % P
```

Denne kan bruges med vores decryption funktion til at dekryptere flaget.

Se fuldt solve script [her](../solution/solve.py).

Flag: `NC3{https://www.cryptoisnotcryptocurrency.com/}`
