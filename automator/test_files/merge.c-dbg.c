#include <stdio.h>
/* merge.c -- Given two sorted sequences of integers, it creates
 *            a sorted sequence consisting of all their numbers.
 */

#include <stdio.h>

#define NMAX 100

void printIntArray(int a[], int n);
void merge(int c[], int *nc, int a[], int na, int b[], int nb);

int main(int argc, char **argv) {
  fprintf(stderr, "test_files/merge.c:12:call(main)\n");
  fprintf(stderr, "test_files/merge.c:12:decl(int,argc)\n");
  fprintf(stderr, "test_files/merge.c:12:assign(int,argc,%d)\n", argc);
  fprintf(stderr, "test_files/merge.c:12:decl(char**,argv)\n");
  fprintf(stderr, "test_files/merge.c:12:assign(char**,argv,%p)\n", argv);
  int x[100] = {1, 3, 5, 6, 7, 8, 10, 11, 15, 20, 21, 21, 22, 24, 26, 28, 29, 32, 34, 35};
  fprintf(stderr, "test_files/merge.c:13:decl(int*,x)\n");
  fprintf(stderr, "test_files/merge.c:13:assign(int*,x,%p)\n", x);
  int y[100] = {2, 3, 4, 6, 6, 9, 10, 12, 16, 21, 23, 23, 26, 27, 29, 33, 35, 39, 40, 41};
  fprintf(stderr, "test_files/merge.c:14:decl(int*,y)\n");
  fprintf(stderr, "test_files/merge.c:14:assign(int*,y,%p)\n", y);
  int z[100 + 100];
  fprintf(stderr, "test_files/merge.c:15:decl(int*,z)\n");
  fprintf(stderr, "test_files/merge.c:15:assign(int*,z,%p)\n", z);
  int nz;
  fprintf(stderr, "test_files/merge.c:16:decl(int,nz)\n");
  fprintf(stderr, "test_files/merge.c:16:assign(int,nz,%d)\n", nz);
  merge(z, &nz, x, 20, y, 20);
  printIntArray(z, nz);
  fprintf(stderr, "test_files/merge.c:20:return(main,int,ret,undef)\n");
}


void printIntArray(int a[], int n)
     /* n is the number of elements in the array a.
      * These values are printed out, five per line. */
{
  fprintf(stderr, "test_files/merge.c:22:call(printIntArray)\n");
  fprintf(stderr, "test_files/merge.c:22:decl(int*,a)\n");
  fprintf(stderr, "test_files/merge.c:22:assign(int*,a,%p)\n", a);
  fprintf(stderr, "test_files/merge.c:22:decl(int,n)\n");
  fprintf(stderr, "test_files/merge.c:22:assign(int,n,%d)\n", n);
  int i;
  fprintf(stderr, "test_files/merge.c:26:decl(int,i)\n");
  fprintf(stderr, "test_files/merge.c:26:assign(int,i,%d)\n", i);
  fprintf(stderr, "test_files/merge.c:28:scope_in\n");
  for ((i = 0) | (fprintf(stderr, "test_files/merge.c:28:assign(int,i,%d)\n", i) == 0); i < n; (i++) | (fprintf(stderr, "test_files/merge.c:28:assign(int,i,%d)\n", i + 1) == 0))
  {
    printf("\t%d ", a[i]);
    if ((i % 5) == 4)
      printf("\n");

  }

  fprintf(stderr, "test_files/merge.c:28:scope_out\n");
  printf("\n");
  fprintf(stderr, "test_files/merge.c:34:return(printIntArray,void,ret,undef)\n");
}


