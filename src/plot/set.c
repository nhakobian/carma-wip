/*
	<set.c>
	04mar91 jm  Original code.
	19jul91 jm  Changed set routines to query current value before
		    setting it in variable code.
	15aug92 jm  Added wipgetlimits() routine.
	15sep92 jm  Modified error messages to be a bit more verbose.
	13nov96 jm  Added wipDebugMode() routine.

Routines:
void wipcolor(int color);
void wipexpand(double exp);
void wipfill(int fill);
void wipfont(int font);
void wipltype(int style);
void wiplw(int width);
void wipsetbgci(int color);
void wipsetitf(int type);
void wipsetangle(double ang);
void wipsetslope(double xa, double xb, double ya, double yb);
void wiplimits(void);
void wipgetlimits(float *x1, float *x2, float *y1, float *y2);
void wipviewport(void);
void wipgetvp(float *vx1, float *vx2, float *vy1, float *vy2);
void wipsetr(float tr[]);
void wipgetr(float tr[]);
void wipsetsub(int subx1, int subx2, int suby1, int suby2);
void wipgetsub(int *subx1, int *subx2, int *suby1, int *suby2);
void wipsetick(float xtick, int nxsub, float ytick, int nysub);
void wipgetick(float *xtick, int *nxsub, float *ytick, int *nysub);
void wipsetsubmar(float subx, float suby);
void wipgetsubmar(float *subx, float *suby);
void wipsetcir(int cmin, int cmax);
void wipgetcir(int *cmin, int *cmax);
 int wipDebugMode(void);
*/

#include "wip.h"

/* Global Variables needed just for this file */

/* Code */

/* This macro checks the validity of integer arguments below. */
#define CHECK(what,in,val) \
  if ((val) != (in)) { \
    wipoutput(stderr, \
      "Requested %s value does not match returned value.\n", what); \
    wipoutput(stderr, "Returned %s is %d.\n", what, (val)); \
  }

/* This macro is used to set variables and warn if they were not set. */
#define SETVAR(what,name,val) \
  if (wipsetvar(what, (double)(val))) \
    wipoutput(stderr, "Trouble saving %s value.\n", name)

void wipcolor(int color)
{
    int narg;

    cpgsci(color);
    cpgqci(&narg);
    CHECK("color index", color, narg);

    if (narg != color)
      wipoutput(stderr,
        "Check color index range (see variables CMIN and CMAX).\n");

    SETVAR("color", "color index", narg);
    return;
}

void wipexpand(double exp)
{
    float arg, expand;

    expand = exp;
    cpgsch(expand);
    cpgqch(&arg);

    if (arg != expand) {
      wipoutput(stderr,
        "Requested expand value does not match returned value.\n");
      wipoutput(stderr, "Returned character expansion is %f.\n", arg);
    }

    SETVAR("expand", "expand", arg);
    return;
}

void wipfill(int fill)
{
    int narg;

    cpgsfs(fill);
    cpgqfs(&narg);
    CHECK("fill style", fill, narg);

    SETVAR("fill", "fill", narg);
    return;
}

void wipfont(int font)
{
    int narg;

    cpgscf(font);
    cpgqcf(&narg);
    CHECK("font type", font, narg);

    SETVAR("font", "font", narg);
    return;
}

void wipltype(int style)
{
    int narg;

    cpgsls(style);
    cpgqls(&narg);
    CHECK("line style", style, narg);

    SETVAR("lstyle", "line style", narg);
    return;
}

void wiplw(int width)
{
    int narg;

    cpgslw(width);
    cpgqlw(&narg);
    CHECK("line width", width, narg);

    SETVAR("lwidth", "line width", narg);
    return;
}

void wipsetbgci(int color)
{
    int narg;

    cpgstbg(color);
    cpgqtbg(&narg);
    CHECK("background color index", color, narg);

    SETVAR("bgci", "background color index", narg);
    return;
}

void wipsetitf(int type)
{
    int narg;

    cpgsitf(type);
    cpgqitf(&narg);
    CHECK("image transfer function", type, narg);

    SETVAR("itf", "image transfer function", narg);
    return;
}

void wipsetangle(double ang)
{
    SETVAR("angle", "angle", ang);
    return;
}

