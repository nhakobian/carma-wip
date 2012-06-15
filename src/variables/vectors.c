/*
	<vectors.c>
	04oct91 jm  Original code.
	26feb92 jm  Added wipvectornpts and modified wipvector routine.
		    This was due to a change in the VECTOR structure to
		    include the current number of points in the array.
	26feb92 jm  Modified wipNewVector for VECTOR->npts member.
	31jul92 jm  Modified to use wipnewstring() command.
	01aug92 jm  Code combined from multiple source files into a
		    single file.  This is to hide as much structure
		    as possible.  Also changed the order in which
		    new stack items are loaded (at the front rather
		    than at the end); this should mean more recent
		    additions will be found quicker.  Also, sort the
		    initially defined elements such that more commonly
		    accessed items are closer to the end of the list.
	15sep92 jm  Added wipisvecfunc() and wipvecfunc() functions.
	16sep92 jm  Added wipvectorinit() function and added bounds
		    check to wipvectornpts() routine.
	29sep92 jm  Modified wipvectorinit() to include a npts input value.
	01oct92 jm  Changed initVector() to a static function called
		    once by find_vector().
	31jan94 jm  Added a test for closing brace in find_vector().
        30nov00 pjt ansi-c

Routines:
static    int  initVector(void);
static VECTOR *find_vector(const char *inname, int *indx);
       double  wipgetvec(const char *inword, LOGICAL *error);
          int  wipsetvec(const char *inword, double value);
*/

#define WIP_VECTORS
#include "wip.h"
#include "vectors.h"

/* Global variables for just this file */

static VECTOR *VECHEAD = (VECTOR *)NULL;

/* Code */

/*  Returns 0 if successful, 1 on error. */
static int initVector(void)
{
    register int j, number;
    int maxsize;
    double dsize;
    LOGICAL error;
    VECTOR *vb;

    number = sizeof(initialVecArray) / sizeof(initialVecArray[0]);
    maxsize = 0;

    VECHEAD = (VECTOR *)NULL;
    for (j = 0; j < number; j++) {
      vb = &initialVecArray[j];
      vb->next = VECHEAD;
      VECHEAD = vb;
      if (vb->size < 1) {
        if (maxsize < 1) {    /* Get the user specified array maximum. */
          dsize = wipgetvar("maxarray", &error);
          maxsize = (error == TRUE) ? 20000 : NINT(dsize);
        }
        vb->size = maxsize;
      }
      if ((vb->value = vector(vb->size)) == (float *)NULL) {
        wipoutput(stderr, "Could not allocate storage for the array [%s].\n",
          vb->name);
        return(1);
      }
    }

    return 0;
}

/*
 *  Returns a pointer to the VECTOR structure and the index requested
 *  if "inname" is defined as a vector; a pointer to NULL otherwise.
 */
static VECTOR *find_vector(const char *inname, int *indx)
{
    char *par, *ptr, *closing;
    char word[STRINGSIZE];
    int arrayindex;
    double arg;
    static LOGICAL FirstTime = TRUE;
    VECTOR *vb;

    if (FirstTime == TRUE) {     /* Initialize the predefined vectors. */
      FirstTime = FALSE;
      if (initVector() != 0) {
        wipoutput(stderr, "Trouble initializing the vectors!\n");
        wipoutput(stderr, "Some vectors will be undefined!\n");
      }
    }

    ptr = Strncpy(word, inname, STRINGSIZE);      /* Make a local copy. */
    word[STRINGSIZE-1] = Null;           /* Make sure it is terminated. */
    if ((par = (ptr)) == (char *)NULL)       /* Nothing here. */
      return((VECTOR *)NULL);
    wiplower(par);                               /* Make it lower case! */

    closing = wipbracextract(par, &ptr);    /* Find the index argument. */
    if (ptr == (char *)NULL)                      /* No argument found. */
      return((VECTOR *)NULL);

    *ptr++ = Null;           /* par now points to just the vector name. */
    if (closing != (char *)NULL)          /* A closing brace was found. */
      *closing = Null;           /* ptr now points to the vector index. */

    for (vb = VECHEAD; vb != (VECTOR *)NULL; vb = vb->next)
      if (Strcmp(par, vb->name) == 0)                      /* Found it. */
        break;

    if (vb == (VECTOR *)NULL)                             /* Not found. */
      return((VECTOR *)NULL);

    /*if (wiparguments(&ptr, 1, &arg) != 1)       /* Get the array index. */
    /*  return((VECTOR *)NULL); */
    arrayindex = 0.5 + arg;
    arrayindex--;              /* Change from 1 index based to 0 based. */
    if ((arrayindex < 0) || (arrayindex >= vb->size))
      return((VECTOR *)NULL);

    *indx = arrayindex;
    return vb;
}

/*
 *  Returns, if the vector exists, the current value of the vector
 *  at the desired index and sets error to FALSE; otherwise, it
 *  returns 0 and sets error to TRUE.
 */
double wipgetvec(const char *inword, LOGICAL *error)
{
    int arrayindex;
    double value;
    VECTOR *vb;

    if ((vb = find_vector(inword, &arrayindex)) == (VECTOR *)NULL) {
      wipoutput(stderr, "Unknown vector: %s\n", inword);
      *error = TRUE;
      return(0);
    }

    *error = FALSE;
    if (arrayindex > (vb->npts - 1)) vb->npts = arrayindex + 1;
    value = vb->value[arrayindex];
    return value;
}

/* Returns 0 if the vector exists and was set; 1 if an error occured. */
int wipsetvec(const char *inword, double value)
{
    int arrayindex;
    VECTOR *vb;

    if ((vb = find_vector(inword, &arrayindex)) == (VECTOR *)NULL) {
      wipoutput(stderr, "Unknown vector: %s\n", inword);
      return(1);
    }

    if (arrayindex > (vb->npts - 1)) vb->npts = arrayindex + 1;
    vb->value[arrayindex] = value;
    return 0;
}

