#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int getIndex(char c, char* from)
{
  for(int i = 0; i < strlen(from); i++) {
    if(from[i] == c) return i;
  }
  return -1;
}

int main(int argc, char** argv) {
  if(argc != 3) {
    fprintf(stderr, "must have 2 args");
    exit(1);
  }
  char* from = argv[1];
  char* to = argv[2];

  if(strlen(from) != strlen(to)) {
    fprintf(stderr, "lengths of input must be the same");
    exit(1);
  }

  for(int i = 0; i < strlen(from); i++) {
    for(int j = i+1; j < strlen(from); j++) {
      if(from[i] == from[j]) {
	fprintf(stderr, "identical bytes in the from input");
	exit(1);
      }
    }
  }

  char c;
  
  while(!feof(stdin))
    {
      if(ferror(stdin))
	{
	  fprintf(stderr, "stdin error");
	  exit(1);
	}
      //get the char
      c = getchar();
      if(c == EOF) break;
      
      int index = getIndex(c, from);

      if(index != -1) {
	putchar(to[index]);
      }
      else {
	putchar(c);
      }

    }
  return 0;

}
