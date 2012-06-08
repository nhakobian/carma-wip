%module cwip
%{
  #include "wip.h"
%}

/* Code in wip/branch */

extern int wipexecute(const char *cmdname, char *line);
extern int wipprocess(char *cmdline, int *mode, LOGICAL keep);
extern int wipinit(void);

/* Code in wip/images */
extern  void   wipextrema(float **image, int nx, int ny, float *min, \
                          float *max);
extern  void  *wipimage(const char *file, int plane, float blank);
extern  void   wipimagenxy(const void *image, int *nx, int *ny);
extern  void   wipimageminmax(void *image, float *min, float *max, int force);
extern   int   wipimagexists(const void *image);
extern float **wipimagepic(const void *image);
extern   int   wipimlogscale(void *image, float scale);
extern   int   wipimsetminmax(void *image, float min, float max);
extern   int   wipimgethead(const void *image, int axis, double *crval, \
			    double *crpix, double *cdelt, char *ctype);
extern   int   wipimctype(const void *image, int axis, char *ctype);
extern  char  *wipimtype(const void *image);
extern   int   wipimplane(const void *image);
extern   int   wipimhdprsnt(const void *image, const char *hdname);
extern   int   wipimhdval(const void *image, const char *hdname, \
			  double *retval);
extern   int   wipimhdstr(const void *image, const char *hdname, char *retval,\
			  size_t maxlen);
extern  void  *wipimcur(const char *imagename);
extern  void   wipimsetcur(const char *imagename, const void *image);
extern  void   wipfreeimage(const char *imagename);
extern   int   wipheader(int blcx, int blcy, int trcx, int trcy, \
			 const char *xtype, const char *ytype);
extern   int   wipsmooth(float **array, int nx, int ny, int order, \
			 float blank);

/* Code in wip/interact */
extern COMMAND *create_command(void);
extern    void  add_command(COMMAND *cmd);
extern    void  delete_command(COMMAND *cmd);
extern    void  wipdecode(const char *string, char *outstr, size_t maxout);
extern     int  wiphelp(char *rest);
extern COMMAND *wipifxecute(char **rest);
extern    void  wipsaveline(COMMAND *macro, const char *line);
extern COMMAND *wipstartins(char *rest);
extern    void  wipinsert(COMMAND *command, const char *line);
extern     int  wipdelete(char *rest);
extern COMMAND *wipstartmac(const char *macname);
extern COMMAND *find_command(COMMAND *start, const char *cmdname, int exact);
extern COMMAND *wipinterpret(char **cmdline);
extern     int  wiplist(int line1, int line2, const char *rest);
extern COMMAND *wiploopxecute(char **cmdline, int *ncount);
extern COMMAND *create_macro(const char *macname);
extern    void  add_to_macro(COMMAND *mac, const char *cmdline);
extern    void  insert_macro(COMMAND *mac, const char *cmdline, int before);
extern    void  delete_macro(COMMAND *mac, int first, int last);
extern     int  wipmaxecute(COMMAND *mac, int cnt, const char *rest);
extern    char *wipparse(char **line);
extern     int  wipcountwords(const char *line);
extern    void  wiplower(char *line);
extern    void  wipupper(char *line);
extern    char *wipleading(const char *line);
extern     int  wiplenc(char *line);
extern    char *wipnewstring(const char *string);
extern     int  wiparguments(char **rest, int numarg, double arg[]);
extern     int  wipreadinput(const char *rest);
extern     int  wipwritemac(const char *file, const char *macs);
extern     int  wipplayback(const char *rest);
extern     int  wipreadmac(const char *rest);
extern     int  wipmacroinput(const char *file);

/* Code in wip/fit */
extern    void  wipplotfit(float x1, float x2, float step, float x[], int nx);
extern    void  wipfitrange(float x1, float x2, float y1, float y2);
extern     int  wipfit(const char *rest, int nxy, float x[], float y[], \
		       int ns, float sig[]);
extern     int  wipgaussfit(char *rest, float x[], float y[], int nxy, \
			    float sig[], int nsig, int ngauss, float terms[]);
extern     int  lsqfit(float x[], float y[], int ndata, float sig[], int mwt, \
		       float *a, float *b, float *siga, float *sigb, \
		       float *chi2, float *q);
extern     int  medfit(float x[], float y[], int ndata, float *a, float *b, \
		       float *abdev);

/* Code in wip/plot */
extern    void   wipaitoff( int nxy, float x[], float y[]);
extern    void   wipaitoffgrid( int nlong, int nlats);
extern     int   wiparc(float majx, float majy, float arcangle, float angle, \
			float start);
