/*
	<find.c>
	04oct91 jm  Original code.
	06nov91 jm  Added new/freeitem code.
	16feb92 jm  Modified new/freeitem code to allow multiple declarations.
	01aug92 jm  Substantially modified to move all references to
		    vectors, variables, and strings variables to their
		    own private routines.  Also add "strings" to new and
		    free commands.
	23sep92 jm  Modified wipnewitem() to use routine which tests
		    for previously existing items.
         9oct00 pjt no more PROTOTYPE #ifdefs

Routines:
   int wipisuserfunc(const char *name);
double wipuserfunc(const char *inword, double arg, LOGICAL *error);
*/

#include "wip.h"

/* Global variables for just this file */

/* Code */

/* Returns 1 if user function; 0 otherwise. */
int wipisuserfunc(const char *name)
{
    register char *ptr, *opbrac;
    char word[BUFSIZ];

    (void)Strcpy(word, name);
    if ((ptr = (word)) == (char *)NULL) return(0);

    /* End the string at the first open brace. */

    if ((opbrac = Strchr(ptr, '(')) != (char *)NULL) *opbrac = Null;
    if ((opbrac = Strchr(ptr, '[')) != (char *)NULL) *opbrac = Null;
    if ((opbrac = Strchr(ptr, '{')) != (char *)NULL) *opbrac = Null;

    /* ptr points to the function name without any arguments or any */
    /* braces (i.e. if name = userfunc(x), ptr points to userfunc). */

    /* NO USER FUNCTIONS YET... */
    return(0);
}

/* ARGSUSED */
double wipuserfunc(const char *inword, double arg, LOGICAL *error)
{
    /* NO USER FUNCTIONS YET... */
    *error = TRUE;
    return(0.0);
}
