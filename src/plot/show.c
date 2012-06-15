/*
	<show.c>
	14apr91 jm  Original code.
	28oct91 jm  Modified for new image variable.
	19jul91 jm  Changed show() to reflect change in variable syntax.
	28feb92 jm  Changed show() to allow selectable items to be displayed.
		    This meant that the call sequence was changed to
		    only include the "rest" string.  All else is retrievable.
	30sep93 jm  Added EPS to value in log10 expression when value < 1
		    in wipfpfmt() so that 0.1 & 0.2 both work out correctly.
	10nov93 jm  Modified image variable to new opaque pointer type.
	12oct95 jm  Modified to use wipgetcxy.
	24apr96 jm  Modified to use wipgetcir.

Routines:
char *wipfpfmt(float arg, int nfig);
char *wipifmt(float arg);
*/

#include "wip.h"

/* Global variables for just this file */

/* Code */

char *wipfpfmt(float arg, int nfig)
{
      int ndec, iexpo, nchar;
      char *ptr, fspec;
      char fmt[20];
      static char field[80];
      float val, expo;

      val = ABS(arg);
      if (val == 0.0) {
        ndec = nfig;
        nchar = nfig + 3;
        fspec = 'f';
      } else if ((val < 1.0e6) && (val > 1.0e-4)) {
        if (val < 0.9) val += 1.0e-5;
        expo = LOG10(val);
        iexpo = expo;
        if (expo >= 0.0) iexpo++;
        ndec = MAX(nfig - iexpo, 0);
        nchar = ndec + 2 + MAX(iexpo, 0);
        fspec = 'f';
      } else {
        ndec = nfig - 1;
        nchar = nfig + 6;
        fspec = 'E';
      }
      SPrintf(fmt, "%%%d.%d%c", nchar, ndec, fspec);
      SPrintf(field, fmt, arg);
      ptr = field;
      return(ptr);
}

char *wipifmt(float arg)
{
      int iexpo, nchar;
      char *ptr;
      char fmt[20];
      static char field[80];
      float val, expo;

      val = ABS(arg);
      if (val == 0.0) {
        nchar = 2;
      } else {
        expo = LOG10(val);
        iexpo = expo;
        nchar = iexpo + 2;
      }
      SPrintf(fmt, "%%%dd", nchar);
      SPrintf(field, fmt, NINT(arg));
      ptr = field;
      return(ptr);
}
