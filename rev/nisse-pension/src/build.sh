gcc encrypt_consts.c aes.c -Wall -DCBC=1 -DECB=0 -DCTR=0 -o encrypt_consts
gcc nisseby.c aes.c -Wall -DCBC=1 -DECB=0 -DCTR=0 -o nisseby
