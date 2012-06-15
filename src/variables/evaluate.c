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
static    int  wipisop(const char *inword);
static double  wipdoop(const char *op, double arg1, double arg2, \
                      LOGICAL *error);
static    int  wipisfunction(const char *inword);
static double  wipdofunc(const char *inwrd, double arg, LOGICAL *error);
          int  wipisnumber(const char *inword, double *retval);
          int  wipsetuser(const char *input);
         char *wipgettoken(char *output, const char *input, char **next);
         char *wipbracextract(const char *inword, char **left);
*/

#include "wip.h"

/* Global variables for just this file */

static double USERVAR[MAXVAR]; /* USERVAR is an array of user setable variables. */

/* Code */

/* Returns 1 if "inword" is a predefined operation; 0 otherwise. */
static int wipisop(const char *inword)
{
    char *ptr;

    if ((ptr = (inword)) == (char *)NULL)
      return(0);

    if ((Strcmp("+",   ptr) == 0) || (Strcmp("-",   ptr) == 0) ||
        (Strcmp("*",   ptr) == 0) || (Strcmp("/",   ptr) == 0) ||
        (Strcmp("%",   ptr) == 0) || (Strcmp("**",  ptr) == 0) ||
        (Strcmp("max", ptr) == 0) || (Strcmp("min", ptr) == 0) ||
        (Strcmp("==",  ptr) == 0) || (Strcmp("!=",  ptr) == 0) ||
        (Strcmp("<",   ptr) == 0) || (Strcmp(">",   ptr) == 0) ||
        (Strcmp("<=",  ptr) == 0) || (Strcmp(">=",  ptr) == 0) ||
        (Strcmp("||",  ptr) == 0) || (Strcmp("&&",  ptr) == 0) ||
        (Strcmp("^",   ptr) == 0)) {
      return(1);
    } else if ((*ptr == ESC) && (Strlen(ptr) == 1)) {
      return(1);
    }
    return(0);
}

/* Returns the result of the operation (arg1 op arg2). */
static double wipdoop(const char *inword, double arg1, double arg2, LOGICAL *error)
{
    char *ptr;
    double arg;

    *error = TRUE;
    if ((ptr = (inword)) == (char *)NULL)
      return(0);

    if (Strcmp(ptr, "+") == 0) {
      arg = arg1 + arg2;
    } else if (Strcmp(ptr,   "-") == 0) {
      arg = arg1 - arg2;
    } else if (Strcmp(ptr,   "*") == 0) {
      arg = arg1 * arg2;
    } else if (Strcmp(ptr,   "/") == 0) {
      arg = arg1 / arg2;
    } else if (Strcmp(ptr,   "%") == 0) {
      arg = arg1 - (arg2 * INT(arg1 / arg2));
    } else if (*ptr == ESC) {
      arg = INT(arg1 / arg2);
    } else if (Strcmp(ptr, "max") == 0) {
      arg = MAX(arg1, arg2);
    } else if (Strcmp(ptr, "min") == 0) {
      arg = MIN(arg1, arg2);
    } else if (Strcmp(ptr,  "**") == 0) {
      if (arg1 <= 0.0) {
        arg = 0.0;
        if (arg1 == 0.0) {
          if (arg2 <= 0.0) {
            wipoutput(stderr, "Cannot take exponent of negative value.\n");
            return(0);
          }
        } else {
          long tmpint;
          tmpint = arg2;
          if (tmpint != arg2) {
            wipoutput(stderr, "Cannot take exponent of negative value.\n");
            return(0);
          }
          arg = EXP(arg2 * LOG(-arg1)); /* Fudge. */
          if (tmpint & 1) arg = -arg;
        }
      } else {
        arg = EXP(arg2 * LOG(arg1)); /* Fudge. */
      }
    } else if (Strcmp(ptr,   "<") == 0) {
      arg = arg1 < arg2;
    } else if (Strcmp(ptr,   ">") == 0) {
      arg = arg1 > arg2;
    } else if (Strcmp(ptr,  "<=") == 0) {
      arg = arg1 <= arg2;
    } else if (Strcmp(ptr,  ">=") == 0) {
      arg = arg1 >= arg2;
    } else if (Strcmp(ptr,  "==") == 0) {
      arg = arg1 == arg2;
    } else if (Strcmp(ptr,  "!=") == 0) {
      arg = arg1 != arg2;
    } else if (Strcmp(ptr,  "&&") == 0) {
      arg = arg1 && arg2;
    } else if (Strcmp(ptr,  "||") == 0) {
      arg = arg1 || arg2;
    } else if (Strcmp(ptr,   "^") == 0) {
      arg = !(arg1 && arg2) && (arg1 || arg2);
    } else {
      wipoutput(stderr, "Unrecognized arithmetic operator: %s\n", inword);
      return(0);
    }
    *error = FALSE;
    return(arg);
}

