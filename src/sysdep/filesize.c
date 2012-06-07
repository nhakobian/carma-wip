/*
	<filesize.c>
	17sep90 jm  Original code.
	17sep90 jm  Modified error returns to send literal long ints.
         9oct00 pjt no PROTOTYPE's

Routines:
long int filesize(FILE *fp);
*/

#include "wip.h"

/* Global Variables needed just for this file */

/* Code */

/*
 *  Returns -1 if an error seeking; otherwise the routine
 *  returns the size of a file in bytes and leaves the file
 *  at the beginning when finished (successful).
 *
 *  This routine assumes FSEEK and FTELL are present on the system.
 */
long int filesize(FILE *fp)
{
      long int fsize;

      if (Fseek(fp, 0L, SEEK_END) != 0) {
        wipoutput(stderr, "Error searching for the end of the file.\n");
        return(-1L);
      }
      fsize = Ftell(fp);
      if (Fseek(fp, 0L, SEEK_SET) != 0) {
        wipoutput(stderr, "Error finding the beginning of the file.\n");
        return(-1L);
      }
      return(fsize);
}
