#include <stdio.h>
#include <stdlib.h>

int compare(const void *pa, const void *pb) {
  const int *a = (const int *)pa;
  const int *b = (const int *)pb;
  return (*a > *b) - (*a < *b);
}

int main(int argc, char*argv[]) {

  char line[100];
  int32 *digits;
  FILE *fp;
  int i=0, count, last;

  if (argc<3) {
    printf("%s <inputfile> <lines>", argv[0]);
    exit(-1);
  }
  count = (int)atoi(argv[2]);
  fp = fopen(argv[1], "r");
  digits = (int *)malloc(count * sizeof(int));

  while (fgets(line, 100, fp)) {
    digits[i++] = (int32)atoi(line);
  }
  fclose(fp);

  qsort(digits, count, sizeof(int), compare);

  last = -1;
  for (i=0; i<count; i++) {
    if (last!=digits[i]) printf("%d\n", digits[i]);
    last = digits[i];
  }
}