void merge(int c[], int *nc, int a[], int na, int b[], int nb){
  fprintf(stderr, "test_files/merge.c:36:call(merge)\n");
  fprintf(stderr, "test_files/merge.c:36:decl(int*,c)\n");
  fprintf(stderr, "test_files/merge.c:36:assign(int*,c,%p)\n", c);
  fprintf(stderr, "test_files/merge.c:36:decl(int*,nc)\n");
  fprintf(stderr, "test_files/merge.c:36:assign(int*,nc,%p)\n", nc);
  fprintf(stderr, "test_files/merge.c:36:decl(int*,a)\n");
  fprintf(stderr, "test_files/merge.c:36:assign(int*,a,%p)\n", a);
  fprintf(stderr, "test_files/merge.c:36:decl(int,na)\n");
  fprintf(stderr, "test_files/merge.c:36:assign(int,na,%d)\n", na);
  fprintf(stderr, "test_files/merge.c:36:decl(int*,b)\n");
  fprintf(stderr, "test_files/merge.c:36:assign(int*,b,%p)\n", b);
  fprintf(stderr, "test_files/merge.c:36:decl(int,nb)\n");
  fprintf(stderr, "test_files/merge.c:36:assign(int,nb,%d)\n", nb);
  int cursora = 0;
  fprintf(stderr, "test_files/merge.c:41:decl(int,cursora)\n");
  fprintf(stderr, "test_files/merge.c:41:assign(int,cursora,%d)\n", cursora);
  int cursorb = 0;
  fprintf(stderr, "test_files/merge.c:41:decl(int,cursorb)\n");
  fprintf(stderr, "test_files/merge.c:41:assign(int,cursorb,%d)\n", cursorb);
  int cursorc = 0;
  fprintf(stderr, "test_files/merge.c:41:decl(int,cursorc)\n");
  fprintf(stderr, "test_files/merge.c:41:assign(int,cursorc,%d)\n", cursorc);
  fprintf(stderr, "test_files/merge.c:43:scope_in\n");
  while ((cursora < na) && (cursorb < nb))
    if (a[cursora] <= b[cursorb])
  {
    fprintf(stderr, "test_files/merge.c:44:scope_in\n");
    c[cursorc] = a[cursora];
    cursorc++;
    fprintf(stderr, "test_files/merge.c:46:assign(int,cursorc,%d)\n", cursorc);
    cursora++;
    fprintf(stderr, "test_files/merge.c:47:assign(int,cursora,%d)\n", cursora);
    fprintf(stderr, "test_files/merge.c:44:scope_out\n");
  }
  else
  {
    fprintf(stderr, "test_files/merge.c:44:scope_in\n");
    c[cursorc] = b[cursorb];
    cursorc++;
    fprintf(stderr, "test_files/merge.c:51:assign(int,cursorc,%d)\n", cursorc);
    cursorb++;
    fprintf(stderr, "test_files/merge.c:52:assign(int,cursorb,%d)\n", cursorb);
    fprintf(stderr, "test_files/merge.c:44:scope_out\n");
  }


  fprintf(stderr, "test_files/merge.c:43:scope_out\n");
  fprintf(stderr, "test_files/merge.c:55:scope_in\n");
  while (cursora < na)
  {
    c[cursorc] = a[cursora];
    cursorc++;
    fprintf(stderr, "test_files/merge.c:57:assign(int,cursorc,%d)\n", cursorc);
    cursora++;
    fprintf(stderr, "test_files/merge.c:58:assign(int,cursora,%d)\n", cursora);
  }

  fprintf(stderr, "test_files/merge.c:55:scope_out\n");
  fprintf(stderr, "test_files/merge.c:61:scope_in\n");
  while (cursorb < nb)
  {
    c[cursorc] = b[cursorb];
    cursorc++;
    fprintf(stderr, "test_files/merge.c:63:assign(int,cursorc,%d)\n", cursorc);
    cursorb++;
    fprintf(stderr, "test_files/merge.c:64:assign(int,cursorb,%d)\n", cursorb);
  }

  fprintf(stderr, "test_files/merge.c:61:scope_out\n");
  *nc = cursorc;
  fprintf(stderr, "test_files/merge.c:68:return(merge,void,ret,undef)\n");
}

