#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/stat.h>
#include <ctype.h>

int f = 0;

int frobcmp(char const *a, char const *b);
int compare(const void *a, const void *b);

int main(int argc, char** argv)
{
  //printf("HELLO: %s\n", argv[1]);
  if(argc == 2 && strcmp(argv[1], "-f") == 0) {
    //    printf("-f\n");
    f = 1;
  } else if (argc >= 2) {
    fprintf(stderr, "bad argument(s) or too many arguments");
    exit(1);
  }
  //  printf("F IS: %d\n", f);

  struct stat buffer;
  int status = fstat(0, &buffer);
  int numlines = 0;
  size_t bytes = buffer.st_size;
  //  printf("bytes: %d\n", buffer.st_size);
  
  char* line = (char*)malloc(sizeof(char));
  char** lines = (char**)malloc((numlines+2)*sizeof(char*));
  int lenline = 0;

  size_t initbytes = bytes;
  if(bytes == 0) initbytes = 1;
  char buf[initbytes];
  
  if(line == NULL || lines == NULL)
    {
      fprintf(stderr, "Malloc failed. Exiting.");
      exit(1);
    }
  read(0, buf, bytes);
  for(size_t i = 0; i < bytes; i++) {
    // printf("%d\n", i);
    //    printf("i: %d\n", i);
    //printf("inside the file one\n");
    char c = buf[i];
    
    line = (char*)realloc(line, (lenline+2)*sizeof(char));
    if(line == NULL)
      {
	fprintf(stderr, "realloc failed. exiting.");
	exit(1);
      }
	
    //space
    if(c == ' ') {
      line[lenline] = ' ';
      
      lines[numlines] = line;
      numlines++;

      lines = (char**)realloc(lines, (numlines+2)*sizeof(char*));
      if(lines == NULL)
	{
	  fprintf(stderr, "realloc failed. Exiting.");
	  exit(1);
	}
      lenline = 0;

      line = (char*)malloc(sizeof(char));
      if(line == NULL)
	{
	  fprintf(stderr, "malloc failed. Exiting.");
	  exit(1);
	}
      continue;
    }

    //any other character we add
    line[lenline] = c;
    //printf("adding char: %c\n", buf[0]);
    lenline++;
	//printf("line so far:\n");
	//for(int i = 0; i < lenline; i++) {
	//  putchar(line[i]);
	//	}
    //printf("\n");
    
  }
  //printf("\n");
  char buf2[1];
  //rest of the stuff if the file changes, I guess
  while(read(0, buf2, 1) > 0)
    {
      //printf("???\n");
      //printf("inside the other one\n");
      line = (char*)realloc(line, (lenline+2)*sizeof(char));
      if(line == NULL)
	{
	  fprintf(stderr, "malloc failed. Exiting.");
	  exit(1);
	}

      //space 
      if(buf2[0] == ' ')
	{
	  //  printf("is space char\n");
	  line[lenline] = ' ';
	  lenline = 0;
	  lines = (char**)realloc(lines, (numlines+2)*sizeof(char*));
	  if(lines == NULL)
	    {
	      fprintf(stderr, "realloc failed. Exiting.");
	      exit(1);
	    }
	  lines[numlines] = line;
	  numlines++;
	  line = (char*)malloc(sizeof(char));
	  if(line == NULL)
	    {
	      fprintf(stderr, "malloc failed. Exiting.");
	      exit(1);
	    }
	  continue;
	}
      //      printf("adding char:%c\n", buf[0]);
      //any other character
      line[lenline] = buf2[0];
      lenline++;
      //printf("line so far:\n");
      //for(int i = 0; i < lenline; i++) {
      //  putchar(line[i]);
      //}
      //printf("\n");
    }
  //  printf("lenline: %d\n", lenline);
  if(lenline != 0) {
    //printf("??? wut\n");
    line[lenline] = ' ';
    lenline = 0;
    lines = (char**)realloc(lines, (numlines+2)*sizeof(char*));
    if(lines == NULL)
      {
	fprintf(stderr, "realloc failed. Exiting.");
	exit(1);
      }
    lines[numlines] = line;
    numlines++;
    line = (char*)malloc(sizeof(char));
    if(line == NULL)
      {
	fprintf(stderr, "malloc failed. Exiting.");
	exit(1);
      }
  }
  //  printf("here now\n");

  if(line != NULL) {
    free(line);
  }
  //  printf("putchar:\n");
  //  for(size_t i = 0; i < numlines; i++) {
  //    for(int j = 0; lines[i][j] != ' '; j++) {
  //      putchar(lines[i][j]);
  //    }
  //    putchar(' ');
  //  }
  
  qsort(lines, numlines, sizeof(char*), compare);
  //  printf("what im supposed to do\n");
  for(size_t i = 0; i < numlines; i++) {
    //printf("is this stuff actually getting here\n");
    for(int j = 0; lines[i][j] != ' '; j++) {
      //printf("writing %c\n", lines[i][j]);
      write(1, &lines[i][j], 1);
    }
    char buf[1] = {' '};
    write(1, buf, 1);
  }
  
  for(int i = 0; i < numlines; i++) {
    if(lines[i] != NULL) free(lines[i]);
  }
  if(lines != NULL) free(lines);
  return 0;
}


int frobcmp(char const *a, char const *b)
{
  while((*a) != ' ' && (*b) != ' ')
  {
    char c1 = (*a)^42;
    char c2 = (*b)^42;
    //ignore case with toupper
    if(f == 1) {
      if(isalpha(c1)) c1 = toupper(c1);
      if(isalpha(c2)) c2 = toupper(c2);
    }
    if(c1 < c2) return -1;
    else if (c1 > c2) return 1;
    else {
      a++;
      b++;
    }
  }
  if((*a) == ' ' && (*b) != ' ') return -1;
  else if ((*a) != ' ' && (*b) == ' ') return 1;
  
  return 0;
}

int compare(const void *a, const void *b)
{
  return frobcmp(*(char**)a, *(char**)b);
}


