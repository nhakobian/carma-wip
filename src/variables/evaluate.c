/*
	<evaluate.c>
	09jul90 jm  Original code.
	29oct91 jm  Modified for new stack structure.
	18nov91 jm  Added a check for the end of a string to bracextract.
	24feb92 jm  Added routine wipgettoken().
	01aug92 jm  Reordered code so statics appear at the top of the file.
		    Also added a bounds check for USERVAR.
        03aug92 jm  Modified wipsetuser() to return status (void -> int)
		    rather than using a passed LOGICAL pointer.
        23sep92 jm  Added wiptokenexists() test routine.
        09aug93 jm  Added wipisnumber() function.
        10nov93 jm  Modified image variable to new opaque pointer type.
        02jul96 jm  Added rand and gasdev functions.
        22sep00 pjt USERVAR is now bigger, and better protected to overrun
         9oct00 pjt no more PROTOTYPE #ifdefs
	

Routines:
         char *wipbracextract(const char *inword, char **left);
*/

#include "wip.h"

/* Code */

char *wipbracextract(const char *inword, char **left)
{
    char *ptr;
    int level, chopen, chclose;
 
    *left = (char *)NULL;
    ptr = (char *)inword;
    while ((*ptr != Null) && (*ptr != '#')) {
      if ((*ptr == '(') || (*ptr == '[') || (*ptr == '{')) break;
      ptr++;
    }
    if (*ptr == Null) return((char *)NULL);

    *left = ptr;
    chopen = *ptr++;
    switch (chopen) {
      case '(': chclose = ')'; break;
      case '[': chclose = ']'; break;
      case '{': chclose = '}'; break;
      default: *left = (char *)NULL; return((char *)NULL);
    }
    level = 1;
    while ((*ptr != Null) && (*ptr != '#') && (level > 0)) {
      if (*ptr == chopen) level++;
      if (*ptr == chclose) level--;
      if (level) ptr++;
    }
    if (*ptr == Null) return((char *)NULL); /* End of string. */
    if (*ptr == '#') return((char *)NULL); /* Comment character. */
    return(ptr);
}
