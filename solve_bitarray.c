#include <stdio.h>
#include <stdlib.h>

int main(int argc, char*argv[]) {

  char line[100];
  char *bit, *bitarray = (char *)malloc(12375000);
  FILE *fp;
  if (argc>1) fp = fopen(argv[1], "r");
  else exit(1);

  int i;

  while (fgets(line, 100, fp)) {
    i = atoi(line);
    bit = (int)bitarray[(i-1000000)>>3];
    if (!(bit & 1<<(i%8))) {
      printf("%d\n", i);
      bit|=1<<(i%8;
  }
  fclose(fp);
}