/*  Returns 1 if "inword" is a predefined (standard) function; 0 otherwise. */
static int wipisfunction(const char *inword)
{
    register char *ptr, *opbrac;
    char word[BUFSIZ];

    (void)Strcpy(word, inword); /* Input string is already in lower case. */
    if ((ptr = (word)) == (char *)NULL) return(0);

    /* End the string at the first open brace. */

    if ((opbrac = Strchr(ptr, '(')) != (char *)NULL) *opbrac = Null;
    if ((opbrac = Strchr(ptr, '[')) != (char *)NULL) *opbrac = Null;
    if ((opbrac = Strchr(ptr, '{')) != (char *)NULL) *opbrac = Null;
 
    /* ptr points to the function name without any arguments or any */
    /* braces (i.e. if name = thisfunc(x), ptr points to thisfunc). */

    if ((Strcmp("sin",  ptr) == 0) || (Strcmp("sind",  ptr) == 0) ||
        (Strcmp("asin", ptr) == 0) || (Strcmp("asind", ptr) == 0) ||
        (Strcmp("cos",  ptr) == 0) || (Strcmp("cosd",  ptr) == 0) ||
        (Strcmp("acos", ptr) == 0) || (Strcmp("acosd", ptr) == 0) ||
        (Strcmp("tan",  ptr) == 0) || (Strcmp("tand",  ptr) == 0) ||
        (Strcmp("atan", ptr) == 0) || (Strcmp("atand", ptr) == 0) ||
        (Strcmp("sqrt", ptr) == 0) || (Strcmp("ln",    ptr) == 0) ||
        (Strcmp("log",  ptr) == 0) || (Strcmp("log10", ptr) == 0) ||
        (Strcmp("exp",  ptr) == 0) || (Strcmp("abs",   ptr) == 0) ||
        (Strcmp("int",  ptr) == 0) || (Strcmp("nint",  ptr) == 0) ||
        (Strcmp("rand", ptr) == 0) || (Strcmp("gasdev", ptr) == 0)) {
      return(1);
    }
    return(0);
}

/* Returns the result of the operation (F(arg)). */
static double wipdofunc(const char *inword, double arg, LOGICAL *error)
{
    long int narg;
    static long int randarg = (-911);
    double value;

    *error = TRUE;
    if (Strcmp("sin", inword) == 0) {
      value = SIN(arg);
    } else if (Strcmp("sind", inword) == 0) {
      arg *= RPDEG;
      value = SIN(arg);
    } else if (Strcmp("asin", inword) == 0) {
      if (ABS(arg) > 1.0) goto BADVALUE;
      value = ASIN(arg);
    } else if (Strcmp("asind", inword) == 0) {
      if (ABS(arg) > 1.0) goto BADVALUE;
      value = ASIN(arg) / RPDEG;
    } else if (Strcmp("cos", inword) == 0) {
      value = COS(arg);
    } else if (Strcmp("cosd", inword) == 0) {
      arg *= RPDEG;
      value = COS(arg);
    } else if (Strcmp("acos", inword) == 0) {
      if (ABS(arg) > 1.0) goto BADVALUE;
      value = ACOS(arg);
    } else if (Strcmp("acosd", inword) == 0) {
      if (ABS(arg) > 1.0) goto BADVALUE;
      value = ACOS(arg) / RPDEG;
    } else if (Strcmp("tan", inword) == 0) {
      value = TAN(arg);
    } else if (Strcmp("tand", inword) == 0) {
      arg *= RPDEG;
      value = TAN(arg);
    } else if (Strcmp("atan", inword) == 0) {
      value = ATAN(arg);
    } else if (Strcmp("atand", inword) == 0) {
      value = ATAN(arg) / RPDEG;
    } else if (Strcmp("sqrt", inword) == 0) {
      if (arg < 0.0) goto BADVALUE;
      value = SQRT(arg);
    } else if (Strcmp("ln", inword) == 0) {
      if (arg <= 0.0) goto BADVALUE;
      value = LOG(arg);
    } else if ((Strcmp("log", inword) == 0) || (Strcmp("log10", inword) == 0)) {
      if (arg <= 0.0) goto BADVALUE;
      value = LOG10(arg);
    } else if (Strcmp("exp", inword) == 0) {
      value = EXP(arg);
    } else if (Strcmp("abs", inword) == 0) {
      value = ABS(arg);
    } else if (Strcmp("int", inword) == 0) {
      value = INT(arg);
    } else if (Strcmp("nint", inword) == 0) {
      value = NINT(arg);
    } else if (Strcmp("rand", inword) == 0) {
      narg = NINT(arg);
      if (narg >= 0) narg = randarg;
      value = wiprand(&narg);
      randarg = narg;
    } else if (Strcmp("gasdev", inword) == 0) {
      narg = NINT(arg);
      if (narg >= 0) narg = randarg;
      value = wipgaussdev(&narg);
      randarg = narg;
    } else {
      wipoutput(stderr, "Unrecognized arithmetic operator: %s\n", inword);
      return(0);
    }
    *error = FALSE;
    return(value);

BADVALUE:
    wipoutput(stderr, "Illegal operation: %s %G\n", inword, arg);
    return(0);
}