void wipsetslope(double xa, double xb, double ya, double yb)
{
    float xmin, xmax, ymin, ymax;
    double angle, dx, dy;

    cpgqwin(&xmin, &xmax, &ymin, &ymax);
    dx = (xb - xa) / (xmax - xmin);
    dy = (yb - ya) / (ymax - ymin);

    cpgqvp(0, &xmin, &xmax, &ymin, &ymax);
    dx *= (xmax - xmin);
    dy *= (ymax - ymin);

    if ((dx == 0.0) && (dy == 0.0))
      angle = 0.0;
    else
      angle = ATAN2(dy, dx) / RPDEG;

    wipsetangle(angle);
}

void wiplimits(void)
{
    float xmin, xmax, ymin, ymax;

    cpgqwin(&xmin, &xmax, &ymin, &ymax);

    if ((wipsetvar("x1", (double)xmin)) ||
        (wipsetvar("x2", (double)xmax)) ||
        (wipsetvar("y1", (double)ymin)) ||
        (wipsetvar("y2", (double)ymax)))
      wipoutput(stderr, "Trouble saving window limits.\n");

    return;
}

void wipgetlimits(float *x1, float *x2, float *y1, float *y2)
{
    LOGICAL error;

    /* Provide a suitable default in case of error. */
    *x1 = *y1 = 0.0;
    *x2 = *y2 = 1.0;

    wiplimits();
    *x1 = wipgetvar("x1", &error);
    if (error == TRUE) goto MISTAKE;
    *x2 = wipgetvar("x2", &error);
    if (error == TRUE) goto MISTAKE;
    *y1 = wipgetvar("y1", &error);
    if (error == TRUE) goto MISTAKE;
    *y2 = wipgetvar("y2", &error);
    if (error == TRUE) goto MISTAKE;

    return;

MISTAKE:
    wipoutput(stderr, "Trouble getting world coordinate limits.\n");
    return;
}

void wipviewport(void)
{
    float xmin, xmax, ymin, ymax;

    cpgqvp(0, &xmin, &xmax, &ymin, &ymax);

    if ((wipsetvar("vx1", (double)xmin)) ||
        (wipsetvar("vx2", (double)xmax)) ||
        (wipsetvar("vy1", (double)ymin)) ||
        (wipsetvar("vy2", (double)ymax)))
      wipoutput(stderr, "Trouble saving viewport limits.\n");

    return;
}

void wipgetvp(float *vx1, float *vx2, float *vy1, float *vy2)
{
    LOGICAL error;

    /* Provide a suitable default in case of error. */
    *vx1 = *vy1 = 0.2;
    *vx2 = *vy2 = 0.8;

    wipviewport();
    *vx1 = wipgetvar("vx1", &error);
    if (error == TRUE) goto MISTAKE;
    *vx2 = wipgetvar("vx2", &error);
    if (error == TRUE) goto MISTAKE;
    *vy1 = wipgetvar("vy1", &error);
    if (error == TRUE) goto MISTAKE;
    *vy2 = wipgetvar("vy2", &error);
    if (error == TRUE) goto MISTAKE;

    return;

MISTAKE:
    wipoutput(stderr, "Trouble getting viewport limits.\n");
    return;
}

void wipsetr(float tr[])
{
    char transfer[12];
    register int j;

    (void)Strcpy(transfer, "transfer[1]");
    for (j = 0; j < 6; j++) {
      transfer[9] = j + '1';
      if (wipsetvec(transfer, (double)tr[j])) {
        wipoutput(stderr, "Trouble saving the transformation matrix.\n");
        break;
      }
    }

    return;
}

void wipgetr(float tr[])
{
    char transfer[12];
    register int j;
    LOGICAL error;

    /* Provide a suitable default in case of error. */
    for (j = 0; j < 6; j++) tr[j] = 0.0;
    tr[1] = tr[5] = 1.0;

    (void)Strcpy(transfer, "transfer[1]");
    for (j = 0; j < 6; j++) {
      transfer[9] = j + '1';
      tr[j] = wipgetvec(transfer, &error);
      if (error == TRUE) {
        wipoutput(stderr, "Trouble getting the transformation matrix.\n");
        break;
      }
    }

    return;
}

void wipsetsub(int subx1, int subx2, int suby1, int suby2)
{
    if ((wipsetvar("subx1", (double)subx1)) ||
        (wipsetvar("subx2", (double)subx2)) ||
        (wipsetvar("suby1", (double)suby1)) ||
        (wipsetvar("suby2", (double)suby2)))
      wipoutput(stderr, "Trouble saving subimage values.\n");

    return;
}

