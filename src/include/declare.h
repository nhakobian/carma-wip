/*
	<declare.h>
	15jun91 jm  Original code.
	02nov91 jm  Added variables subdirectory and removed files
		    plot/variables and sysdep.../fillinit.
	01aug92 jm  Cleaned up and fixed entries due to changes in /variables.
	04oct95 jm  Added if-else for wipoutput declaration.
	13nov96 jm  Added wipDebugMode and wipsetQuiet.
	21jan98 jm  VMS reserves the readonly keyword, so it was changed
		    to justread in declaration of wipbegin().
*/

#ifndef WIP_DECLARE
#define WIP_DECLARE

/* Code in wip/images */
extern  void  *wipimage(const char *file, int plane, float blank);
extern  void   wipimagenxy(const void *image, int *nx, int *ny);
extern   int   wipimagexists(const void *image);
extern   int   wipimgethead(const void *image, int axis, double *crval, \
			    double *crpix, double *cdelt, char *ctype);

/*parse */
char *wipparse(char **line);
int  wipcountwords(const char *line);
void  wiplower(char *s);
void  wipupper(char *s);
char *wipleading(const char *line);
int  wiplenc(char *c);
char *wipnewstring(const char *string);


/* Code in wip/plot */
extern    void   wipaitoff( int nxy, float x[], float y[]);
extern    void   wipaitoffgrid( int nlong, int nlats);
extern    void   wiplogarithm(float array[], int nxy, float scale);
extern    void   wiprange(int nx, float x[], float *xmin, float *xmax);
extern     int   wiperrorbar(int locat, float x[], float y[], float err[], \
			     int nxy);
extern     int   wiphline(int npts, float x[], float y[], float gap, \
			  int center);
extern     int   wipbar(int npts, float x[], float y[], int nc, float color[],\
			int location, int dolimit, float barlimit, \
			float barwidth);
extern   float   wipimval(float **image, int nx, int ny, float cx, float cy, \
			  float tr[], LOGICAL *error);
extern    char  *wipradecfmt(float position);
extern    char  *wipinquire(const char *item);
extern     int   wipishard(void);
extern     int   wiplevels(char *rest, float level[], int maxlev);
extern     int   wipautolevs(char *rest, float level[], int maxlev, float min,\
			     float max);
extern     int   wipscalevels(const char *stype, float slev, float pmin, \
			      float pmax, float levels[], int nlev);
extern   float  *vector(int nx);
extern   float **matrix(int offx, int nx, int offy, int ny);
extern    void   freevector(float *vector);
extern    void   freematrix(float **matrix, int offx, int offy);
extern    void   wipmove(float x, float y);
extern    void   wipdraw(float x, float y);
extern    void   wipgetcxy(float *cx, float *cy);
extern    void   wippanel(int nx, int ny, int k);
extern     int   wipscale(float scalex, float scaley, int k);
extern    void   wipcolor(int color);
extern    void   wipexpand(double expand);
extern    void   wipfill(int fill);
extern    void   wipfont(int font);
extern    void   wipltype(int style);
extern    void   wiplw(int width);
extern    void   wipsetbgci(int color);
extern    void   wipsetitf(int type);
extern    void   wipsetangle(double angle);
extern    void   wipsetslope(double xa, double xb, double ya, double yb);
extern    void   wiplimits(void);
extern    void   wipgetlimits(float *x1, float *x2, float *y1, float *y2);
extern    void   wipviewport(void);
extern    void   wipgetvp(float *x1, float *x2, float *y1, float *y2);
extern    void   wipsetr(float tr[]);
extern    void   wipgetr(float tr[]);
extern    void   wipsetsub(int subx1, int subx2, int suby1, int suby2);
extern    void   wipgetsub(int *subx1, int *subx2, int *suby1, int *suby2);
extern    void   wipsetick(float xtick, int nxsub, float ytick, int nysub);
extern    void   wipgetick(float *xtick, int *nxsub, float *ytick, int *nysub);
extern    void   wipsetsubmar(float subx, float suby);
extern    void   wipgetsubmar(float *subx, float *suby);
extern    void   wipsetcir(int cmin, int cmax);
extern    void   wipgetcir(int *cmin, int *cmax);
extern     int   wipDebugMode(void);
extern    char  *wipfpfmt(float arg, int nsig);
extern    char  *wipifmt(float arg);
extern     int   wipwedge(char *side, float disp, float thick, float bg, \
			  float fg, char *label);

/* Code in wip/sysdep */
extern long int  filesize(FILE *fp);
#ifndef NOVARARGS
  extern     void   wipoutput(FILE *fp, const char *fmt, ...);
#else
  #define wipoutput (void)fprintf
#endif /* !NOVARARGS */

/* Code in wip/variables */
extern   char *wipbracextract(const char *inword, char **left);
extern double  wipgetvar(const char *name, LOGICAL *error);
extern    int  wipsetvar(const char *name, double value);
extern double  wipgetvec(const char *name, LOGICAL *error);
extern    int  wipsetvec(const char *name, double value);

#endif /* WIP_DECLARE */
