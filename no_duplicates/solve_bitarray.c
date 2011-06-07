#include <stdio.h>
#include <stdlib.h>

int main(int argc, char*argv[]) {

  char line[100];
  char *bit, *bitarray = (char *)malloc(12375000);
  FILE *fp = fopen(argv[1], "r");

  int i;

  while (fgets(line, 100, fp)) {
    i = atoi(line);
    if (!(bitarray[(i-1000000)>>3] & 1<<(i%8))) {
      printf("%d\n", i);
      bitarray[(i-1000000)>>3]|=(1<<(i%8));
    }
  }
  fclose(fp);
  return 0;
}
