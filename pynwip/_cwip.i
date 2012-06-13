%{
  #define SWIG_FILE_WITH_INIT
  #include "wip.h"
%}

%module cwip

%include "typemaps.i"
%include "numpy.i"
%feature("autodoc", "2");

%init %{
import_array();
%}

/* cpgplot defs */
void cpgtbox(const char *xopt, float xtick, int nxsub, \
	     const char *yopt, float ytick, int nysub);  // Draw box
void cpgpage(void);  // Erase screen.
void cpgswin(float x1, float x2, float y1, float y2); // Set plot limits.
//   Writes labels, similar to mtext.
void cpglab(const char *xlbl, const char *ylbl, const char *toplbl); 
void cpgpap(float width, float aspect); // Sets papersize, aspect.
void cpgwnad(float x1, float x2, float y1, float y2); // Set equal aspect.
void cpgsvp(float x1, float x2, float y1, float y2); // Set viewport.
void cpgshs(float angle, float sepn, float phase); // set hatch style
void cpgrect(float x1, float x2, float y1, float y2); // draw rectangle.

// CPGPOLY Wrapper Begin
// void cpgpoly(int n, const float *xpts, const float *ypts);
%apply (int DIM1, float* IN_ARRAY1) { (int len1, float* vec1),
                                      (int len2, float* vec2)}
%rename (cpgpoly) mod_cpgpoly;
%exception mod_cpgpoly {
  $action
    if (PyErr_Occurred()) SWIG_fail;
}
%inline %{
void mod_cpgpoly(int len1, float* vec1, int len2, float* vec2)
{
  if (len1 != len2) {
    PyErr_Format(PyExc_ValueError, "Arrays of lengths (%d,%d) given", len1,
		 len2);
    return;
  }
  cpgpoly(len1, vec1, vec2);
  return;
}
%}
%clear (int len1, float* vec1), (int len2, float* vec2);
// CPGPOLY Wrapper End

/* CPGHI2D Wrapper Begin
// void cpghi2d(const float *data, int nxv, int nyv, int ix1, int ix2, \
//              int iy1, int iy2, const float *x, int ioff, float bias, \
//              Logical center, float *ylims);
   Arguments:
   DATA   (input)  : the data array to be plotted.
   NXV    (input)  : the first dimension of DATA.
   NYV    (input)  : the second dimension of DATA.
   IX1    (input)
   IX2    (input)
   IY1    (input)
   IY2    (input)  : PGHI2D plots a subset of the input array DATA.
                     This subset is delimited in the first (x)
		     dimension by IX1 and IX2 and the 2nd (y) by IY1
		     and IY2, inclusively. Note: IY2 < IY1 is
		     permitted, resulting in a plot with the
		     cross-sections plotted in reverse Y order.
		     However, IX2 must be => IX1.
   X      (input)  : the abscissae of the bins to be plotted. That is,
                     X(1) should be the X value for DATA(IX1,IY1), and
		     X should have (IX2-IX1+1) elements.  The program
		     has to assume that the X value for DATA(x,y) is
		     the same for all y.
   IOFF   (input)  : an offset in array elements applied to successive
                     cross-sections to produce a slanted effect.  A
		     plot with IOFF > 0 slants to the right, one with
		     IOFF < 0 slants left.
   BIAS   (input)  : a bias value applied to each successive cross-
                     section in order to raise it above the previous
		     cross-section.  This is in the same units as the
		     data.
   CENTER (input)  : if .true., the X values denote the center of the
                     bins; if .false. the X values denote the lower
		     edges (in X) of the bins.
   YLIMS  (input)  : workspace.  Should be an array of at least
                     (IX2-IX1+1) elements.
*/
%apply (float* IN_ARRAY2, int DIM1, int DIM2) {(float *data, int nx, int ny)}
%apply (int DIM1, float* IN_ARRAY1) {(int xsize, float *x),
                                     (int ysize, float *ylims)}
