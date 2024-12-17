# Writeup

PCAPen kan åbnes i Wireshark, hvor der primært er TLS-krypteret trafik.
Der findes dog ukrypterede undtagelser, alle fra én IP.
Denne client besøger en række sider over HTTP, og vi ser han også har en samtale over en ukrypteret custom protokol:

```
#START CHAT#

#CHAT ACCEPTED#

#MSG# Hallo, Krynfsk her, er der nogen fra IT-support?

#MSG# Ja mig, Grompf
#MSG# Det her er en gammel ukrypteret kanal, den må du slet ikke bruge, alt skal være krypteret nu!

#MSG# Ehhm, jeg har muligvis ved en fejl slået TLS fra og ved ikke, hvordan jeg får sat det op igen

#MSG# Jeg bliver så træt...
#MSG# Nå, men det burde være hurtigt at fikse, vi bruger samme RSA-nøgle til alt og alle i Kaos A/S, det var nemmest

#MSG# Nåååårh, ja jeg faldt godt over en private key i din rodekasse på fællesdrevet, det må være den!

#MSG# Ehhh, den troede jeg, jeg havde slettet igen... Det gør jeg lige med det samme...

#MSG# Bare rolig, hvis du mister den, kan vi altid genskabe den!

#MSG# Øhhhh hvad?!?

#MSG# Ja ja! Flomfq hjalp mig med at uploade primtallene til en online faktor database, så vi altid kan slå dem op igen ud fra public key!

#MSG# Det er simpelthen løgn, hvis en nisse får fat i den, er vi færdige hele bundtet...

#MSG# Skal jeg lige sende den, så du kan tjekke, om det er den rigtige?

#MSG# NEJ NEJ NEJ, du må endelig ikke sende den til nogen og ISÆR ikke over en ukrypteret kanal!
#MSG# Den private nøgle bruges af serveren til at opsætte TLS sessions - enhver der har den kan dekryptere ALT!

#MSG# Nå nå, ingen grund til at blive sur... Jeg kommer bare forbi dit kontor i stedet
#END CHAT#

#CHAT ENDED#
```

Krynfsk skulle altså have haft benyttet TLS kryptering til alt, og der findes en RSA private key, der kan dekryptere alt. Den vil vi gerne have, så vi ser på de handshakes, der laves - specifikt i SERVER HELLOs.

Her ser vi, at den benyttede cipher suite er `TLS_RSA_WITH_AES_256_GCM_SHA384`, så RSA som forventet.
Ser vi i certifikat felterne, finder vi issuer info om det benyttede certifikat:

```
Country: GN
State or province: Region Grum
Locality: Brokhøj
Organization: Kaos A/S
Unit: Afdelingen for Julens Undergang
Common name: julens-undergang.gnom
Email: support@kaos.gnom
```

Herudover kan vi finde info om RSA public key under subjectPublicKeyInfo -> subjectPublicKey

```
modulus: 0x00d0fc206f734aa02e5ff4f05bf6e61e2360d29c2b6ee1f4d77d728f1cfdad8c7aa28fbe41518708ea8eb822bfd1921fdd4cdbb3b2d155db4b9814b5cb527df7eb6a0b93aa7db457d6523b131da06b1fb412218f04cdf8d152b745d025fb70f8f8e9f787813e969e200fa893f55b4b15a2c2fc88db18416e252def94f86a6a2171fd011374cf7de7f22e0bd4e9e4499f935b0d5cf2ec02f68c2b25776430706781a28eb9e1748806ec2a1bfb7a18ed262ba674bdc0d5821ec0ec1ba303e68566bf4a9c3b1ccaca42bcb574bf26f5a1c512b1addd3f12f6f141e5f973eaae77f1fd6d6ed8d9d1741d40cd53879cbb7d0a9bdf89bdb06f5d5ebb89363fbf211ad767

publicExponent: 65537
```

