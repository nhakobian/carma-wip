/*
	<move.c>
	10apr91 jm  Original code.

Routines:
void wipmove(float x, float y);
void wipdraw(float x, float y);
void wipgetcxy(float *cx, float *cy);
*/

#include "wip.h"

/* Global variables for just this file */

/* Code */

void wipmove(float x, float y)
{
      cpgmove(x, y);
      (void)wipsetvar("cx", (double)x);
      (void)wipsetvar("cy", (double)y);
      return;
}

void wipdraw(float x, float y)
{
      cpgdraw(x, y);
      (void)wipsetvar("cx", (double)x);
      (void)wipsetvar("cy", (double)y);
      return;
}

void wipgetcxy(float *cx, float *cy)
{
      double arg;
      LOGICAL error;

      arg = wipgetvar("cx", &error);
      *cx = (error == TRUE) ? 0.0 : arg;
      arg = wipgetvar("cy", &error);
      *cy = (error == TRUE) ? 0.0 : arg;
      return;
}
