/*
	<vars.c>
	03oct91 jm  Original code.
	31jul92 jm  Code combined from multiple source files into a
		    single file.  This is to hide as much structure
		    as possible.  Also changed the order in which
		    new stack items are loaded (at the front rather
		    than at the end); this should mean more recent
		    additions will be found quicker.  Also, sort the
		    initially defined elements such that more commonly
		    accessed items are closer to the end of the list.
	01oct92 jm  Changed initVariable() to a static function called
		    once by find_variable().
         9oct00 pjt no more PROTOTYPE

Routines:
static      int  initVariable(void);
static VARIABLE *find_variable(const char *inname);
         double  wipgetvar(const char *inword, LOGICAL *error);
            int  wipsetvar(const char *inword, double value);
*/

#define WIP_VARIABLES
#include "wip.h"
#include "variables.h"

/* Global variables for just this file */

static VARIABLE *VARHEAD = (VARIABLE *)NULL;

/* Code */

/*  Always returns 0, but function needs to return a status int. */
static int initVariable(void)
{
    register int j, number;
    VARIABLE *vb;

    number = sizeof(initialVarArray) / sizeof(initialVarArray[0]);

    VARHEAD = (VARIABLE *)NULL;
    for (j = 0; j < number; j++) {
      vb = &initialVarArray[j];
      vb->next = VARHEAD;
      VARHEAD = vb;
    }

    return(0);
}

/*
 *  Returns a pointer to the VARIABLE structure if "inname" is defined
 *  as a variable; a pointer to NULL otherwise.
 */
static VARIABLE *find_variable(const char *inname)
{
    char *par, *ptr;
    char word[STRINGSIZE];
    static LOGICAL FirstTime = TRUE;
    VARIABLE *vb;

    if (FirstTime == TRUE) {   /* Initialize the predefined variables. */
      FirstTime = FALSE;
      if (initVariable() != 0) {
        wipoutput(stderr, "Trouble initializing the variables!\n");
        wipoutput(stderr, "Some variables will be undefined!\n");
      }
    }

    ptr = Strncpy(word, inname, STRINGSIZE);     /* Make a local copy. */
    word[STRINGSIZE-1] = Null;          /* Make sure it is terminated. */
    if ((par = wipparse(&ptr)) == (char *)NULL)       /* Nothing here! */
      return((VARIABLE *)NULL);
    wiplower(par);                              /* Make it lower case! */

    for (vb = VARHEAD; vb != (VARIABLE *)NULL; vb = vb->next)
      if (Strcmp(par, vb->name) == 0)                     /* Found it. */
        return(vb);

    return((VARIABLE *)NULL);                            /* Not found. */
}

/*
 *  Returns, if the variable exists, the current value of the variable
 *  and sets error to FALSE; otherwise, it returns 0 and sets error to TRUE.
 */
double wipgetvar(const char *inword, LOGICAL *error)
{
    VARIABLE *vb;

    if ((vb = find_variable(inword)) == (VARIABLE *)NULL) {
      wipoutput(stderr, "Unknown variable - %s\n", inword);
      *error = TRUE;
      return(0);
    }

    *error = FALSE;
    return(vb->value);
}

/* Returns 0 if the variable exists and was set; 1 if an error occured. */
int wipsetvar(const char *inword, double value)
{
    VARIABLE *vb;

    if ((vb = find_variable(inword)) == (VARIABLE *)NULL) {
      wipoutput(stderr, "Unknown variable - %s\n", inword);
      return(1);
    }

    vb->value = value;
    return(0);
}
