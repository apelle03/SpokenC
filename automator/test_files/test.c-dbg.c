#include <stdio.h>
#include <stdio.h>

int foo(float *b) {
  fprintf(stderr, "test_files/test.c:3:call(foo)\n");
  fprintf(stderr, "test_files/test.c:3:decl(float*,b)\n");
  fprintf(stderr, "test_files/test.c:3:assign(float*,b,%p)\n", b);
  int ____1 = (int) (*b);
  fprintf(stderr, "test_files/test.c:4:return(foo,int,ret,%d)\n", ____1);
  return ____1;
  fprintf(stderr, "test_files/test.c:5:return(foo,int,ret,undef)\n");
}


void main(int x, char **y) {
  fprintf(stderr, "test_files/test.c:7:call(main)\n");
  fprintf(stderr, "test_files/test.c:7:decl(int,x)\n");
  fprintf(stderr, "test_files/test.c:7:assign(int,x,%d)\n", x);
  fprintf(stderr, "test_files/test.c:7:decl(char**,y)\n");
  fprintf(stderr, "test_files/test.c:7:assign(char**,y,%p)\n", y);
  float i;
  fprintf(stderr, "test_files/test.c:8:decl(float,i)\n");
  fprintf(stderr, "test_files/test.c:8:assign(float,i,%f)\n", i);
  fprintf(stderr, "test_files/test.c:9:scope_in\n");
  int ____0 = 0;
  fprintf(stderr, "test_files/test.c:9:decl(int,i)\n");
  fprintf(stderr, "test_files/test.c:9:assign(int,i,%d)\n", ____0);
  for (int i = ____0; i < 1; (i++) | (fprintf(stderr, "test_files/test.c:9:assign(int,i,%d)\n", i + 1) == 0))
  {
    i = 3;
    fprintf(stderr, "test_files/test.c:10:assign(int,i,%d)\n", i);
  }

  fprintf(stderr, "test_files/test.c:9:scope_out\n");
  i = 3;
  fprintf(stderr, "test_files/test.c:12:assign(float,i,%f)\n", i);
  fprintf(stderr, "test_files/test.c:13:return(main,void,ret,undef)\n");
}

