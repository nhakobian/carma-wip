/*
	<extrema.c>
	11aug90 jm  Original code.

Routines:
void wipextrema ARGS(( float **image, int nx, int ny, float *pmin, float *pmax ));
*/

#include "wip.h"

/* Global Variables needed just for this file */

/* WIP routines needed */

/* Code */

void wipextrema(float **image, int nx, int ny, float *pmin, float *pmax)
{
      register int x, y;
      register float val, imin, imax;

      imax = imin = image[0][0];

      for (y = 0; y < ny; y++) {
        for (x = 0; x < nx; x++) {
          val = image[y][x];
          if (val < imin) imin = val;
          if (val > imax) imax = val;
        }
      }

      *pmin = imin;
      *pmax = imax;
      return;
}