extern     int   wipbeam(float major, float minor, float posangle, float offx,\
			 float offy, int fillcolor, float scale, int bgrect);
extern    void   wiparrow(float xp, float yp, float angle, float vent);
extern    void   wipvfield(float x[], float y[], float r[], float phi[], \
			   int npts, float angle, float vent);
extern    void   wiplogarithm(float array[], int nxy, float scale);
extern    void   wiprange(int nx, float x[], float *xmin, float *xmax);
extern     int   wiperrorbar(int locat, float x[], float y[], float err[], \
			     int nxy);
extern    void   wipcursor(float *cx, float *cy, LOGICAL keep);
extern    void   wipfixcurs(const char *cmd, char *rest, LOGICAL keep);
extern     int   wipdevice(const char *devicename);
extern    void   wipclose(void);
extern    void   wipheq(int nx, int ny, float **image, int x1, int x2, int y1,\
			int y2, float blank, float min, float max, int nbins);
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
extern    void   wippalette(int which, int levels);
extern    void   wippanel(int nx, int ny, int k);
extern     int   wipphard(const char *device, const char *rest);
extern     int   wippoints(int nstyle, float style[], int nxy, float x[], \
			   float y[], int nc, float c[]);
extern    void   wipputlabel(const char *line, double justify);
extern    char  *fixputlabel(const char *cmdname, char *rest, LOGICAL save);
extern     int   wipmtext(char *side, float disp, float coord, float just, \
			  char *line);
extern     int   wipquarter(int quadrant);
extern    void   wipreset(void);
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
extern    void   wipshow(const char *rest);
extern    char  *wipfpfmt(float arg, int nsig);
extern    char  *wipifmt(float arg);
extern     int   wipwedge(char *side, float disp, float thick, float bg, \
			  float fg, char *label);

/* Code in wip/sysdep */
extern long int  filesize(FILE *fp);
extern     void  wipsetQuiet(int quiet);
extern     void  wipbegin(int disable, int justread);
extern     void  wipexit(int status);
#ifndef NOVARARGS
  extern     void   wipoutput(FILE *fp, const char *fmt, ...);
#else
  #define wipoutput (void)fprintf
#endif /* !NOVARARGS */
extern      int  wipinput(FILE *fp, const char *prompt, char *line, \
			  size_t maxsize);
extern    float  wiprand(long int *seed);
extern    float  wipgaussdev(long int *seed);
extern     void  wiplines(int first, int last);
extern     void  wipgetlines(int *first, int *last);
extern      int  wipopenfile(const char *file);
extern      int  wipreadcol(float array[], int maxsize, int ncol);
extern     char *wipreadstr(int first, int second);
extern      int  wipspool(const char *spoolfile);
extern      int  wipcommand(const char *command);

/* Code in wip/variables */
extern    int  wipisnumber(const char *inword, double *retval);
extern   void  wipecho(const char *input);
extern    int  wipsetuser(const char *input);
extern   char *wipgettoken(char *out, const char *in, char **next);
extern    int  wiptokenexists(const char *inword);
extern double  wipevaluate(const char *inword, LOGICAL *error);
extern   char *wipbracextract(const char *inword, char **left);
extern    int  wipnewitem(const char *string);
extern    int  wipfreeitem(const char *string);
extern    int  wipisuserfunc(const char *name);
extern double  wipuserfunc(const char *inword, double arg, LOGICAL *error);
extern   void  clear_stack(void);
extern    int  push_stack(double value);
extern    int  pop_stack(double *value);
extern    int  wipisstring(const char *name);
extern   char *wipgetstring(const char *name);
extern    int  wipsetstring(const char *name, const char *value);
extern    int  wipNewStrVar(const char *name);
extern    int  wipFreeString(const char *name);
extern    int  wipisvar(const char *name);
extern double  wipgetvar(const char *name, LOGICAL *error);
extern    int  wipsetvar(const char *name, double value);
extern    int  wipNewVariable(const char *name);
extern    int  wipFreeVariable(const char *name);
extern    int  wipisvec(const char *name);
extern double  wipgetvec(const char *name, LOGICAL *error);
extern    int  wipsetvec(const char *name, double value);
extern  float *wipvector(const char *name, int *maxsize, int *currentSize);
extern    int  wipvectornpts(const char *name, int currentSize);
extern    int  wipisvecfunc(const char *inword);
extern double  wipvecfunc(const char *inword, const char *arg, LOGICAL *error);
extern    int  wipvectorinit(const char *name, int npts, \
			     const char *expression);
extern    int  wipNewVector(const char *name, int size);
extern    int  wipFreeVector(const char *name);

