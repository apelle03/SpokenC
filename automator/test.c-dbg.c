#include <stdio.h>
#include <stdio.h>

void main(int x, char **y) {
  fprintf(stderr, "test.c:4:scope_in\n");
  int ____0 = 0;
  fprintf(stderr, "test.c:4:decl(int,i)\n");
  fprintf(stderr, "test.c:4:assign(int,i,%d)\n", ____0);
  for (int i = ____0; i < 10; (i++) | (fprintf(stderr, "test.c:4:assign(int,i,%d)\n", i + 1) == 0))
  {
    switch (i)
    {
      case 1:
        if (1)
      {
        fprintf(stderr, "test.c:7:scope_in\n");
        int d = 1;
        fprintf(stderr, "test.c:8:decl(int,d)\n");
        fprintf(stderr, "test.c:8:assign(int,d,%d)\n", d);
        int e = 10;
        fprintf(stderr, "test.c:8:decl(int,e)\n");
        fprintf(stderr, "test.c:8:assign(int,e,%d)\n", e);
        int f;
        fprintf(stderr, "test.c:8:decl(int,f)\n");
        fprintf(stderr, "test.c:8:assign(int,f,%d)\n", f);
        d++;
        fprintf(stderr, "test.c:9:assign(int,d,%d)\n", d);
        fprintf(stderr, "test.c:7:scope_out\n");
      }

        break;

    }

    if (1)
    {
      fprintf(stderr, "test.c:13:scope_in\n");
      int d = 1;
      fprintf(stderr, "test.c:14:decl(int,d)\n");
      fprintf(stderr, "test.c:14:assign(int,d,%d)\n", d);
      int e = 10;
      fprintf(stderr, "test.c:14:decl(int,e)\n");
      fprintf(stderr, "test.c:14:assign(int,e,%d)\n", e);
      int f;
      fprintf(stderr, "test.c:14:decl(int,f)\n");
      fprintf(stderr, "test.c:14:assign(int,f,%d)\n", f);
      d += e;
      fprintf(stderr, "test.c:15:assign(int,d,%d)\n", d);
      fprintf(stderr, "test.c:13:scope_out\n");
    }

  }

  fprintf(stderr, "test.c:4:scope_out\n");
}
