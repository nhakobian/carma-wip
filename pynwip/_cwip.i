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

 int wipinit(void);
 int wipdevice(const char *devicename);
/*   wipgetick(float *xtick , int *nxsub , float *ytick , int *nysub); */
void wipgetick(float *OUTPUT, int *OUTPUT, float *OUTPUT, int *OUTPUT);
 int wipmtext(char *side, float disp, float coord, float just, char *line);
void wipclose(void);
void wiplimits(void);
void wipmove(float x, float y);

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
