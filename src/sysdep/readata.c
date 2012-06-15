/*
	<readata.c>
	24jul90 jm  Original C code.
	13apr91 jm  Modified wipreadcol() to return EOF on failure.
	28feb92 jm  Increased dimension of character array "line" in
		    wipreadcol() from STRINGSIZE to BUFSIZ.
	02aug92 jm  Modified wipopenfile() to return status (void -> int)
		    rather than using a passed LOGICAL pointer.
	16aug92 jm  Added wipreadstr() routine.
	28sep92 jm  Modified wipreadcol() to test if a file exists only
		    if the column to read is greater than zero.  Added a
		    clear flag to remove any EOF's when data is read
		    from stdin; this should keep WIP from exiting.  Also
		    added a prompt when data is read from stdin.  Changed
		    temporary file usage from tmpfile() to tmpnam().
	12jan93 jm  Modified wipopenfile() to check that the opened file
		    does have something inside it.  Modified wipreadcol()
		    to save a copy of input line to use in error message.
        21jul93 jm  Modified for syntax change of wipinput().
	29mar95 jm  Modified LINE2 to allow an arbitrary maximum size.
		    See the comments below for more details.  Also
		    modified wipopenfile() to drop maxsize requirement.
	18nov97 jm  Modified wipreadcol() to warn user when number of
	            points is larger than (and truncated to) maxsize.
	16nov04 pjt add suggestion that's an FAQ
        14apr10 pjt no more prototypes

Routines:
void  wiplines(int first, int last);
void  wipgetlines(int *first, int *last);
 int  wipopenfile(const char *name);
 int  wipreadcol(float array[], int maxsize, int nc);
*/

#include "wip.h"

/* Global variables for just this file */

static FILE *datafp = (FILE *)NULL;

/*
 *  LINE1 is the first data line; lines 1 to LINE1-1 are skipped
 *  before reading data.  LINE2 is the last line to read.  If LINE2
 *  is less than LINE1, it is treated as if LINE2 were infinite.
 */
static int LINE1;
static int LINE2;

/* Code */

void wiplines(int first, int last)
{
    LINE1 = first;
    LINE2 = last;
    return;
}

void wipgetlines(int *first, int *last)
{
    *first = LINE1;
    *last = LINE2;
    return;
}

/*  Returns 1 on error; 0 otherwise. */
int wipopenfile(const char *name)
{
    char *ptr;
    char enddata[8];
    char line[STRINGSIZE];
    int inflag;
    static char *tmpName = (char *)NULL;   /* Save the temp file name. */

    if (datafp != (FILE *)NULL) {   /* datafp is file global variable. */
      Fclose(datafp);
      if (tmpName != (char *)NULL) {
        if (Remove(tmpName) != 0) {    /* Only remove temporary files. */
          wipoutput(stderr, "Could not remove temporary file [%s].\n", tmpName);
        }
        tmpName = (char *)NULL;
      }
    }

    ptr = Strncpy(line, name, STRINGSIZE);       /* Make a local copy. */
    line[STRINGSIZE-1] = Null;            /* Insure a Null at the end. */
    wiplower(ptr);                              /* Make it lower case. */
    if (Strcmp("stdin", ptr) != 0) {              /* An external file. */
      ptr = (char *)name;            /* Point to un-lowered file name. */
    } else {                                       /* Read from stdin. */
      /**
       * Use mkstemp to create temporary file name, tmpnam() is deprecated.
       */
      char tmpName[] = "/tmp/wiptmpXXXXXX";
      int tmp_fd     = mkstemp(tmpName);
      if ((datafp = fdopen(tmp_fd, "w")) == (FILE *)NULL) {
        wipoutput(stderr, "Trouble opening a scratch file... \n");
        wipoutput(stderr, "\t...is the temporary file [%s] writeable?\n",
          tmpName);
        return 1;
      }

      wipoutput(stdout,
        "Enter data terminated by the word `enddata' on a line by itself.\n");

      while ((inflag = wipinput(stdin, "Data Input> ", line, STRINGSIZE))
                     != (int)EOF) {
        if ((inflag == (int)Null) || ((ptr = (line)) == (char *)NULL))
          continue;
        (void)Strncpy(enddata, ptr, 7);
        enddata[7] = Null;
        wiplower(enddata);
        if (Strncmp(enddata, "enddata", 7) == 0) break;
        wipoutput(datafp, "%s\n", line);
      }
      Clearerr(stdin);               /* Remove any EOF or error flags. */
      Fclose(datafp);      /* Close it from writing; open for reading. */
      ptr = tmpName;              /* Point to the temporary file name. */
    }

    if ((datafp = Fopen(ptr, "r")) == (FILE *)NULL) {
      wipoutput(stderr, "Error opening file [%s] for reading.\n", ptr);
      return 1;
    }

    if (filesize(datafp) <= 0L) {
      wipoutput(stderr, "No data within file [%s] to read.\n", ptr);
      return 1;
    }

    wiplines(1, 0);
    return 0;
}