void wipgetsub(int *subx1, int *subx2, int *suby1, int *suby2)
{
    double value;
    LOGICAL error;

    /* Provide a suitable default in case of error. */
    *subx1 = *suby1 = 1;
    *subx2 = *suby2 = 2;

    value = wipgetvar("subx1", &error);
    if (error == TRUE) goto MISTAKE;
    *subx1 = NINT(value);
    value = wipgetvar("subx2", &error);
    if (error == TRUE) goto MISTAKE;
    *subx2 = NINT(value);
    value = wipgetvar("suby1", &error);
    if (error == TRUE) goto MISTAKE;
    *suby1 = NINT(value);
    value = wipgetvar("suby2", &error);
    if (error == TRUE) goto MISTAKE;
    *suby2 = NINT(value);

    return;

MISTAKE:
    wipoutput(stderr, "Trouble getting subimage values.\n");
    return;
}

void wipsetick(float xtick, int nxsub, float ytick, int nysub)
{
    if ((wipsetvar("xtick", (double)xtick)) ||
        (wipsetvar("ytick", (double)ytick)) ||
        (wipsetvar("nxsub", (double)nxsub)) ||
        (wipsetvar("nysub", (double)nysub)))
      wipoutput(stderr, "Trouble saving tick mark values.\n");

    return;
}

void wipgetick(float *xtick, int *nxsub, float *ytick, int *nysub)
{
    double value;
    LOGICAL error;

    /* Provide a suitable default in case of error. */
    *xtick = *ytick = 0.0;
    *nxsub = *nysub = 0;

    *xtick = wipgetvar("xtick", &error);
    if (error == TRUE) goto MISTAKE;
    *ytick = wipgetvar("ytick", &error);
    if (error == TRUE) goto MISTAKE;
    value = wipgetvar("nxsub", &error);
    if (error == TRUE) goto MISTAKE;
    *nxsub = NINT(value);
    value = wipgetvar("nysub", &error);
    if (error == TRUE) goto MISTAKE;
    *nysub = NINT(value);

    return;

MISTAKE:
    wipoutput(stderr, "Trouble getting tick mark values.\n");
    return;
}

void wipsetsubmar(float subx, float suby)
{
    if ((wipsetvar("xsubmar", (double)subx)) ||
        (wipsetvar("ysubmar", (double)suby)))
      wipoutput(stderr, "Trouble saving sub-margin values.\n");

    return;
}


void wipgetsubmar(float *subx, float *suby)
{
    LOGICAL error;

    /* Provide a suitable default in case of error. */
    *subx = *suby = 2.0;

    *subx = wipgetvar("xsubmar", &error);
    if (error == TRUE) goto MISTAKE;
    *suby = wipgetvar("ysubmar", &error);
    if (error == TRUE) goto MISTAKE;

    return;

MISTAKE:
    wipoutput(stderr, "Trouble getting sub-margin values.\n");
    return;
}

void wipsetcir(int cmin, int cmax)
{
    int nmin, nmax;

    cpgscir(cmin, cmax);
    cpgqcir(&nmin, &nmax);
    if ((cmin != nmin) || (cmax != nmax)) {
      wipoutput(stderr,
        "Requested color index range values do not match returned values.\n");
      wipoutput(stderr, "Returned color index range is [%d-%d].\n", nmin, nmax);
    }

    if ((wipsetvar("cmin", (double)nmin)) ||
        (wipsetvar("cmax", (double)nmax)))
      wipoutput(stderr, "Trouble saving color index range values.\n");

    return;
}

void wipgetcir(int *cmin, int *cmax)
{
    double value;
    LOGICAL error;

    *cmin = 0; /* Provide a suitable default in case of error. */
    *cmax = 1;

    value = wipgetvar("cmin", &error);
    if (error == TRUE) goto MISTAKE;
    *cmin = NINT(value);
    value = wipgetvar("cmax", &error);
    if (error == TRUE) goto MISTAKE;
    *cmax = NINT(value);

    return;

MISTAKE:
    wipoutput(stderr, "Trouble getting color index range values.\n");
    return;
}

int wipDebugMode(void)
{
    int mode;
    double value;
    LOGICAL error;

    /* Provide a suitable default in case of error. */
    mode = 0;

    value = wipgetvar("debugmode", &error);
    if (error != TRUE)
      mode = value + 0.5;

    return(mode);
}
