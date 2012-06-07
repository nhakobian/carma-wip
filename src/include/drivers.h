/*
 *	<drivers.h> --- Image include file.
 *	26oct91 jm  Original code.
 *	10nov93 jm  Modified declarations to usage of void.
 *
 */

/* ARGS(alist), FLOAT, and void are defined in imageP.h */

extern void *miropen ARGS(( Const char *name, int naxis, int axes[] ));
extern void mirclose ARGS(( void *op ));
extern int mirread ARGS(( void *op, int indx, FLOAT *array, FLOAT badpixel ));
extern int mirsetpl ARGS(( void *op, int naxis, int axes[] ));
extern void mirrdhdd ARGS(( void *op, Const char *key,double *val,double def ));
extern void mirrdhdr ARGS(( void *op, Const char *key, FLOAT *val,FLOAT rdef ));
extern void mirrdhdi ARGS(( void *op, Const char *key, int *val, int defval ));
extern void mirrdhda ARGS(( void *op, Const char *key, char *val, Const char *defval, size_t maxlen ));
extern int mirhdprsnt ARGS(( void *op, Const char *key ));

extern void *fitopen ARGS(( Const char *name, int naxis, int axes[] ));
extern void fitclose ARGS(( void *op ));
extern int fitread ARGS(( void *op, int indx, FLOAT *data, FLOAT badpixel ));
extern int fitsetpl ARGS(( void *op, int naxis, int axes[] ));
extern void fitrdhdd ARGS(( void *op, Const char *key,double *val,double def ));
extern void fitrdhdr ARGS(( void *op, Const char *key, FLOAT *val,FLOAT rdef ));
extern void fitrdhdi ARGS(( void *op, Const char *key, int *val, int defval ));
extern void fitrdhda ARGS(( void *op, Const char *key, char *val, Const char *defval, size_t maxlen ));
extern int fithdprsnt ARGS(( void *op, Const char *key ));

extern void *basopen ARGS(( Const char *name, int naxis, int axes[] ));
extern void basclose ARGS(( void *op ));
extern int basread ARGS(( void *op, int indx, FLOAT *array, FLOAT badpixel ));
extern int bassetpl ARGS(( void *op, int naxis, int axes[] ));
extern void basrdhdd ARGS(( void *op, Const char *key,double *val,double def ));
extern void basrdhdr ARGS(( void *op, Const char *key, FLOAT *val,FLOAT rdef ));
extern void basrdhdi ARGS(( void *op, Const char *key, int *val, int defval ));
extern void basrdhda ARGS(( void *op, Const char *key, char *val, Const char *defval, size_t maxlen ));
extern int bashdprsnt ARGS(( void *op, Const char *key ));

#ifdef WIP_DRIVERS
#undef WIP_DRIVERS

/*
 *  Structure in which to store image reading commands.  Contains:
 *  imtype    : What kind of file is this.
 *  imopen    : Test and open routine.
 *  imclose   : Close the image file.
 *  imread    : Read selected plane.
 *  imsetpl   : Select plane number.
 *  imrdhdd   : Get double precision header item.
 *  imrdhdr   : Read a real header item.
 *  imrdhdi   : Get an integer header.
 *  imrdhda   : Read a character (string) header item.
 *  imhdprsnt : Returns 1 if the header is present; 0 otherwise.
 */
typedef struct {
    char   *imtype;
    void *(*imopen)  ARGS(( Const char *name, int naxis, int axes[] ));
    void  (*imclose) ARGS(( void *op ));
     int  (*imread)  ARGS(( void *op, int indx, FLOAT *array, FLOAT badpixel ));
     int  (*imsetpl) ARGS(( void *op, int naxis, int axes[] ));
    void  (*imrdhdd) ARGS(( void *op, Const char *key, double *val, double defval ));
    void  (*imrdhdr) ARGS(( void *op,Const char *key,FLOAT *val,FLOAT defval ));
    void  (*imrdhdi) ARGS(( void *op, Const char *key, int *val, int defval ));
    void  (*imrdhda) ARGS(( void *op, Const char *key, char *val, Const char *defval, size_t maxlen ));
     int  (*imhdprsnt) ARGS(( void *op, Const char *key ));
} IMFORMAT;

static IMFORMAT Format_Table[] = {
  {"miriad", miropen, mirclose, mirread, mirsetpl,
             mirrdhdd, mirrdhdr, mirrdhdi, mirrdhda, mirhdprsnt},
  {  "fits", fitopen, fitclose, fitread, fitsetpl,
             fitrdhdd, fitrdhdr, fitrdhdi, fitrdhda, fithdprsnt},
  { "basic", basopen, basclose, basread, bassetpl,
             basrdhdd, basrdhdr, basrdhdi, basrdhda, bashdprsnt},
};

#else

typedef char IMFORMAT;

#endif /* WIP_DRIVERS */
