/*
 *    <image.c>
 *
 *  History:
 *    13aug90 jm  Original code.
 *    01dec90 jm  Heavily Modified
 *    25oct91 jm  Completely overhauled.  The intent now is to take
 *                the structure that is returned from the image routines
 *                and use it as an opaque pointer to all subsequent image
 *                routines.  Keep all important parameters of the image
 *                around until a new image is called for.  At that time
 *                release the real data as well.  Currently, only one
 *                image is present at a time.
 *    26feb92 jm  Added wipimplane routine.
 *    02mar92 jm  Modified wipimage/getimage routines to permit user
 *                to specify what value bad pixels should be set to.
 *    31jul92 jm  Did some cleaning and added wipnewstring().  Also,
 *                added wipfreeimage() and made wipimagefree() static.
 *                Fixed a pointer bug in wipimsetcur() by adding last.
 *    15aug92 jm  Modified wipimsetminmax() to return status int.
 *    27may93 jm  Corrected malloc statement for pixels.  It was
 *                allocating for (float **) instead of for (FLOAT *).
 *    28jul93 jm  Added wipimlogscale() function and added force
 *                option to wipimageminmax().
 *    10nov93 jm  Modified declarations to usage of void.
 *    17aug94 jm  Modified getimage to notify user if requested plane
 *                number is not in the range [1,NZ] and what plane will
 *                be used instead.
 *    28oct96 jm  Modified wipimage to reset subimage range and to set
 *                the local crval, etc. headers.
 *    13nov96 jm  Modified wipimage so ctype was declared as large as
 *                in the WIPIMAGE structure.  There was a problem with
 *                memory overwrite for some images.
 *    18may99 pjt simple support for cd1_1 cd2_2 instead of cdelt1/2
 *    10oct00 pjt no more PROTOTYPE
 *    
 *
 * Routines:
 * static void wipimagefree(void *image);
 * static WIPIMAGE *getimage(const char *file, int plane, float blank);
 * void *wipimage(const char *file, int plane, float blank);
 * void wipimagenxy(const void *image, int *nx, int *ny);
 * int wipimagexists(const void *image);
 * int wipimgethead(const void *image, int axis, double *crval,
 *   double *crpix, double *cdelt, char *ctype);
 */

#define WIP_IMAGE
#define WIP_DRIVERS
#include "wip.h"

/* Global Variables needed just for this file */

/* Define a structure in which to store image data. */
/* MAXNAX and FLOAT are defined in image.h */
typedef struct {
    char   *name;                /* The input file name of this image. */
    void   *fmt;          /* Opaque handle of different image drivers. */
    void   *handle;    /* Opaque handle used in low level image calls. */
    char    imtype[80];       /* String describing name of image type. */
    int     plane;                /* (In range) selected plane number. */
    int     nx;                  /* Number of pixels along the X axis. */
    int     ny;                  /* Number of pixels along the Y axis. */
    int     nz;                  /* Number of pixels along the Z axis. */
    float   min;                           /* Minimum of chosen plane. */
    float   max;                           /* Maximum of chosen plane. */
    double  crval[MAXNAX];                    /* Value at CRPIX pixel. */
    double  crpix[MAXNAX];         /* Reference pixel along each axis. */
    double  cdelt[MAXNAX];   /* Step size (CRVAL units) for each axis. */
    char    ctype[MAXNAX][80];           /* String defining axis type. */
    float  *ptrows;                             /* Private work array. */
    FLOAT **pixels;                                /* Real data array. */
} WIPIMAGE;

typedef struct image_stack {
  char *name;                              /* (Lower case) stack name. */
  void *image;                     /* (WIPIMAGE *) cast into (char *). */
  struct image_stack *next;
} IMSTACK;
static IMSTACK imstackHead = {"curimage", (void *)NULL, (IMSTACK *)NULL};

/* Code */

static void wipimagefree(void *image)
{
    IMFORMAT *fmt;
    WIPIMAGE *ptr;

    if (image != (void *)NULL) {
      ptr = (WIPIMAGE *)image;
      if (ptr->pixels != (FLOAT **)NULL) Free(ptr->pixels);
      if (ptr->ptrows != (float *)NULL) freevector(ptr->ptrows);
      if (ptr->name != (char *)NULL) Free(ptr->name);
      if (ptr->fmt != (void *)NULL) {
        fmt = (IMFORMAT *)ptr->fmt;
        fmt->imclose(ptr->handle);
      }
      Free(ptr);
    }
}

/*
 *  Fill the real array pixels[ny][nx] and the structure image.
 *  Returns a pointer to the structure if successful; NULL on error.
 */
