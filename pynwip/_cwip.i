%{
  #define SWIG_FILE_WITH_INIT
  #include "wip.h"
%}

%module cwip

%include "typemaps.i"
%include "numpy.i"

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
%apply (float* IN_ARRAY1, int DIM1) {(float* tr, int trdim)}
%rename (cpgimag) mod_cpgimag;
%exception mod_cpgimag {
  $action
  if (PyErr_Occurred()) SWIG_fail;
}
%inline %{
void mod_cpgimag(float* a, int idim, int jdim, int i1, int i2, int j1, \
                 int j2, float a1, float a2, float* tr, int trdim)
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
                 int j2, float fg, float bg, float* tr, int trdim)
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
%clear (float* tr, int trdim);
// CPGGRAY Wrapper End
// NOTE: End of shared %apply and %clear

 int wipinit(void);
 int wipdevice(const char *devicename);
/*   wipgetick(float *xtick , int *nxsub , float *ytick , int *nysub); */
void wipgetick(float *OUTPUT, int *OUTPUT, float *OUTPUT, int *OUTPUT);
/*   wipgetsub(int *subx1, int *subx2, int *suby1, int *suby2); */
void wipgetsub(int *OUTPUT, int *OUTPUT, int *OUTPUT, int *OUTPUT);
 int wipmtext(char *side, float disp, float coord, float just, char *line);
void wipclose(void);
void wiplimits(void);
void wipmove(float x, float y);
void wippanel(int nx, int ny, int k);
void wipputlabel(const char *line, double justify);
 int wipheader(int blcx, int blcy, int trcx, int trcy, const char *xtype, \
	       const char *ytype);

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