%rename (cpghi2d) mod_cpghi2d;
%exception mod_cpghi2d {
  $action
  if (PyErr_Occurred()) SWIG_fail;
}
%inline %{
void mod_cpghi2d(float *data, int nx, int ny, int ix1, int ix2, int iy1, \
		 int iy2, int xsize, float *x, int ioff, float bias, \
		 int center, int ysize,	float *ylims)
{
  if (xsize != (ix2-ix1+1)) {
    PyErr_Format(PyExc_ValueError, " xvector must have %d components.", \
		   (ix2-ix1+1));
    return;
  }
  if (ysize != (ix2-ix1+1)) {
    PyErr_Format(PyExc_ValueError, " yvector must have %d components.", \
		   (ix2-ix1+1));
      return;
  }
  cpghi2d(data, nx, ny, ix1, ix2, iy1, iy2, x, ioff, bias, center, ylims);
  return;
}
%}
%clear (float *data, int nx, int ny);
%clear (int xsize, float *x), (int ysize, float *ylims);
// CPGHI2D Wrapper End

// CPGHIST Wrapper Begin
// void cpghist(int n, const float *data, float datmin, float datmax, \
//              int nbin, int pgflag);
//
%apply (int DIM1, float* IN_ARRAY1) { (int n, float* data) }
void cpghist(int n, const float *data, float datmin, float datmax, \
             int nbin, int pgflag);
%clear (int n, float* data);
// CPGHIST Wrapper End

// CPGBIN Wrapper Begin
// void cpgbin(int nbin, const float *x, const float *data, int center);
//
%apply (int DIM1, float* IN_ARRAY1) { (int len1, float* vec1),
                                      (int len2, float* vec2)}
%rename (cpgbin) mod_cpgbin;
%exception mod_cpgbin {
  $action
    if (PyErr_Occurred()) SWIG_fail;
}
%inline %{
  void mod_cpgbin(int len1, float* vec1, int len2, float* vec2, int center)
  {
    if (len1 != len2) {
      PyErr_Format(PyExc_ValueError, "Arrays of lengths (%d,%d) given", len1,
		   len2);
      return;
    }
    cpgbin(len1, vec1, vec2, center);
    return;
  }
  %}
%clear (int len1, float* vec1), (int len2, float* vec2);
// CPGBIN Wrapper End

// CPGPT Wrapper Begin
// void cpgpt(int n, const float *xpts, const float *ypts, int symbol);
//      Plot points routine.
%apply (int DIM1, float* IN_ARRAY1) { (int len1, float* vec1),
                                      (int len2, float* vec2)}
%rename (cpgpt) mod_cpgpt;
%exception mod_cpgpt {
  $action
  if (PyErr_Occurred()) SWIG_fail;
}
%inline %{
void mod_cpgpt(int len1, float* vec1, int len2, float* vec2, int symbol)
{
  if (len1 != len2) {
    PyErr_Format(PyExc_ValueError, "Arrays of lengths (%d,%d) given", len1, 
		 len2);
    return;
  }
  cpgpt(len1, vec1, vec2, symbol);
  return;
}
%}
%clear (int len1, float* vec1), (int len2, float* vec2);
// CPGPT Wrapper End

// CPGLINE Wrapper Begin
// void cpgline(int n, const float *xpts, const float *ypts);
//      Connect points in lines.
%apply (int DIM1, float* IN_ARRAY1) { (int len1, float* vec1),
                                      (int len2, float* vec2)}
%rename (cpgline) mod_cpgline;
%exception mod_cpgline {
  $action
  if (PyErr_Occurred()) SWIG_fail;
}
%inline %{
void mod_cpgline(int len1, float* vec1, int len2, float* vec2)
{
  if (len1 != len2) {
    PyErr_Format(PyExc_ValueError, "Arrays of lengths (%d,%d) given", len1, 
		 len2);
    return;
  }
  cpgline(len1, vec1, vec2);
  return;
}
%}
%clear (int len1, float* vec1), (int len2, float* vec2);
// CPGLINE Wrapper End

