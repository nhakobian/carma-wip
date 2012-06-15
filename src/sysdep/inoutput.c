/*
	<inoutput.c>
	18jul90 jm  Original code.
	16aug92 jm  Added wipexit() routine.
	21jul93 jm  Modified wipinput to use fgets rather than getc.
		    Also added #ifdef for READLINE use.
	25jul94 jm  Modified wipoutput* to flush if last character is a \n.
	22aug94 jm  Combined all individual wipoutput* calls into one
		    varargs form.  Once that method is tested, I will remove
		    the individual calls....  Also added ability to turn
		    off READLINE history archiving with a command line option.
	12dec94 jm  Removed individual flavors of wipoutout*.  Also
		    added another option so the user can disable READLINE
		    via a command line option.
	21jan98 jm  VMS reserves the readonly keyword, so it was changed
		    to justread in wipbegin().  Also modified definition
		    of historyFile variable for VMS machines (is this
		    even available for VMS machines?).
 	 9oct00 pjt no more #ifdef PROTOTYPE

Routines:
void wipoutput(FILE *fp, const char *fmt, ...);
*/

#include "wip.h"

/* Global variables for just this file */

static int quietMode = 0;

#ifdef READLINE

static LOGICAL WriteHistory;
static LOGICAL UseReadLine;
#ifdef WIPVMS
static char *historyFile = "wiphistory.log";
#else
static char *historyFile = "./.wiphistory";
#endif /* WIPVMS */

extern  int  read_history(char *filename);
extern  int  write_history(char *filename);
extern char *readline(char *prompt);
extern void  add_history(char *string);

#endif /* READLINE */

/* Code */

#ifndef NOVARARGS
/*VARARGS2*/
void wipoutput(FILE *fp, const char *fmt, ...)
{
    va_list ap;

    if ((fp == stdout) && (quietMode > 0)) {    /* No messages wanted. */
      return;
    }

    va_start(ap, fmt);

    VFPrintf(fp, fmt, ap);
    if (strchr(fmt, '\n') != (char *)NULL) {
#ifdef WIPVMS
      /*
       * This next statement is added to keep error messages
       * from being overwritten by the next prompt.
       */
      if (fp == stderr) {
        FPrintf(fp, "\n");
      }
#endif /* WIPVMS */
      Fflush(fp);
    }


    va_end(ap);

    return;
}
#endif /* !NOVARARGS */
