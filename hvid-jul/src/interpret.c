#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define STACK_SIZE 1024
#define HEAP_SIZE 1024

int sp = 0;

void push(int* stack, int n);
int pop(int* stack);
void interpret(const char *code);

void init() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

int main(int argc, char** argv) {
    init();

    int max_size = 128 * 128;

    // Allocate a large buffer for input
    char *whitespace_code = malloc(max_size);
    if (!whitespace_code) {
        fprintf(stderr, "Hukommelsesallokering fejlede :(\n");
        return 1;
    }

    printf("Indtast dit Whitespace program, afslut med .\n");

    // Read until EOF
    size_t index = 0;
    char c;

    while ((c = getchar()) != EOF) {
        if (index == max_size) break;
        if (c == '.') break;  // Stop reading on .

        // Ignore non-whitespace
        if (c == ' ' || c == '\t' || c == '\n') {
            whitespace_code[index++] = c;
        }
    }

    interpret(whitespace_code);

    free(whitespace_code);
    return 0;
}

// Error handling
void error(const char *msg) {
    fprintf(stderr, "Hov hov, det må man ikke: %s\n", msg);
    exit(EXIT_FAILURE);
}

// Push a value onto the stack
void push(int* stack, int n) {
    if (sp >= 1042) error("Stack overflow");
    stack[sp++] = n;
}

// Pop a value from the stack
int pop(int* stack) {
    if (sp <= 0) error("Stack underflow");
    return stack[--sp];
}

// Interpret Whitespace code
void interpret(const char *code) {
    int heap[HEAP_SIZE];
    int stack[STACK_SIZE];

    const char *pc = code; // Program counter

    while (*pc) {
        if (*pc == ' ') {
            // Stack manipulation
            pc++;
            if (*pc == ' ') {
                // Push number
                pc++;
                int negate = (*pc == '\t' ? 1 : 0);
                pc++;
                int num = 0;
                while (*pc != '\n') {
                    num = num * 2 + (*pc == '\t' ? 1 : 0);
                    pc++;
                }
                if (negate) {
                    num = -num;
                }
                #ifdef DEBUG
                	printf("Pushing %d to STACK[%d]\n", num, sp);
                #endif
                push(stack, num);
            } else if (*pc == '\n') {
                pc++;
                if (*pc == ' ') { // Duplicate
                    #ifdef DEBUG
                    	puts("Duplicating TOS");
                    #endif
                    push(stack, stack[sp - 1]);
                } else if (*pc == '\t') { // Swap
                    #ifdef DEBUG
                    	puts("Swapping TOS");
                    #endif
                    int a = pop(stack);
                    int b = pop(stack);
                    push(stack, a);
                    push(stack, b);
                } else if (*pc == '\n') { // Pop top
                    #ifdef DEBUG
                    	puts("POP TOS");
                    #endif
                    pop(stack);
                }
            }
        } else if (*pc == '\t') {
            pc++;
            if (*pc == ' ') {
                // Arithmetic
                pc++;
                int a = pop(stack);
                int b = pop(stack);
                if (*pc == ' ') {
                    pc++;
                    if (*pc == ' ') {
                        #ifdef DEBUG
                        	printf("Pushing %d + %d = %d\n", b, a, a + b);
                        #endif
                        push(stack, b + a);      // Add
                    } else if (*pc == '\t') {
                        #ifdef DEBUG
                        	printf("Pushing %d - %d = %d\n", b, a, b - a);
                        #endif
                        push(stack, b - a); // Subtract
                    } else if (*pc == '\n') {
                        #ifdef DEBUG
                        	printf("Pushing %d * %d = %d\n", a, b, a * b);
                        #endif
                        push(stack, b * a); // Multiply
                    }
                } else if (*pc == '\t') {
                    pc++;
                    if (*pc == ' ') {
                        #ifdef DEBUG
                        	printf("Pushing %d / %d = %d\n", b, a, b / a);
                        #endif
                        push(stack, b / a);      // Integer division
                    } else if (*pc == '\t') {
                        #ifdef DEBUG
                        	printf("Pushing %d %% %d = %d\n", b, a, b % a);
                        #endif
                        push(stack, b % a); // Modulo
                    } else if (*pc == '\n') {
                        #ifdef DEBUG
                        	printf("Pushing %d ^ %d = %d\n", b, a, b ^ a);
                        #endif
                        push(stack, b ^ a); // XOR
                    }
                }
            } else if (*pc == '\t') {
                // Heap access
                pc++;
                if (*pc == ' ') {
                    int val = pop(stack);
                    int addr = pop(stack);
                    if (addr >= 1024) error("Heap overflow");
                    #ifdef DEBUG
                    	printf("Storing popped value %d in HEAP[%d]\n", val, addr);
                    #endif
                    heap[addr] = val; // Store
                } else if (*pc == '\t') {
                    int addr = pop(stack);
                    #ifdef DEBUG
                    	printf("Retrieving value from HEAP[%d]\n", addr);
                    #endif
                    push(stack, heap[addr]); // Retrieve
                }
            } else if (*pc == '\n') {
                // I/O
                pc++;
                if (*pc == ' ') {
                    pc++;
                    if (*pc == ' ') {
                        #ifdef DEBUG
                        	puts("Printing ASCII value");
                        #endif
                        printf("%c", pop(stack));
                    } else if (*pc == '\t') {
                        #ifdef DEBUG
                        	puts("Printing number");
                        #endif
                        printf("%d", pop(stack));
                    }
                } else if (*pc == '\t') {
                    pc++;
                    if (*pc == ' ') {
                        int addr = pop(stack);
                        if (addr >= 1024) error("Heap overflow");
                        char val = getchar();
                        #ifdef DEBUG
                        	printf("Store char %c at popped heap address HEAP[%d]\n", val, addr);
                        #endif
                        heap[addr] = val;
                    } else if (*pc == '\t') {
                        int addr = pop(stack);
                        if (addr >= 1024) error("Heap overflow");
                        #ifdef DEBUG
                        	printf("Store input number at popped heap address HEAP[%d]\n", addr);
                        #endif
                        scanf("%d", &heap[addr]);
                    }
                }
            }
        } else if (*pc == '\n') {
            pc++;
            if (*pc == '\n') {
                pc++;
                if (*pc == '\n') {
                    #ifdef DEBUG
                    	puts("Bye bye");
                    #endif
                    break; // End of program
                }
            } else {
                puts("Meh, hvem har også brug for flow control");
                pc++;
            }
        }
        pc++;
    }
}
