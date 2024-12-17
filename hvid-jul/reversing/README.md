# Hvid Jul: Reversing

#### Intro

I Nisseland skal alt holdes meget hemmeligt, og derfor udvikles alt i sproget [Whitespace](https://esolangs.org/wiki/Whitespace), så programmer er usynlige for nysgerrige blikke.

Udviklingsnisserne har skrevet deres egen fortolker til sproget, de selv kan udvide med praktiske instruktioner 👀 Det har også den fordel, at eksisterende interpreters og compilers ofte fejler.

*Den udleverede interpreter binary er identisk for begge `Hvid Jul` opgaver.*

#### Opgaven

Julemanden har fået udviklet en kryptomat i sproget, så han sikkert kan sende beskeder til Påskeharen og bl.a. koordinere, hvornår butikkerne skal skifte mellem at sælge påskeæg og pebernødder.

Den er godt nok hardcoded til beskeder på 48 karakterer, men udviklernisserne har for travlt til at generalisere den.

Kan du reverse programmet og dekryptere hans seneste besked?

**Tip:** Programmet kan fx køres ved at starte `./interpret` og paste Whitespace indholdet. Alternativt kan det ønskede input skrives i en tekstfil og program plus input indlæses med

```cmd
$ cat hvid-jul.ws input.txt | ./interpret
```

- [hvid-jul-reversing.zip](src/hvid-jul-reversing.zip)