Chatten hinter ret kraftigt til, at de tilhørende primtalsfaktorer er blevet uploadet til en online database. Har man bare lidt kryptoerfaring vil tankerne hurtigt ledes hen på [https://factordb.com](https://factordb.com), der også er helt standard lige at tjekke alle offentlige nøgler, man finder på. Slår man nøgken op her, finder man, den faktisk har gemt de to faktorer:

```
p = 150346507085147942241260814838443844698294368178800410029288378094628423223149337889414668267565279907694101416395335155546160512355319089478896177309669681424162499407448014533532723980897709501614098395104150473244440063208482280406434854761645777823683470893940658656232939655902756570427621987734645860231

q = 175473951834764860743916816952668434826567713396775241028829896253119594591766833162822942385799516376444130938331581045784438872239049635510789226186957047303322976652648655683321813754650264193151406519524988772975610030536261392876607740935754517606917491374983996564248660137839943303139906207315957860641
```

Fra disse, kan vi finde `phi(n) = (p - 1) * (q - 1)` og herfra dekrypteringsnøglen `d = e^-1  mod phi(n)`. Med Python kan vi nu finde private key og gemme den i et PEM-format, Wireshark kan loade ind:

```py
from Crypto.PublicKey import RSA

n = 0x00d0fc206f734aa02e5ff4f05bf6e61e2360d29c2b6ee1f4d77d728f1cfdad8c7aa28fbe41518708ea8eb822bfd1921fdd4cdbb3b2d155db4b9814b5cb527df7eb6a0b93aa7db457d6523b131da06b1fb412218f04cdf8d152b745d025fb70f8f8e9f787813e969e200fa893f55b4b15a2c2fc88db18416e252def94f86a6a2171fd011374cf7de7f22e0bd4e9e4499f935b0d5cf2ec02f68c2b25776430706781a28eb9e1748806ec2a1bfb7a18ed262ba674bdc0d5821ec0ec1ba303e68566bf4a9c3b1ccaca42bcb574bf26f5a1c512b1addd3f12f6f141e5f973eaae77f1fd6d6ed8d9d1741d40cd53879cbb7d0a9bdf89bdb06f5d5ebb89363fbf211ad767
e = 0x10001

p = 150346507085147942241260814838443844698294368178800410029288378094628423223149337889414668267565279907694101416395335155546160512355319089478896177309669681424162499407448014533532723980897709501614098395104150473244440063208482280406434854761645777823683470893940658656232939655902756570427621987734645860231
q = 175473951834764860743916816952668434826567713396775241028829896253119594591766833162822942385799516376444130938331581045784438872239049635510789226186957047303322976652648655683321813754650264193151406519524988772975610030536261392876607740935754517606917491374983996564248660137839943303139906207315957860641

phi = (p - 1) * (q - 1)
d = pow(e, -1, phi)

key = RSA.construct((n, e, d, p, q))

with open("rsakey.pem", "wb") as f:
    f.write(key.export_key("PEM"))
```

Det giver følgende RSA key:

```
-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEA0Pwgb3NKoC5f9PBb9uYeI2DSnCtu4fTXfXKPHP2tjHqij75B
UYcI6o64Ir/Rkh/dTNuzstFV20uYFLXLUn3362oLk6p9tFfWUjsTHaBrH7QSIY8E
zfjRUrdF0CX7cPj46feHgT6WniAPqJP1W0sVosL8iNsYQW4lLe+U+GpqIXH9ARN0
z33n8i4L1OnkSZ+TWw1c8uwC9owrJXdkMHBngaKOueF0iAbsKhv7ehjtJiumdL3A
1YIewOwbowPmhWa/Spw7HMrKQry1dL8m9aHFErGt3T8S9vFB5flz6q538f1tbtjZ
0XQdQM1Th5y7fQqb34m9sG9dXruJNj+/IRrXZwIDAQABAoIBAHBM290n9hUHdpb3
xmNxmwZl1CcJi+cuG9IUimUIyIaxq8NUeGMoDhmFIdvCegpsxw2zDehsZxeVkp6m
ZiDpAh1l+dybBDux68B6cDY+avI5YHjaErngGBO72m8Uyf4WPCP12MIR8Pv9vIxZ
HcK2IWU6JFwiZ/FZD++US9gFzwwy7G5hZmuY36gw7vlBqj1bhqpxIbkVmU2xzbXl
9dveN8y/UMPIbbw8plpwkBkI+Nm+WbR+0PJ6H5hYaEnddZgbVUvL17ZftgCslOAv
1oBuFGOfFY0/CaaMzejtTVYEoiJnoNuA4IWowYtLIVVECZU+jAPj/nBxVqcNvtnO
fY71ssECgYEA1hm8he3Yt4SWgaY5t6N+KKJlH4fAheAptu9KDU/zQeR/IkvnmPPY
H4dN+jpZfws54Cj351ie2+OOIJbbXYmWlDotuv/X9F6dKoN0cRm8DADUhXak/hXI
OxHrzk6Nldu/1MZ3eGxZdbHOx3GjurIopXNu168JQIhx2RBppyJDZ4cCgYEA+eIZ
hjRpEia964fEjb5jvbT5IWxd8QHrxDnfTH9qSSVgj6uHw3vbcjw+cs/HjtN41zSO
9rj1xKGg8Khlvu6A9bx8WDfR3eu4+jT0rnT7msYboq5ftAcJbmqnyA5uCZogswPU
PbxL3ZrWl05+0r1vBRTD7zZfC9iW29ioE7IzSSECgYB2rpOTxlIRAP2RZvytsIKZ
sdPOk6kETUuybZkmIgCdsTVMZLlAT0Opzo5KPJgp1aZCfVNWughtqgm6RQXbJw8C
ofGBrJsgimYjD/W3UGWuXbNxPGCfvKFfJUMK/P59aPBA2beWWLGKjYMrifIR5vqj
JIb4Jr5BOKGriu6WSGcG9wKBgB5Q5wXYL/MqzhnYI+mKcrFeVmdOrWsC76aj2sp+
Htf29+sWRWdbDHmkg3MMcEqMr3l0f+/A6thLP6pS091BNFYb4v4U75o78foxGIpd
2PSjGlE3VJcTz3oc6HQmBAWYNGVjjola4d1l3qkGte49W03Dgi3wa8GVKmBLvcB9
+yjhAoGBANVqH+hOjgSYYa9E+PjhFbMlplGPwxJ1wLiYm9WOmAIhjuF0I+JRQvOK
W2+rI39WFC5i8eQbLzPSnVWhCrpMzGsXpQpxYakU658Bds80VGeUTXDVNitX4dgN
y8mOfbF6aGF+U4uaW56CJO+/5n8cREGL6JzfHOHGIo2Sr4z/2v9l
-----END RSA PRIVATE KEY-----
```

I Wireshark kan denne loades ind ved at gå til `Edit -> Preferences... -> Protocols -> TLS -> RSA keys list` og klikke `Edit`. Klik `+` her og under `Key file` browse til den gemte `rsakey.pem`. Klik `OK` og `Apply`, så anvendes den helt automatisk til dekryptering, hvor den kan.

Det virker, og nu har vi adgang til en række ekstra streams, inklusive flere mails. Den sidste er (UTF-8 decoded):

```
From: Gnoklios <ceo@kaos.gnom>
To: Afdelingen for Julens Undergang <undergang@kaos.gnom>
Subject: Operation Julens Undergang

Alle gnomer i Kaos A/S!

Tiden er kommet til den største operation mod Nisseland til dato!
Nisserne er travle med juleforberedelserne og er ikke opmærksomme på deres omgivelser.
Vi har over den seneste måned infiltreret deres værksteder og saboteret legetøjet,
så de er mere pressede end nogensinde før.

Operation Julens Undergang begynder på torsdag lige efter deres frokostpause
 - en tyk nisse er en langsom nisse.

Det er EKSTREMT vigtigt, denne information bliver i Kaos A/S.
Hvis bare en enkelt snagende nisse får fat på informationen med sine klamme korte fingre,
er hele operationen kompromiteret.

NC3{d3jl1g_3r_jul3n_pr@gt1g_3r_d3ns_und3rg4ng}

Julen bliver endelig vores!
Gnoklios, CEO Kaos A/S
```

## Flag

`NC3{d3jl1g_3r_jul3n_pr@gt1g_3r_d3ns_und3rg4ng}`