/*
 *  This routine will test if the input string is just a simple number.
 *  This takes into account integers, floating point numbers, and numbers
 *  presented in scientific notation (including Fortran's D-format).
 *  This routine returns 0 if the input string could not be formatted
 *  entirely into a number and the value of "retval" will be undefined;
 *  otherwise, the number will be assigned to "retval" and 1 will be returned.
 */
int wipisnumber(const char *inword, double *retval)
{
    char *ptr;
    char temp[50];
    int dummy, expon;
    double arg;

    if ((ptr = (inword)) == (char *)NULL)
      return(0);                                /* Nothing to process. */

    SPrintf(temp, "%s~~1", ptr);           /* Fudge to make test work. */
    if ((SScanf(temp, "%lg~~%d", &arg, &dummy) == 2) && (dummy == 1)) {
      *retval = arg;                /* Token was just a simple number. */
    } else if ((SScanf(temp, "%lg%*[dD]%d~~%d", &arg, &expon, &dummy) == 3) &&
               (dummy == 1)) {          /* Token was a Fortran double. */
      *retval = arg;
      if (expon != 0)
        *retval *= EXP(expon * LOG(10.0));
    } else {                         /* Token was not a simple number. */
      return(0);
    }

    return(1);
}


char *wipgettoken(char *output, const char *input, char **next)
{
/*
 * This function parses the input string and returns the next token and
 * a pointer to the character following the current token (address relative
 * to the input string).  The syntax of the input string can contain any
 * literal text enclosed in double quotes ("), single user variables or
 * string variables, and multiple expressions to be evaluated that are
 * enclosed in braces (see definition of BRACE in wip.h).
 *
 * NOTE: that the returned token is located in the string OUTPUT and this
 * should be large enough to hold the token.  No test for this is done!
 * The pointer returned is the first character of OUTPUT.
 */
    char *ptr, *par, *current, *ptrbegin;
    char *openbrace, *closebrace;

    if ((ptr = (input)) == (char *)NULL)       /* Nothing here. */
      return((char *)NULL);
    current = par = output;                   /* Initialize the pointers. */

    if (*ptr == '"') {               /* Special case for a quoted string. */
      *par++ = *ptr++;                  /* Copy the open quote character. */
      while ((*ptr != Null) && (*ptr != '"'))
        *par++ = *ptr++;                  /* Copy over the quoted string. */
      *par++ = '"'; /* Put a final double quote at the end of the string. */
      *par++ = Null;                             /* Terminate the string. */
      if (*ptr == '"') ptr++;  /* Skip the quote character, if necessary. */
      *next = ptr;                            /* Identify where we ended. */
      return(current);                    /* All done if this is a quote. */
    }

    if ((*ptr == '-') && (!WHITE(*(ptr+1))))              /* Unary minus. */
      *par++ = *ptr++;               /* Copy the minus sign and continue. */

    if (BRACE(*ptr)) {                /* Is this character an open brace? */
      closebrace = wipbracextract(ptr, &openbrace);   /* Find it's match. */
      if (ptr != openbrace) {                /* Check that all went well. */
        wipoutput(stderr, "Format error: %s\n", input);
        return((char *)NULL);
      }
      if (closebrace != (char *)NULL) {        /* A closebrace was found. */
        closebrace++;                         /* Move past closing brace. */
        while (ptr != closebrace) *par++ = *ptr++;  /* Copy braced token. */
        *par++ = Null;                           /* Terminate the string. */
      } else {       /* No closebrace found; copy to end of input string. */
        while (*ptr != Null) *par++ = *ptr++;  /* Copy over the string... */
        switch (*openbrace) {               /* Include a closing brace... */
          case '{': *par++ = '}'; break;
          case '[': *par++ = ']'; break;
          default : *par++ = ')'; break;
        }
        *par++ = Null;                    /* ...and terminate the string. */
      }
    } else {      /* What remains is either a function or a simple token. */
      ptrbegin = ptr;
      while ((*ptr != Null) && (!WHITE(*ptr)))
        *par++ = *ptr++;             /* First, parse a simple word token. */
      *par = Null;        /* Terminate the token and test for a function. */
      if (*ptr != Null) {                    /* Still more in the string? */
        closebrace = wipbracextract(current, &openbrace);  /* A function? */
        if ((openbrace != (char *)NULL) && (closebrace == (char *)NULL)) {
                                                           /* A function. */
          closebrace = wipbracextract(ptrbegin, &openbrace);  /* Get end. */
          if (closebrace != (char *)NULL) closebrace++;
                                           /* Get past the closing brace. */
          while (ptr != closebrace) *par++ = *ptr++;/* Copy braced token. */
          *par++ = Null;                         /* Terminate the string. */
        } else {                                          /* No function. */
          ptr++;                     /* Advance past the end of the word. */
        }
      }
    }
    *next = ptr;                              /* Identify where we ended. */
    return(current);
}

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
