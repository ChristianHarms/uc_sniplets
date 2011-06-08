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
  int i=0, last;
  FILE *fp = fopen(argv[1], "r");
  int count = (int)atoi(argv[2]);
  int32_t *digits = (int32_t *)malloc(count * sizeof(int32_t));

  // reading the lines, convert into an int, push into array
  while (fgets(line, 100, fp)) {
    digits[i++] = (int32_t)atoi(line);
  }
  fclose(fp);


  //sort the complete array
  qsort(digits, count, sizeof(int), compare);

  //Print all int, ignore doubles
  last = -1;
  for (i=0; i<count; i++) {
    if (last!=digits[i]) printf("%d\n", digits[i]);
    last = digits[i];
  }
  return 0;<
}
