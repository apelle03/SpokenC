#include <stdio.h>
#include <stdio.h>

int factorial(int i) {
  fprintf(stderr, "test_files/fact.c:3:call(factorial)\n");
  fprintf(stderr, "test_files/fact.c:3:decl(int,i)\n");
  fprintf(stderr, "test_files/fact.c:3:assign(int,i,%d)\n", i);
  if (i <= 1)
  {
    fprintf(stderr, "test_files/fact.c:4:scope_in\n");
    int ____0 = 1;
    fprintf(stderr, "test_files/fact.c:5:return(factorial,int,ret,%d)\n", ____0);
    return ____0;
    fprintf(stderr, "test_files/fact.c:4:scope_out\n");
  }
  else
  {
    fprintf(stderr, "test_files/fact.c:4:scope_in\n");
    int ____1 = i * factorial(i - 1);
    fprintf(stderr, "test_files/fact.c:7:return(factorial,int,ret,%d)\n", ____1);
    return ____1;
    fprintf(stderr, "test_files/fact.c:4:scope_out\n");
  }

  fprintf(stderr, "test_files/fact.c:9:return(factorial,int,ret,undef)\n");
}


int main(int argc, char **argv) {
  fprintf(stderr, "test_files/fact.c:11:call(main)\n");
  fprintf(stderr, "test_files/fact.c:11:decl(int,argc)\n");
  fprintf(stderr, "test_files/fact.c:11:assign(int,argc,%d)\n", argc);
  fprintf(stderr, "test_files/fact.c:11:decl(char**,argv)\n");
  fprintf(stderr, "test_files/fact.c:11:assign(char**,argv,%p)\n", argv);
  int x = 0;
  fprintf(stderr, "test_files/fact.c:12:decl(int,x)\n");
  fprintf(stderr, "test_files/fact.c:12:assign(int,x,%d)\n", x);
  const char *string = "The factorial of %d is: %d\n";
  fprintf(stderr, "test_files/fact.c:13:decl(char*,string)\n");
  fprintf(stderr, "test_files/fact.c:13:assign(char*,string,%s)\n", string);
  fprintf(stderr, "test_files/fact.c:14:scope_in\n");
  int ____2 = 1;
  fprintf(stderr, "test_files/fact.c:14:decl(int,i)\n");
  fprintf(stderr, "test_files/fact.c:14:assign(int,i,%d)\n", ____2);
  for (int i = ____2; i <= 2; (i++) | (fprintf(stderr, "test_files/fact.c:14:assign(int,i,%d)\n", i + 1) == 0))
  {
    x = factorial(i);
    fprintf(stderr, "test_files/fact.c:15:assign(int,x,%d)\n", x);
    printf(string, i, x);
  }

  fprintf(stderr, "test_files/fact.c:14:scope_out\n");
  x = 10;
  fprintf(stderr, "test_files/fact.c:18:assign(int,x,%d)\n", x);
  int ____3 = 0;
  fprintf(stderr, "test_files/fact.c:19:return(main,int,ret,%d)\n", ____3);
  return ____3;
  fprintf(stderr, "test_files/fact.c:20:return(main,int,ret,undef)\n");
}

