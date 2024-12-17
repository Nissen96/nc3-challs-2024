#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <unistd.h>
#include "aes.h"

static const uint8_t key[16] = "NISSEKEY_FRA_MIG";
static const uint8_t iv_mask[16] = "HYGGELIG_JULETID";
static const uint8_t xor_mask1[16] = "XOR_MASKE_#1_HER";
static const uint8_t xor_mask2[16] = "NUMMER2_XORMASKE";

static uint8_t hint1[80] = "Har du mon decompilet og undersøgt koden? Måske gemmer der sig noget brugbart\x00";
static const uint8_t hint1_iv[16] = "FRITZ_HINT_1_IV!";

static uint8_t hint2[80] = "Måske kan Fritz snyde systemet med ekstra data og styre hvor han vil hoppe hen\x00";
static const uint8_t hint2_iv[16] = "IV_TIL_HINT_NR_2";

void encrypt(uint8_t *pt, const uint8_t *iv_param, size_t length) {
    // Create the IV by XORing iv_param with iv_mask
    char iv[16];
    for (int i = 0; i < 16; i++) {
        iv[i] = iv_param[i] ^ iv_mask[i];
    }

    struct AES_ctx ctx;
    AES_init_ctx_iv(&ctx, (uint8_t*)key, (uint8_t*)iv);

    for (int i = 0; i < length; i++) {
        pt[i] ^= xor_mask2[15 - (i % length)];
    }

    // Prepare the plaintext
    AES_CBC_encrypt_buffer(&ctx, (uint8_t*)pt, length);

    for (int i = 0; i < length; i++) {
        pt[i] ^= xor_mask1[15 - (i % length)];
    }
}

int main() {
    encrypt(hint1, hint1_iv, 80);
    printf("Hint 1: ");
    for (int i = 0; i < 80; i++) {
        printf("\\x%02x", hint1[i]);
    }
    printf("\n\n");

    encrypt(hint2, hint2_iv, 80);
    printf("Hint 2: ");
    for (int i = 0; i < 80; i++) {
        printf("\\x%02x", hint2[i]);
    }
    printf("\n");

    return 0;
}
