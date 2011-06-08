#include <stdio.h>
#include <stdlib.h>

int main(int argc, char*argv[]) {

  char line[100];
  const minValue = 1000000;
  const maxValue = 100000000;
  char *bitarray = (char *)malloc((maxValue - minValue) / 8);
  FILE *fp = fopen(argv[1], "r");

  int pos;

  while (fgets(line, 100, fp)) {
    pos = atoi(line);
    if (!(bitarray[(pos-minValue)>>3] & 1<<(pos%8))) {
      printf("%d\n", pos);
      bitarray[(pos-minValue)>>3]|=(1<<(pos%8));
    }
  }
  fclose(fp);
  return 0;
}