static WIPIMAGE *getimage(const char *filename, int plane, float blank)
{

    void *handle;         /* Opaque handle returned from open routine. */
    char ctype1[80], ctype2[80];
    register int j, number;
    int indx;
    int nsize[MAXNAX];
    float fmin, fmax;
    float *rptr, *fptr;
    FLOAT **pixels;
    double crval1, crval2, crpix1, crpix2, cdelt1, cdelt2, tmpd;
    WIPIMAGE *image;
    IMFORMAT *fmt;

    number = sizeof(Format_Table) / sizeof(Format_Table[0]);

    for (j = 0; j < number; j++) {
      fmt = &Format_Table[j];
      if ((fmt != (IMFORMAT *)NULL) && (fmt->imopen != NULL)) {
        if ((handle = fmt->imopen(filename, MAXNAX, nsize)) != (void *)NULL)
          break;
      }
    }

    if ((j >= number) || (fmt->imopen == NULL))
      return((WIPIMAGE *)NULL);

    if ((image = (WIPIMAGE *)Malloc(sizeof(WIPIMAGE))) == (WIPIMAGE *)NULL) {
      wipoutput(stderr, "GETIMAGE: No memory to store image information.\n");
      if (fmt->imclose != NULL) fmt->imclose(handle);
      return((WIPIMAGE *)NULL);
    }

    if ((fmt->imrdhdd == NULL) || (fmt->imrdhdr == NULL) ||
        (fmt->imrdhdi == NULL) || (fmt->imrdhda == NULL)) {
      wipoutput(stderr, "GETIMAGE: No header access functions!\n");
      wipimagefree((void *)image);
      return((WIPIMAGE *)NULL);
    }

    fmt->imrdhdr(handle, "datamin",   &fmin, 0.0);
    fmt->imrdhdr(handle, "datamax",   &fmax, 0.0);
    fmt->imrdhdd(handle,  "crval1", &crval1, 0.0);
    fmt->imrdhdd(handle,  "crval2", &crval2, 0.0);
    fmt->imrdhdd(handle,  "crpix1", &crpix1, 0.0);
    fmt->imrdhdd(handle,  "crpix2", &crpix2, 0.0);
    fmt->imrdhdd(handle,  "cdelt1", &cdelt1, 0.0);
    fmt->imrdhdd(handle,  "cdelt2", &cdelt2, 0.0);
    if (cdelt1 == 0.0) {
      fmt->imrdhdd(handle,  "cd1_1", &cdelt1, 0.0);
      fmt->imrdhdd(handle,  "cd1_2", &tmpd, 0.0);
      if (tmpd != 0.0) 
	wipoutput(stderr, "GETIMAGE: cd1_2 = %g non-zero ...\n", tmpd);
    }
    if (cdelt2 == 0.0) {
      fmt->imrdhdd(handle,  "cd2_2", &cdelt2, 0.0);
      fmt->imrdhdd(handle,  "cd2_1", &tmpd, 0.0);
      if (tmpd != 0.0) 
	wipoutput(stderr, "GETIMAGE: cd2_1 = %g non-zero ...\n", tmpd);
    }
    fmt->imrdhda(handle,  "ctype1",  ctype1, "(none)", 80);
    fmt->imrdhda(handle,  "ctype2",  ctype2, "(none)", 80);

    image->fmt = (void *)fmt;
    image->handle = handle;

    if ((image->name = (char *)Malloc(Strlen(filename) + 1)) != (char *)NULL)
      (void)Strcpy(image->name, filename);

    (void)Strcpy(image->imtype, fmt->imtype);
    image->nx = nsize[0];
    image->ny = nsize[1];
    image->nz = nsize[2];
    image->min = fmin;
    image->max = fmax;
    image->crval[0] = crval1;
    image->crval[1] = crval2;
    image->crpix[0] = crpix1;
    image->crpix[1] = crpix2;
    image->cdelt[0] = cdelt1;
    image->cdelt[1] = cdelt2;
    (void)Strncpy(image->ctype[0], ctype1, 80);
    image->ctype[0][79] = Null; /* Force a Null at the end of the string. */
    (void)Strncpy(image->ctype[1], ctype2, 80);
    image->ctype[1][79] = Null; /* Force a Null at the end of the string. */

    image->ptrows = fptr = vector(image->nx * image->ny);
    image->pixels = pixels = (FLOAT **)Malloc(image->ny * sizeof(FLOAT *));
    if ((fptr == (float *)NULL) || (pixels == (FLOAT **)NULL)) {
      wipoutput(stderr,
        "GETIMAGE: Not enough internal storage room for the image.\n");
      wipimagefree((void *)image);
      return((WIPIMAGE *)NULL);
    }

    indx = MAX(MIN(plane, image->nz), 1);
    if (indx != plane) {
      wipoutput(stderr, "GETIMAGE: Plane %d is out of range...\n", plane);
      wipoutput(stderr, "GETIMAGE: Will look for plane #%d.\n", indx);
    }
    if (fmt->imsetpl(handle, 1, &indx)) {
      wipoutput(stderr, "GETIMAGE: Trouble setting plane %d...\n", indx);
      wipoutput(stderr, "GETIMAGE: Trying plane #1.\n");
      indx = 1;
      if (fmt->imsetpl(handle, 1, &indx)) {
        wipoutput(stderr, "GETIMAGE: Trouble setting plane %d...\n", indx);
        wipoutput(stderr, "GETIMAGE: Something really wrong here!\n");
        wipimagefree((void *)image);
        return((WIPIMAGE *)NULL);
      }
    }
    image->plane = indx;

    for (indx = 0; indx < image->ny; indx++) {
      rptr = fptr + (indx * image->nx);
      if (fmt->imread(handle, indx, rptr, blank)) {
        wipoutput(stderr, "GETIMAGE: Trouble reading image row %d.n", indx+1);
        wipimagefree((void *)image);
        return((WIPIMAGE *)NULL);
      }
      pixels[indx] = (FLOAT *)rptr;
    }

    return(image);
}

