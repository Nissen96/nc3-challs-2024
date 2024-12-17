# PostNordpolen III

Tredje gang er lykkens gang - kryptonisserne har endnu engang udskiftet kryptosystemet, og det er sikrere nu end nogensinde!

Nøglenisserne deler stadig en kodebog, men nu har hver postnisse også sit eget kodeord, kun de kender!
Når en postnisse afhenter et brev, udledes en krypteringsnøgle fra *begge* disse dele.

Herudover genereres en tilfældig engangskode til krypteringen, som postnissen får udleveret.

Når postnissen afleverer brevet, skal denne indtaste sit kodeord og den tilfældige engangskode, og først der kan den modtagende nøglenisse udlede den rigtige dekrypteringsnøgle.

På den måde kender ingen alle hemmeligheder, og nu burde både postnisser og selv uvedkommende nøglenisser være forhindrede i at snage!

**Opklarende info:** Kodebogen er ikke ændret fra PostNordpolen II, den indeholder stadig helt tilfældige og uendeligt mange værdier, der aldrig cycler. Den er uden for scope og kan funktionelt erstattes med `os.urandom(16)` uden at ændre på løsningen.

[https://tryhackme.com/jr/postnordpoleniii2o24](https://tryhackme.com/jr/postnordpoleniii2o24)

Forbind med: `nc <tildelt-ip> 1337`

- [postnordpolen-3.py](src/postnordpolen-3.py)
