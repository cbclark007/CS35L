#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int frobcmp(char const *a, char const *b);
int compare(const void *a, const void *b);

int main()
{
  char c;
  char* line = (char*)malloc(sizeof(char));
  char** lines = (char**)malloc(sizeof(char*));
  int numlines = 0;
  int lenline = 0;

  if(line == NULL || lines == NULL)
    {
      fprintf(stderr, "Malloc failed. Exiting.");
      exit(1);
    }
  
  while(!feof(stdin))
    {
      if(ferror(stdin))
	{
	  fprintf(stderr, "stdin error");
	  exit(1);
	}
      //get the char
      c = getchar();
      
      //c is a space character
      if(c == ' ' || c == EOF || feof(stdin))
	{
	  //append space char at end of the line
	  line = (char*)realloc(line, (lenline+2)*sizeof(char));
	  if(line == NULL)
	    {
	      fprintf(stderr, "realloc failed. exiting.");
	      exit(1);
	    }
	  
	  line[lenline] = ' ';
	  lenline++;

	  //create a new line n stuff
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

	  lenline = 0;
	} else
	{
	  //c is not a space; append it to line
	  line = (char*)realloc(line, (lenline+2)*(sizeof(char)));

	  if(line == NULL)
	    {
	      fprintf(stderr, "realloc failed. Exiting.");
	      exit(1);
	    }
	  
	  line[lenline] = c;
	  lenline++;
	}      
    }
  if(line != NULL) {
    free(line);
  }
  
  qsort(lines, numlines, sizeof(char*), compare);

  for(int i = 0; i < numlines; i++) {
    for(int j = 0; lines[i][j] != ' '; j++) {
      putchar(lines[i][j]);
    }
    putchar(' ');
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


