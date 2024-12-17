#!/usr/bin/env python3

from Crypto.Cipher import AES

# Kodebog der aldrig løber tør!
from secret import FLAG, CODEBOOK


def encrypt(pt, key, iv=None):
    # Genererer og returnerer tilfældig engangskode, hvis ikke defineret
    cipher = AES.new(key, mode=AES.MODE_CFB, iv=iv)
    return cipher.encrypt(pt), cipher.iv


def derive_key():
    # Udled krypteringsnøgle fra nøglenissens kodebog og postnissens kodeord
    shared_key = CODEBOOK.next()
    post_key = input_hex("Postnisse kodeord: ", 32)
    if post_key is None:
        return None

    post_password, post_iv = post_key[:16], post_key[16:]
    enc_key, _ = encrypt(post_password, shared_key, post_iv)
    return enc_key


def input_hex(prompt, length=16):
    try:
        hx = bytes.fromhex(input(prompt))
    except ValueError:
        print("Der var noget galt med dit hex input!")
        return

    if len(hx) == length:
        return hx

    print(f"Input skal være {length} bytes")
    return


def main():
    print("********************************")
    print("*  PostNordpolens Postcentral  *")
    print("*            Uge 49            *")
    print("********************************")

    while True:
        print()
        print("1. Afhent breve til udlevering")
        print("2. Krypter og afsend besked")
        print("3. Afslut arbejdsdag")
        choice = input("> ")
        print()

        if choice == "1":
            if (key := derive_key()) is None:
                continue

            ct, iv = encrypt(FLAG, key)
            print(f"\nDu har 1 brev klar til udlevering: {ct.hex()}")
            print(f"Engangskode - udlever kun til modtager: {iv.hex()}")

        elif choice == "2":
            msg = input("Besked: ")
            addr = input("Adresse: ")

            if (key := derive_key()) is None:
                continue

            ct, _ = encrypt(msg.encode(), key)
            print(f"\nAfsendt til {addr}: {ct.hex()}")

        elif choice == "3":
            print("Tak for i dag, husk at registrere dine timer!")
            break

        else:
            print("Ugyldigt valg :(")


if __name__ == "__main__":
    main()
