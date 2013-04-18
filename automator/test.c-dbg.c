#include <stdio.h>
#include <stdio.h>

int *foo(float *b) {
  fprintf(stderr, "test.c:3:call(foo)\n");
  fprintf(stderr, "test.c:3:decl(float*,b)\n");
  fprintf(stderr, "test.c:3:assign(float*,b,%p)\n", b);
  int *____1 = (int) (*b);
  fprintf(stderr, "test.c:4:return(foo,int*,ret,%p)\n", ____1);
  return ____1;
  fprintf(stderr, "test.c:5:return(foo,int*,ret,undef)\n", );
}


void main(int x, char **y) {
  fprintf(stderr, "test.c:7:call(main)\n");
  fprintf(stderr, "test.c:7:decl(int,x)\n");
  fprintf(stderr, "test.c:7:assign(int,x,%d)\n", x);
  fprintf(stderr, "test.c:7:decl(char**,y)\n");
  fprintf(stderr, "test.c:7:assign(char**,y,%p)\n", y);
  int i;
  fprintf(stderr, "test.c:8:decl(int,i)\n");
  fprintf(stderr, "test.c:8:assign(int,i,%d)\n", i);
  fprintf(stderr, "test.c:9:scope_in\n");
  float ____0 = 0;
  fprintf(stderr, "test.c:9:decl(float,i)\n");
  fprintf(stderr, "test.c:9:assign(float,i,%f)\n", ____0);
  for (float i = ____0; i < 1; (i++) | (fprintf(stderr, "test.c:9:assign(float,i,%f)\n", i + 1) == 0))
  {
    i = 3;
    fprintf(stderr, "test.c:10:assign(float,i,%f)\n", i);
  }

  fprintf(stderr, "test.c:9:scope_out\n");
  i = 3;
  fprintf(stderr, "test.c:12:assign(int,i,%d)\n", i);
  fprintf(stderr, "test.c:13:return(main,void,ret,undef)\n", );
}
