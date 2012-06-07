/*
 *	<drivers.h> --- Image include file.
 *	26oct91 jm  Original code.
 *	10nov93 jm  Modified declarations to usage of void.
 *
 */

/* FLOAT - imageP.h */
extern void *miropen(const char *name, int naxis, int axes[]);
extern void  mirclose(void *op);
extern  int  mirread(void *op, int indx, FLOAT *array, FLOAT badpixel);
extern  int  mirsetpl(void *op, int naxis, int axes[]);
extern void  mirrdhdd(void *op, const char *key,double *val,double def);
extern void  mirrdhdr(void *op, const char *key, FLOAT *val,FLOAT rdef);
extern void  mirrdhdi(void *op, const char *key, int *val, int defval);
extern void  mirrdhda(void *op, const char *key, char *val, \
		      const char *defval, size_t maxlen);
extern  int  mirhdprsnt(void *op, const char *key);
extern void *fitopen(const char *name, int naxis, int axes[]);
extern void  fitclose(void *op);
extern  int  fitread(void *op, int indx, FLOAT *data, FLOAT badpixel);
extern  int  fitsetpl(void *op, int naxis, int axes[]);
extern void  fitrdhdd(void *op, const char *key,double *val,double def);
extern void  fitrdhdr(void *op, const char *key, FLOAT *val,FLOAT rdef);
extern void  fitrdhdi(void *op, const char *key, int *val, int defval);
extern void  fitrdhda(void *op, const char *key, char *val, \
		      const char *defval, size_t maxlen);
extern  int  fithdprsnt(void *op, const char *key);
extern void *basopen(const char *name, int naxis, int axes[]);
extern void  basclose(void *op);
extern  int  basread(void *op, int indx, FLOAT *array, FLOAT badpixel);
extern  int  bassetpl(void *op, int naxis, int axes[]);
extern void  basrdhdd(void *op, const char *key,double *val,double def);
extern void  basrdhdr(void *op, const char *key, FLOAT *val,FLOAT rdef);
extern void  basrdhdi(void *op, const char *key, int *val, int defval);
extern void  basrdhda(void *op, const char *key, char *val, \
		      const char *defval, size_t maxlen);
extern  int  bashdprsnt(void *op, const char *key);

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
    void *(*imopen)  (const char *name, int naxis, int axes[]);
    void  (*imclose) (void *op);
     int  (*imread)  (void *op, int indx, FLOAT *array, FLOAT badpixel);
     int  (*imsetpl) (void *op, int naxis, int axes[]);
    void  (*imrdhdd) (void *op, const char *key, double *val, double defval);
    void  (*imrdhdr) (void *op,const char *key,FLOAT *val,FLOAT defval);
    void  (*imrdhdi) (void *op, const char *key, int *val, int defval);
    void  (*imrdhda) (void *op, const char *key, char *val, \
		      const char *defval, size_t maxlen);
     int  (*imhdprsnt) (void *op, const char *key);
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