// NOTE: CPGIMAG and CPGGRAY share %apply and %clear directives.
// CPGIMAG Wrapper Start
// void cpgimag(const float *a, int idim, int jdim, int i1, int i2, int j1, \
//              int j2, float a1, float a2, const float *tr);
%apply (float* IN_ARRAY2, int DIM1, int DIM2) {(float* a, int idim, int jdim)}
%apply (float* IN_ARRAY1, int DIM1) {( const float* tr, int trdim)}
%rename (cpgimag) mod_cpgimag;
%exception mod_cpgimag {
  $action
  if (PyErr_Occurred()) SWIG_fail;
}
%inline %{
void mod_cpgimag(float* a, int idim, int jdim, int i1, int i2, int j1, \
                 int j2, float a1, float a2,const float* tr, int trdim)
{
  if (trdim != 6) {
    PyErr_Format(PyExc_ValueError, " trdim array size not equal to 6");
    return;
  }
  cpgimag(a, idim, jdim, i1, i2, j1, j2, a1, a2, tr);
  return;
}
%}
// CPGIMAG Wrapper End
// CPGGRAY Wrapper Start
// void cpggray(const float *a, int idim, int jdim, int i1, int i2, int j1, \
//              int j2, float fg, float bg, const float *tr);
%rename (cpggray) mod_cpggray;
%exception mod_cpggray {
  $action
  if (PyErr_Occurred()) SWIG_fail;
}
%inline %{
void mod_cpggray(float* a, int idim, int jdim, int i1, int i2, int j1, \
                 int j2, float fg, float bg, const float* tr, int trdim)
{
  if (trdim != 6) {
    PyErr_Format(PyExc_ValueError, " trdim array size not equal to 6");
    return;
  }
  cpggray(a, idim, jdim, i1, i2, j1, j2, fg, bg, tr);
  return;
}
%}
%clear (float* a, int idim, int jdim);
%clear (const float* tr, int trdim);
// CPGGRAY Wrapper End
// NOTE: End of shared %apply and %clear

 int wipinit(void);
 int wipdevice(const char *devicename);
/*   wipgetick(float *xtick , int *nxsub , float *ytick , int *nysub); */
void wipgetick(float *OUTPUT, int *OUTPUT, float *OUTPUT, int *OUTPUT);
void wipsetick(float xtick , int nxsub , float ytick , int nysub);
/*   wipgetsub(int *subx1, int *subx2, int *suby1, int *suby2); */
void wipgetsub(int *OUTPUT, int *OUTPUT, int *OUTPUT, int *OUTPUT);
 int wipmtext(char *side, float disp, float coord, float just, char *line);
void wipclose(void);
void wiplimits(void);
void wipviewport(void);
void wipmove(float x, float y);
void wippanel(int nx, int ny, int k);
void wipputlabel(const char *line, double justify);
 int wipheader(int blcx, int blcy, int trcx, int trcy, const char *xtype, \
	       const char *ytype);
void wipsetangle(double ang);
/* double wipgetvar(const char *inword, int *error)*/
double wipgetvar(const char *inword, int *OUTPUT);
 int wiparc(float majx, float majy, float arcangle, float angle, float start);
void wiparrow(float xp, float yp, float angle, float vent);
void wipexpand(double exp);
void wipltype(int style);
void wiplw(int width);
/* void wipgetcxy(float *cx, float *cy); */
void wipgetcxy(float *OUTPUT, float *OUTPUT); 
void wipdraw(float xfloat, float yfloat);
void wipsetbgci(int bgci);
void wipfont(int font);
void wipaitoffgrid(float nx, float xy);
 int wipwedge(char *side, float disp, float thick, float bg, float fg, \
	      char *label);
void wipsetitf(int type);
void wipsetsubmar(float subx, float suby);
void wippalette(int which, int levels);
void wipcolor(int color);
void wipfill(int fill);
 int wipbeam(float major, float minor, float posangle, float offx, float offy,\
	     int fillcolor, float scale, int bgrect);

/* WIPPOINTS wrapper begin 
   int wippoints(int nstyle, float style[], int nxy, float x[], \
                 float y[], int nc, float c[]);
*/
%apply (int DIM1, float* IN_ARRAY1) { (int nstyle, float* style),
                                      (int nx, float* x),
                                      (int ny, float* y),
                                      (int nc, float* c) }
