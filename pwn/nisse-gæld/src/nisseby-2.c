#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "aes.h"

unsigned int day = 1;

unsigned int money = 0;
unsigned int debt = 10000000;
bool hint1_bought = false;
bool hint2_bought = false;

bool has_worked = false;

static const uint8_t key[16] = "NISSEKEY_FRA_MIG";
static const uint8_t iv_mask[16] = "HYGGELIG_JULETID";
static const uint8_t xor_mask1[16] = "XOR_MASKE_#1_HER";
static const uint8_t xor_mask2[16] = "NUMMER2_XORMASKE";

static uint8_t hint1_enc[80] = "\x51\x23\x4b\x48\x68\x61\xe8\x87\x54\x65\x90\xd8\x56\xc7\xad\xbe\x5c\x16\x68\x23\xee\xc0\x57\x44\x94\xb9\x65\x43\x4c\xe0\xbd\x05\x84\xeb\x71\x6c\x5e\xb1\x40\x59\xfb\xcb\x2d\x4d\x25\x8f\x70\xa4\xe2\xeb\xaa\x87\x3d\x12\x2b\x5f\x41\x3c\x11\xa4\x42\x0e\x41\xd7\xe5\xe7\x93\x25\x69\x32\xf0\xa7\xfc\xe1\x65\x13\x39\x0e\xf0\xf9";
static const uint8_t hint1_iv[16] = "FRITZ_HINT_1_IV!";

static uint8_t hint2_enc[80] = "\x2f\x5d\x08\xe4\xf0\x76\x8a\x86\x1e\x20\x15\x37\xbc\x6e\x97\xa5\x1f\xfa\x5d\x3c\xe7\x1d\xa7\x63\x32\xf3\xf7\x6a\x9b\x29\x60\xce\x56\x26\xe2\x8a\x5f\xec\xe3\x51\xaf\xbb\xc6\xbd\x24\xe4\x63\xef\xbf\xa3\x3d\xfb\x93\x55\x0b\x46\xa2\x35\x7b\x7c\x52\x69\xa7\x77\xe9\x78\xc7\x69\xb5\x87\x3c\x8b\xd1\x5b\x94\x45\xc4\xd9\x58\x13";
static const uint8_t hint2_iv[16] = "IV_TIL_HINT_NR_2";


void init() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}


void d(uint8_t *ct, uint8_t* pt, const uint8_t *iv_param, size_t length) {
    // Create the IV by XORing iv_param with iv_mask
    uint8_t iv[16];
    for (int i = 0; i < 16; i++) {
        iv[i] = iv_param[i] ^ iv_mask[i];
    }

    struct AES_ctx ctx;
    AES_init_ctx_iv(&ctx, key, iv);

    for (int i = 0; i < length; i++) {
        pt[i] = ct[i] ^ xor_mask1[15 - (i % length)];
    }

    AES_CBC_decrypt_buffer(&ctx, pt, length);

    for (int i = 0; i < length; i++) {
        pt[i] ^= xor_mask2[15 - (i % length)];
    }
}


void work() {
    if (has_worked) {
        puts("Du kan kun arbejde én gang om dagen!");
        return;
    }

    puts("🛠️ Velkommen på værkstedet 🛠️");
    puts("Fritz bruger hele dagen på at lave gaver...");
    for (int i = 0; i < 20; i++) {
        usleep(100000);
        printf("🎁");
    }
    usleep(500000);

    puts("\nDu har arbejdet en lang dag og tjent ❄️100!");
    puts("Desværre går ❄️50 til afbetaling på din gæld");
    money += 50;
    debt -= 50;
    has_worked = true;
}


void sleepy() {
    puts("Fritz går i seng og drømmer sødt om sne, risengrød og gældssanering...");
    for (int i = 0; i < 10; i++) {
        usleep(200000);
        printf("💤");
    }
    usleep(500000);
    puts("");

    day++;
    has_worked = false;
}


