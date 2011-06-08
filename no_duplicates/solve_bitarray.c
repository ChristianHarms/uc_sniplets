#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(int argc, char*argv[]) {

  char line[100];
  const minValue = 1000000;
  const maxValue = 100000000;
  int32_t *bitarray = (int32_t *)malloc(sizeof(int32_t) * (maxValue - minValue) / 32);
  FILE *fp = fopen(argv[1], "r");

  int pos;

  while (fgets(line, 100, fp)) {
    pos = atoi(line);
    if (!(bitarray[(pos-minValue)>>5] & 1<<(pos%32))) {
      printf("%d\n", pos);
      bitarray[(pos-minValue)>>5]|=(1<<(pos%32));
    }
  }
  fclose(fp);
  return 0;
}
