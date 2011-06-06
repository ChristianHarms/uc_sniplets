#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int compare(const void *pa, const void *pb) {
  const int *a = (const int *)pa;
  const int *b = (const int *)pb;
  return (*a > *b) - (*a < *b);
}

int main(int argc, char*argv[]) {

  char line[100];
  int32_t *digits;
  FILE *fp;
  int i=0, count, last;

  if (argc<2) {
    printf("%s <lines> - got %d", argv[0], argc);
    exit(-1);
  }
  count = (int)atoi(argv[1]);
  fp = stdin;
  digits = (int *)malloc(count * sizeof(int));

  while (fgets(line, 100, fp)) {
    digits[i++] = (int32_t)atoi(line);
  }
  fclose(fp);

  qsort(digits, count, sizeof(int), compare);

  last = -1;
  for (i=0; i<count; i++) {
    if (last!=digits[i]) printf("%d\n", digits[i]);
    last = digits[i];
  }

  return 0;
}