%rename (wippoints) mod_wippoints;
%exception mod_wippoints {
  $action
  if (PyErr_Occurred()) SWIG_fail;
}
%inline %{
void mod_wippoints(int nstyle, float* style, int nx, float* x, 
                   int ny, float* y, int nc, float* c)
{
  if (nx != ny) {
    PyErr_Format(PyExc_ValueError, "Arrays of lengths (%d,%d) given", nx, ny);
    return;
  }
  wippoints(nstyle, style, nx, x, y, nc, c);
  return;
}
%}
%clear (int nstyle, float* style), (int nx, float* x), (int ny, float* y),
       (int nc, float* c);
// WIPPOINTS wrapper end

// WIPHLINE wrapper begin
// int wiphline(int npts, float x[], float y[], float gap, int center);
//
%apply (int DIM1, float* IN_ARRAY1) { (int len1, float* vec1),
                                      (int len2, float* vec2)}
%rename (wiphline) mod_wiphline;
%exception mod_wiphline {
  $action
  if (PyErr_Occurred()) SWIG_fail;
}
%inline %{
  void mod_wiphline(int len1, float* vec1, int len2, float* vec2, float gap,
		    int center)
{
  if (len1 != len2) {
    PyErr_Format(PyExc_ValueError, "Arrays of lengths (%d,%d) given", len1, 
		 len2);
    return;
  }
  wiphline(len1, vec1, vec2, gap, center);
  return;
}
%}
%clear (int len1, float* vec1), (int len2, float* vec2);
// WIPHLINE wrapper end

// WIPERRORBAR wrapper begin
// int wiperrorbar(int locat, float x[], float y[], float err[], int nxy);
%apply (int DIM1, float* IN_ARRAY1) { (int len1, float* vec1),
                                      (int len2, float* vec2),
                                      (int len3, float* vec3) }
%rename (wiperrorbar) mod_wiperrorbar;
%exception mod_wiperrorbar {
  $action
  if (PyErr_Occurred()) SWIG_fail;
}
%inline %{
void mod_wiperrorbar(int locat, int len1, float* vec1, int len2, float* vec2,
                     int len3, float* vec3)
{
  if ((len1 != len2) || (len1 != len3))
  {
    PyErr_Format(PyExc_ValueError, "Arrays of lengths (%d,%d,%d) given", len1, 
		 len2, len3);
    return;
  }
  wiperrorbar(locat, vec1, vec2, vec3, len1);
  return;
}
%}
%clear (int len1, float* vec1), (int len2, float* vec2), 
       (int len3, float* vec3);
// WIPERROEBAR wrapper end

// WIPSETR wrapper begin
// void wipsetr(float tr[]);
%apply (int DIM1, float* IN_ARRAY1) { (int len1, float* tr)}
%rename (wipsetr) mod_wipsetr;
%exception mod_wipsetr {
  $action
  if (PyErr_Occurred()) SWIG_fail;
}
%inline %{
void mod_wipsetr(int len1, float* tr)
{
  if (len1 != 6) {
    PyErr_Format(PyExc_ValueError, "TR length must equal 6");
    return;
  }
  wipsetr(tr);
  return;
}
%}
%clear (int len1, float* tr);
// WIPSETR wrapper end

// WIPGETR wrapper begin
// void wipgetr(float tr[]);
%apply (int DIM1, float* ARGOUT_ARRAY1) { (int len1, float* tr)}
%rename (wipgetr) mod_wipgetr;
%exception mod_wipgetr {
  $action
  if (PyErr_Occurred()) SWIG_fail;
}
%inline %{
void mod_wipgetr(int len1, float* tr)
{
  if (len1 != 6) {
    PyErr_Format(PyExc_ValueError, "TR length must equal 6");
    return;
  }
  wipgetr(tr);
  return;
}
%}
%clear (int len1, float* tr);
// WIPGETR wrapper end