void store() {
    int choice;

    while (true) {
        puts("🛒 Velkommen i Frosto, hvad vil du købe? 🛒");
        puts("1. Julegløgg\t❄️50");
        if (hint1_bought) {
            puts("2. Hint\t\t❄️0 (KØBT)");
        } else {
            puts("2. Hint\t\t❄️500");
        }
        if (hint2_bought) {
            puts("3. Hint\t\t❄️0 (KØBT)");
        } else {
            puts("3. Hint\t\t❄️1.337");
        }
        puts("4. Flag\t\t❄️0 (KØBT)");
        puts("5. Gå tilbage");
        printf("> ");

        scanf("%d", &choice);
        puts("");

        switch(choice) {
            case 1:
                if (money >= 50) {
                    puts("Du har købt en varm kop julegløgg! Mmmm...");
                    money -= 50;
                    return;
                } else {
                    puts("Du har ikke råd til julegløgg!");
                }
                break;
            case 2:
                if (money < 500 && !hint1_bought) {
                    puts("Du har ikke råd til hint 1!");
                    break;
                }

                uint8_t hint1[80];
                d(hint1_enc, hint1, hint1_iv, 80);
                printf("Hint 1: %s\n", hint1);

                if (!hint1_bought) {
                    money -= 500;
                    hint1_bought = true;
                }
                return;
            case 3:
                if (money < 1337 && !hint2_bought) {
                    puts("Du har ikke råd til hint 2!");
                    break;
                }

                uint8_t hint2[80];
                d(hint2_enc, hint2, hint2_iv, 80);
                printf("Hint 2: %s\n", hint2);

                if (!hint2_bought) {
                    money -= 1337;
                    hint2_bought = true;
                }
                return;
            case 4:
                puts("Ja, du har ligesom allerede snydt dig til dit pensionsflag, det er jo derfor, du har gigantisk gæld, mester...");
                break;
            case 5:
                return;
            default:
                puts("Ugyldigt valg! Prøv igen.");
        }
        puts("");
    }
}


void ansoeg() {
    char reason[1000];
    char name[100];
    int nisse_id;
    int amount;

    puts("Udfyld ansøgningsskemaet nedenfor for at ansøge Froststyrelsen om gældsnedsættelse.");

    puts("+--------------------------------------------------------------------+");
    printf("| Fuldt navn: ");
    fgets(name, sizeof(name), stdin);
    name[strcspn(name, "\n")] = 0;

    printf("| NisseID: ");
    scanf("%d", &nisse_id);
    getchar();

    printf("| Ønsket nedsættelse: ");
    scanf("%d", &amount);
    getchar();

    printf("| Begrundelse: ");
    fgets(reason, 1024, stdin);

    puts("+--------------------------------------------------------------------+");

    puts("\nTak for din ansøgning! Du vil modtage svar inden for 1-10.000 dage");
}


void login_froststyrelsen() {
    puts("❄️ Velkommen til Froststyrelsen ❄️");
    system("/bin/sh");
}


int main() {
    init();

    puts("🎄 Velkommen til Nisseby! 🎄");
    puts("Hjælp Fritz med at betale hele sin gæld af!");

    int choice;
    while (true) {
        printf("\nDag %d - du har ❄️%d i gæld og ❄️%d til rådighed\n", day, debt, money);
        puts("1. 🛠️ Arbejd på værkstedet");
        puts("2. 💤 Sov");
        puts("3. 🛒 Gå i Frosto");
        puts("4. 💸 Ansøg om gældssanering");
        puts("5. 👋 Afslut");
        printf("> ");

        scanf("%d", &choice);
        getchar();
        puts("");

        switch(choice) {
            case 1:
                work();
                break;
            case 2:
                sleepy();
                break;
            case 3:
                store();
                break;
            case 4:
                ansoeg();
                break;
            case 5:
                puts("🎄 Farvel og glædelig jul! 🎄");
                return 0;
            default:
                puts("Ugyldigt valg! Prøv igen.");
        }
    }

    return 0;
}
