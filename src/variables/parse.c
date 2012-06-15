/*
	<parse.c>
	17jul90 jm  Original code.
	27jul90 jm  Parse and arg corrected.
	02nov91 jm  Removed wipnumarg() in favor of new routine wipevaluate().
	20feb92 jm  Changed wiplenc to change trailing WHITE to Null's.
	28jul92 jm  Added wipnewstring() routine.
	11sep92 jm  Added test for empty (NULL) strings.
	09oct00 pjt no more PROTOTYPE #ifdef

Routines:
char *wipparse(char **line);
 int  wipcountwords(const char *line);
void  wiplower(char *s);
void  wipupper(char *s);
char *wipleading(const char *line);
 int  wiplenc(char *c);
char *wipnewstring(const char *string);
*/

#include "wip.h"

/* Global variables for just this file */

/* Code */

char *wipparse(char **line)
{
    char *s, *par;

    s = *line;
    if ((s == (char *)NULL) || (*s == Null))           /* Empty string. */
      return((char *)NULL);

    while ((*s != Null) && (WHITE(*s))) s++;    /* Skip leading blanks. */
    if (*s == Null) return((char *)NULL);     /* Nothing left to parse. */
    if (*s == '#') return((char *)NULL);             /* A Comment line. */

    par = s;                                           /* Found a word. */
    while ((*s != Null) && (!WHITE(*s)))    /* Extend over entire word. */
      s++;
    if (*s != Null) *s++ = Null;     /* Don't increment if at EOString. */
    *line = s;                                  /* Reset input pointer. */
    return(par);                                  /* Return found word. */
}

int wipcountwords(const char *line)
{
    register int n = 0;
    char *s;
    char save[BUFSIZ];

    s = Strcpy(save, line);   /* Make a temporary copy of input string. */
    while (wipparse(&s) != (char *)NULL) n++;       /* Count the words. */
    return(n);
}

void wiplower(char *s)
{
    register char j;

    while ((j = *s) != Null)
      *s++ = (isupper((int)j) ? (char)tolower((int)j) : j);
}

void wipupper(char *s)
{
    register char j;

    while ((j = *s) != Null)
      *s++ = (islower((int)j) ? (char)toupper((int)j) : j);
}

char *wipleading(const char *line)
{
    register char *s;

    s = (char *)line;
    if ((s == (char *)NULL) || (*s == Null))           /* Empty string. */
      return((char *)NULL);

    while ((*s != Null) && (WHITE(*s))) s++;    /* Skip leading blanks. */
    if (*s == Null) return((char *)NULL);      /* Nothing left to skip. */
    if (*s == '#') return((char *)NULL);             /* A Comment line. */

    return((char *)s);
}

int wiplenc(char *c)
{
    register char *s;

    if ((c == (char *)NULL) || (*c == Null))           /* Empty string. */
      return(0);

    s = (char *)(c) + Strlen(c) - 1;          /* Start at the EOString. */
    while ((s >= c) && (WHITE(*s))) *s-- = Null;       /* Remove WHITE. */

    return((int)(s - c + 1));  /* Return # of chars w/o trailing WHITE. */
}

/*
 *  Copies an instance of a string.  You must release this memory with Free()!
 *  Returns a NULL pointer if the input string is empty or on an error.
 */
char *wipnewstring(const char *string)
{
    char *newstr;
    size_t strsize;

    if (((char *)string == (char *)NULL) || (*string == Null))
      return((char *)NULL);

    strsize = Strlen(string) + 1;  /* Include room for the final Null. */
    if (strsize <= 1)
      return((char *)NULL);

    if ((newstr = (char *)Malloc(strsize * sizeof(char))) == (char *)NULL) {
      wipoutput(stderr, "Could not allocate memory to make a copy of [%s].\n",
        string);
      return((char *)NULL);
    }

    (void)Strcpy(newstr, string);

    return(newstr);
}