void *wipimage(const char *filename, int plane, float blank)
{
    char dummy[80];
    int nx, ny;
    double arg[3];
    WIPIMAGE *ptr;

    ptr = getimage(filename, plane, blank);
    if (wipimagexists((void *)ptr) == 0) {
      wipoutput(stderr, "Image %s could not be loaded.\n", filename);
      wipimagefree((void *)ptr);
      return((void *)NULL);
    }

    wipimagenxy((void *)ptr, &nx, &ny);
    wipoutput(stdout, "Image size: %d by %d.\n", nx, ny);

    wipsetsub(1, nx, 1, ny);
    if (wipimgethead((void *)ptr, 0, &arg[0], &arg[1], &arg[2], dummy) == 0) {
      (void)wipsetvar("crvalx", arg[0]);
      (void)wipsetvar("crpixx", arg[1]);
      (void)wipsetvar("cdeltx", arg[2]);
    }
    if (wipimgethead((void *)ptr, 1, &arg[0], &arg[1], &arg[2], dummy) == 0) {
      (void)wipsetvar("crvaly", arg[0]);
      (void)wipsetvar("crpixy", arg[1]);
      (void)wipsetvar("cdelty", arg[2]);
    }

    return((void *)ptr);
}


void wipimagenxy(const void *image, int *nx, int *ny)
{
    WIPIMAGE *ptr;

    if (wipimagexists(image) == 0) {
      wipoutput(stderr, "You must specify an image first!\n");
      return;
    }

    ptr = (WIPIMAGE *)image;
    *nx = ptr->nx;
    *ny = ptr->ny;
    return;
}

/*  Returns 1 if the named image exists and has data; 0 otherwise. */
int wipimagexists(const void *image)
{
    int doesItExist;
    WIPIMAGE *ptr;

    ptr = (WIPIMAGE *)image;
    doesItExist = (ptr != (WIPIMAGE *)NULL) &&
                  (ptr->pixels != (FLOAT **)NULL) &&
                  (ptr->ptrows != (float *)NULL);

    return(doesItExist);
}

/*
 *  Returns 1 if "image" is not a defined image item or the axis input
 *  is out of range; 0 if no error (successful).
 *
 *  Note: ctype must be declared as large as the structure element!
 *  No test of this is done.
 */
int wipimgethead(const void *image, int axis, double *crval, double *crpix, double *cdelt, char *ctype)
{
    WIPIMAGE *ptr;

    if (wipimagexists(image) == 0) {
      wipoutput(stderr, "You must specify an image first!\n");
      return(1);
    }

    if ((axis < 0) || (axis >= MAXNAX)) {
      wipoutput(stderr, "Axis number specified is out of range!\n");
      return(1);
    }

    ptr = (WIPIMAGE *)image;
    *crval = ptr->crval[axis];
    *crpix = ptr->crpix[axis];
    *cdelt = ptr->cdelt[axis];
    (void)Strcpy(ctype, ptr->ctype[axis]);
    return(0);
}
