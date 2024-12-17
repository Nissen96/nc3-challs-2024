import random

plaintext = """
Kære Julemand,

Jeg håber, du har det godt oppe på Nordpolen, og at Rudolf og de andre rensdyr får masser af gulerødder.

Jeg ønsker mig:
- At alle verdens børn kan få mad nok og en god familie
- At ingen må være ensomme og alene i julen
- NC3{fr3d_på_j0rd_0g_0gså_1_rumm3t}
- En kæmpe Flexi Trax bane

Mange kærlige hilsner
Magnus, 7 år
""".lower().strip()

alphabet = "abcdefghijklmnopqrstuvwxyzæøå"
chars = ["🍮", "⛷️", "⛪", "🌟", "🤶", "🎅", "✨", "🎄", "🎀", "🎁", "🧣", "🧤", "⛸️", "🥌", "🎿", "🛷", "🏒", "🔔", "🕯️", "📜", "🍪", "☕", "🏔️", "🌨️", "❄️", "☃️"]
random.shuffle(chars)
pos = 0

mapping = {}

ciphertext = ""
for c in plaintext:
    if c == " ":
        ciphertext += "  "
    elif c in mapping:
        ciphertext += mapping[c]
    elif c not in alphabet:
        ciphertext += c
    elif pos > len(chars):
        print("Not possible")
        exit()
    else:
        mapping[c] = chars[pos]
        pos += 1
        ciphertext += mapping[c]


print(ciphertext)
