#include <stdio.h>
/* string2.c  -- Compacting sequences of spaces in a string.
                 We use two different methods
 */

#include <stdio.h>
#include <string.h>
#define MAXBUFF 65536

int getline(char line[], int nmax);
int compact1(char line[]);
int compact2(char line[]);

int main(int argc, char **argv) {
  fprintf(stderr, "test_files/compact.c:13:call(main)\n");
  fprintf(stderr, "test_files/compact.c:13:decl(int,argc)\n");
  fprintf(stderr, "test_files/compact.c:13:assign(int,argc,%d)\n", argc);
  fprintf(stderr, "test_files/compact.c:13:decl(char**,argv)\n");
  fprintf(stderr, "test_files/compact.c:13:assign(char**,argv,%p)\n", argv);
  char buffer1[65536];
  fprintf(stderr, "test_files/compact.c:14:decl(char*,buffer1)\n");
  fprintf(stderr, "test_files/compact.c:14:assign(char*,buffer1,%s)\n", buffer1);
  char buffer2[65536];
  fprintf(stderr, "test_files/compact.c:15:decl(char*,buffer2)\n");
  fprintf(stderr, "test_files/compact.c:15:assign(char*,buffer2,%s)\n", buffer2);
  int len;
  fprintf(stderr, "test_files/compact.c:16:decl(int,len)\n");
  fprintf(stderr, "test_files/compact.c:16:assign(int,len,%d)\n", len);
  len = getline(buffer1, 65536);
  fprintf(stderr, "test_files/compact.c:18:assign(int,len,%d)\n", len);
  printf("You entered : %s\n", buffer1);
  strcpy(buffer2, buffer1);
  printf("Which is : %s\n", buffer2);
  len = compact1(buffer1);
  fprintf(stderr, "test_files/compact.c:23:assign(int,len,%d)\n", len);
  printf("compact1: len=%d,  %s\n", len, buffer1);
  len = compact2(buffer2);
  fprintf(stderr, "test_files/compact.c:25:assign(int,len,%d)\n", len);
  printf("compact2: len=%d,  %s\n", len, buffer2);
  fprintf(stderr, "test_files/compact.c:27:return(main,int,ret,undef)\n");
}


int getline(char line[], int nmax)
     /* It prompts user and reads up to nmax
      * characters into line. It returns number
      * of characters read. ['\n' terminates the line]
      */
{
  fprintf(stderr, "test_files/compact.c:29:call(getline)\n");
  fprintf(stderr, "test_files/compact.c:29:decl(char*,line)\n");
  fprintf(stderr, "test_files/compact.c:29:assign(char*,line,%s)\n", line);
  fprintf(stderr, "test_files/compact.c:29:decl(int,nmax)\n");
  fprintf(stderr, "test_files/compact.c:29:assign(int,nmax,%d)\n", nmax);
  int len;
  fprintf(stderr, "test_files/compact.c:35:decl(int,len)\n");
  fprintf(stderr, "test_files/compact.c:35:assign(int,len,%d)\n", len);
  char c;
  fprintf(stderr, "test_files/compact.c:36:decl(char,c)\n");
  fprintf(stderr, "test_files/compact.c:36:assign(char,c,%c)\n", c);
  len = 0;
  fprintf(stderr, "test_files/compact.c:38:assign(int,len,%d)\n", len);
  printf("Enter a string [CR to exit]: ");
  fprintf(stderr, "test_files/compact.c:40:scope_in\n");
  while ((((c = getchar()) | (fprintf(stderr, "test_files/compact.c:40:assign(char,c,%c)\n", c) == 0)) != '\n') && (len < (nmax - 1)))
  {
    line[len] = c;
    len++;
    fprintf(stderr, "test_files/compact.c:42:assign(int,len,%d)\n", len);
  }

  fprintf(stderr, "test_files/compact.c:40:scope_out\n");
  line[len] = '\0';
  int ____2 = len;
  fprintf(stderr, "test_files/compact.c:45:return(getline,int,ret,%d)\n", ____2);
  return ____2;
  fprintf(stderr, "test_files/compact.c:46:return(getline,int,ret,undef)\n");
}


