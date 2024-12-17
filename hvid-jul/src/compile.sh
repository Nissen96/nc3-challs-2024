gcc -o interpret -fstack-protector-all -Wl,-z,relro,-z,now interpret.c
gcc -o interpret-debug -DDEBUG -fstack-protector-all -Wl,-z,relro,-z,now interpret.c
sleep infinity
