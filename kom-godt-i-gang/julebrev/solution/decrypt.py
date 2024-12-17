with open("../src/julebrev.txt") as f:
    ct = f.read()

# Based on iterative analysis
mapping = {
    "🥌": "N",
    "⛪": "C",
    "🌨️": "K",
    "🎀": "Æ",
    "🛷": "R",
    "🕯️": "E",
    "🏒": "O",
    "🍮": "A",
    "🧣": "L",
    "🎄": "Å",
    "🎿": "M",
    "🎅": "G",
    "☕": "I",
    "✨": "H",
    "🏔️": "S",
    "🌟": "D",
    "🤶": "J",
    "📜": "U",
    "🍪": "P",
    "❄️": "B",
    "⛷️": "T",
    "☃️": "F",
    "⛸️": "Y",
    "🧤": "Ø",
    "🔔": "V",
    "🎁": "X"
}

for e, d in mapping.items():
    ct = ct.replace(e, d)

print(ct)
