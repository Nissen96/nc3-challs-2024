#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <unistd.h>
#include "aes.h"

unsigned int day = 1;

unsigned int money = 0;
unsigned int money_spent = 0;
bool hint1_bought = false;
bool hint2_bought = false;

bool has_worked = false;

static const uint8_t key[16] = "NISSEKEY_TIL_DIG";
static const uint8_t iv_mask[16] = "JULETID_ER_HYGGE";
static const uint8_t xor_mask1[16] = "EN_XOR_MASKE_HER";
static const uint8_t xor_mask2[16] = "EKSTRA_XOR_MASKE";

static uint8_t hint1_enc[80] = "\x41\x85\x01\x6f\xb5\xb6\x08\x04\xfa\x23\x46\xf5\x4e\x12\xb6\x37\x90\xc9\xb3\x07\xb9\x5c\x7d\x2f\xa5\x39\x05\x5a\x92\x19\x92\xc8\x4a\x6c\xb4\xea\xfb\x99\x7f\x0f\xa3\xc4\xe6\xd2\x87\xd9\x2c\x7e\x4f\x94\x08\x57\x0f\x72\x62\x24\x5f\x1e\xd0\x2a\xa0\x1f\x67\x1c\x0c\x0c\x79\xf6\x0e\x9e\x74\xc6\x8a\x00\x39\x7d\x6c\xa4\xd0\x78";
static const uint8_t hint1_iv[16] = "HINT1_TIL_FRITZ!";

static uint8_t hint2_enc[128] = "\x16\x01\x47\x6b\xff\x68\xba\x31\x68\x3a\x95\xab\x6e\xdc\xc0\x21\x85\xea\x99\x76\x7b\x89\xff\x79\x6c\x3d\x2e\xe7\x90\xce\xa9\xe1\x5d\x6b\xa1\x75\x3b\x92\xf7\x08\x76\xb6\xc0\x7d\x7f\x6d\xde\xd2\xf1\x3d\x49\xc6\xff\xb5\x12\x8c\x13\x37\x69\x48\xe8\x4e\x80\xc0\xb9\xc9\x32\x46\xd1\x7b\x8c\xbb\x59\x57\xca\x31\xaa\xc3\x90\xe7\xd5\xd5\x3c\x41\x47\x5b\x5d\x0b\x21\x17\x53\x8b\x46\xb3\x8c\xbf\xb5\x1d\x2e\x0b\x5a\xd9\x5e\x2b\x17\xc5\xab\x25\x5c\x67\xc8\x46\xa3\x78\xa3\xa6\x0c\x9b\x11\xa1\xc0\xeb\xb8\xc0\x89\x0d\x75\x71";
static const uint8_t hint2_iv[16] = "HER_ER_IV_HINT2!";

static uint8_t flag_enc[64] = "\x6d\x0a\x37\x61\xbe\x6c\x0c\x5a\xcc\xc2\x27\xdb\xc3\x92\xd0\x19\xb2\x9e\xc5\x31\x0b\xe2\xd9\x82\x74\x43\xec\x31\x7e\x06\x23\x2d\x9e\xcc\x32\x53\xe5\x22\x82\xee\x43\xa4\xe3\x31\xf6\x17\xd9\x7f\x77\x8d\x68\xf8\x8e\xa8\x4e\x5c\x11\x5d\xeb\x37\x1a\xc0\x9f\xaa";
static const uint8_t flag_iv[16] = "\xab\xfe\x34\x3f\x91\x01\x23\xff\xfe\xad\x2a\x10\x99\x89\x0a\x1c";


void init() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}


void validate() {
    if (money + money_spent > 100 * day) {
        puts("Hov hov, du prøver da at snyde!");
        exit(1);
    }
}


void d(uint8_t *ct, uint8_t* pt, const uint8_t *iv_param, size_t length) {
    validate();

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
    money += 100;
    has_worked = true;
}


void sleepy() {
    puts("Fritz går i seng og drømmer sødt om sne og risengrød...");
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
        puts("4. Flag\t\t❄️10.000.000");
        puts("5. Gå tilbage");
        printf("> ");

        scanf("%d", &choice);
        puts("");

        switch(choice) {
            case 1:
                if (money >= 50) {
                    puts("Du har købt en varm kop julegløgg! Mmmm...");
                    money -= 50;
                    money_spent += 50;
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
                    money_spent += 500;
                    hint1_bought = true;
                }
                return;
            case 3:
                if (money < 1337 && !hint2_bought) {
                    puts("Du har ikke råd til hint 2!");
                    break;
                }

                uint8_t hint2[128];
                d(hint2_enc, hint2, hint2_iv, 128);
                printf("Hint 2: %s\n", hint2);

                if (!hint2_bought) {
                    money -= 1337;
                    money_spent += 1337;
                    hint2_bought = true;
                }
                return;
            case 4:
                if (money >= 10000000) {
                    uint8_t flag[64];
                    d(flag_enc, flag, flag_iv, 64);
                    printf("🎉 Tillykke! Her er dit flag: %s 🎉\n", flag);
                    exit(0);
                } else {
                    puts("Du skal arbejde meget mere for at få råd til flaget!");
                }
                break;
            case 5:
                return;
            default:
                puts("Ugyldigt valg! Prøv igen.");
        }
        puts("");
    }
}


int main() {
    init();

    puts("🎄 Velkommen til Nisseby! 🎄");
    puts("Hjælp Fritz med at få ❄️ nok til flaget!");

    int choice;
    while (true) {
        printf("\nDag %d - du har ❄️%d\n", day, money);
        puts("1. 🛠️ Arbejd på værkstedet");
        puts("2. 💤 Sov");
        puts("3. 🛒 Gå i Frosto");
        puts("4. 👋 Afslut");
        printf("> ");

        scanf("%d", &choice);
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
                puts("🎄 Farvel og glædelig jul! 🎄");
                return 0;
            default:
                puts("Ugyldigt valg! Prøv igen.");
        }

        validate();
    }

    return 0;
}
