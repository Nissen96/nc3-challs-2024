# Writeup

## tl;dr

`n` er triviel at primtalsfaktorisere med kvadratrod pga. genbrug af `p`.
Herefter findes `φ(n) = p * (p - 1)` og `d = e^-1  mod φ(p)`, hvorefter flag dekrypteres med `d`.

## Introduktion

I RSA benyttes normalt to store primtal `p` og `q` til at generere `n = p * q`, og en krypteringsnøgle `e` vælges.
Dekrypteringsnøglen `d` er den inverse af denne, og for at finde den, skal bruges `φ(n)`.
For to forskellige primtal gælder, at `φ(p * q) = (p - 1) * (q - 1)`.

Det smarte ved RSA er derved, at når man kender `p` og `q`, kan man finde dekrypteringsnøglen helt trivielt og effektivt, men kender man *ikke* disse, er der ikke en generel effektiv metode til at finde `φ(n)`.

Sikkerheden består derfor i, at det er ekstremt tidskrævende at primtalsfaktorisere `n` til `p` og `q`, eller alternativt at udregne `φ(n)` direkte fra `n` uden at kende dens faktorer.

## Exploit

Usikkerheden i opgaven her består i, at `p` er blevet genbrugt to gange, i stedet for at vælge to uafhængige primtal:

```py
p = getPrime(512)
q = p
n = p * q
```

Det betyder, at `n = p^2`, og dermed kan `p` helt trivielt findes som kvadratroden af `n`, fx med `gmpy2` modulet til håndtering af store tal:

```py
# pip install gmpy2
from gmpy2 import iroot

p = iroot(n, 2)[0]
```

Nu kan `φ(n)` findes. Her skal man være opmærksom på, at formlen er `φ(p * p) = p * (p - 1)` for to *ens* primtal.
Den generelle formel kan findes [her](https://en.wikipedia.org/wiki/Euler%27s_totient_function#Euler's_product_formula). Med `φ(n)` kan `d` findes og ciphertext dekrypteres:

```py
phi = p * p - 1
d = pow(e, -1, phi)

m = pow(ct, d, n)
```

Se fuldt solve script [her](../solution/solve.py).

Flag: `NC3{3t_pr1mt4l_1_hånd3n_3r_b3dr3_3nd_t0_på...3ll3r_v3nt}`
