#include <stdio.h>

int main() {
  int i = 1;
  int ret = (++i) + (++i);
  printf("%d", ret);
  return 0;
}