int compact1(char line[])
     /* It replaces streaks of spaces in line by a
      * single space. It returns lenght of resulting string.
      */
{
  fprintf(stderr, "test_files/compact.c:48:call(compact1)\n");
  fprintf(stderr, "test_files/compact.c:48:decl(char*,line)\n");
  fprintf(stderr, "test_files/compact.c:48:assign(char*,line,%s)\n", line);
  int cursor = 0;
  fprintf(stderr, "test_files/compact.c:53:decl(int,cursor)\n");
  fprintf(stderr, "test_files/compact.c:53:assign(int,cursor,%d)\n", cursor);
  int prevspace = 0;
  fprintf(stderr, "test_files/compact.c:54:decl(int,prevspace)\n");
  fprintf(stderr, "test_files/compact.c:54:assign(int,prevspace,%d)\n", prevspace);
  int lcv = 0;
  fprintf(stderr, "test_files/compact.c:55:decl(int,lcv)\n");
  fprintf(stderr, "test_files/compact.c:55:assign(int,lcv,%d)\n", lcv);
  if (line[cursor] == '\0')
  {
    fprintf(stderr, "test_files/compact.c:57:scope_in\n");
    int ____0 = 0;
    fprintf(stderr, "test_files/compact.c:58:return(compact1,int,ret,%d)\n", ____0);
    return ____0;
    fprintf(stderr, "test_files/compact.c:57:scope_out\n");
  }

  fprintf(stderr, "test_files/compact.c:60:scope_in\n");
  do
  {
    if ((line[cursor] == ' ') && prevspace)
    {
      fprintf(stderr, "test_files/compact.c:61:scope_in\n");
      fprintf(stderr, "test_files/compact.c:64:scope_in\n");
      for ((lcv = cursor) | (fprintf(stderr, "test_files/compact.c:64:assign(int,lcv,%d)\n", lcv) == 0); line[lcv]; (lcv++) | (fprintf(stderr, "test_files/compact.c:64:assign(int,lcv,%d)\n", lcv + 1) == 0))
        line[lcv] = line[lcv + 1];

      fprintf(stderr, "test_files/compact.c:64:scope_out\n");
      fprintf(stderr, "test_files/compact.c:61:scope_out\n");
    }
    else
      prevspace = line[cursor++] == ' ';

  }
  while (line[cursor]);
  fprintf(stderr, "test_files/compact.c:60:scope_out\n");
  int ____1 = cursor;
  fprintf(stderr, "test_files/compact.c:69:return(compact1,int,ret,%d)\n", ____1);
  return ____1;
  fprintf(stderr, "test_files/compact.c:70:return(compact1,int,ret,undef)\n");
}


int compact2(char line[])
     /* It replaces streaks of spaces in line by a
      * single space. It returns lenght of resulting string.
      */
{
  fprintf(stderr, "test_files/compact.c:72:call(compact2)\n");
  fprintf(stderr, "test_files/compact.c:72:decl(char*,line)\n");
  fprintf(stderr, "test_files/compact.c:72:assign(char*,line,%s)\n", line);
  int cursor = 0;
  fprintf(stderr, "test_files/compact.c:77:decl(int,cursor)\n");
  fprintf(stderr, "test_files/compact.c:77:assign(int,cursor,%d)\n", cursor);
  int prevspace = 0;
  fprintf(stderr, "test_files/compact.c:78:decl(int,prevspace)\n");
  fprintf(stderr, "test_files/compact.c:78:assign(int,prevspace,%d)\n", prevspace);
  int lcv = 0;
  fprintf(stderr, "test_files/compact.c:79:decl(int,lcv)\n");
  fprintf(stderr, "test_files/compact.c:79:assign(int,lcv,%d)\n", lcv);
  fprintf(stderr, "test_files/compact.c:81:scope_in\n");
  do
  {
    if (!((line[cursor] == ' ') && prevspace))
    {
      fprintf(stderr, "test_files/compact.c:82:scope_in\n");
      line[lcv++] = line[cursor];
      prevspace = line[cursor] == ' ';
      fprintf(stderr, "test_files/compact.c:84:assign(int,prevspace,%d)\n", prevspace);
      fprintf(stderr, "test_files/compact.c:82:scope_out\n");
    }

  }
  while (line[cursor++]);
  fprintf(stderr, "test_files/compact.c:81:scope_out\n");
  int ____3 = lcv - 1;
  fprintf(stderr, "test_files/compact.c:87:return(compact2,int,ret,%d)\n", ____3);
  return ____3;
  fprintf(stderr, "test_files/compact.c:88:return(compact2,int,ret,undef)\n");
}
