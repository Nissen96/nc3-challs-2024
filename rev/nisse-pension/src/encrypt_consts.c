#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <unistd.h>
#include "aes.h"

static const uint8_t key[16] = "NISSEKEY_TIL_DIG";
static const uint8_t iv_mask[16] = "JULETID_ER_HYGGE";
static const uint8_t xor_mask1[16] = "EN_XOR_MASKE_HER";
static const uint8_t xor_mask2[16] = "EKSTRA_XOR_MASKE";

static uint8_t hint1[80] = "Du er i kontrol over programmet!\nMåske det kan debugges med GDB eller patches?\x00";
static const uint8_t hint1_iv[16] = "HINT1_TIL_FRITZ!";

static uint8_t hint2[128] = "Fritz overvejer, om han mon kan styre sin beholdning af ❄️\nEller måske endda hoppe direkte til et smart sted i programmet!\x00";
static const uint8_t hint2_iv[16] = "HER_ER_IV_HINT2!";

static uint8_t flag[64] = "NC3{30_År5_0psp4r1ng_s1kr3t_nu_k4n_Fr1tz_Gå_pÅ_p3ns10n 🎅}\x00";
static const uint8_t flag_iv[16] = "\xab\xfe\x34\x3f\x91\x01\x23\xff\xfe\xad\x2a\x10\x99\x89\x0a\x1c";

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

    encrypt(hint2, hint2_iv, 128);
    printf("Hint 2: ");
    for (int i = 0; i < 128; i++) {
        printf("\\x%02x", hint2[i]);
    }
    printf("\n\n");

    encrypt(flag, flag_iv, 64);
    printf("Flag: ");
    for (int i = 0; i < 64; i++) {
        printf("\\x%02x", flag[i]);
    }
    printf("\n");

    return 0;
}
