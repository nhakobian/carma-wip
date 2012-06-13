import cwip
import numpy
import miriad_tools

class wip():
    def __init__(self):
        """
        Wip Interface initialization routine. Currently calls built-in wip
        initialization.
        """
        self.__dict__['pstyle'] = 1
        cwip.wipinit()

    def __del__(self):
        """
        Wip Interface destruction routine. The called function is an alias to
        cpgend(), possibly update in the future to this?
        """
        cwip.wipclose()
    
    def NotImplemented(self):
        """Signifies that a function is not implemented. """
        raise NotImplementedError

    # Attributes (wip variables)
    def _wipgetvar(self, varname):
        """
        This is a wrapper function for grabbing wip variables that do
        not have their own wrapping function. This performs some basic
        error checking.
        """
        (value, error) = cwip.wipgetvar(varname)

        if error == 1:
            raise AttributeError
        else:
            return value

    def __getattr__(self, name):
        namedict = { 
            'bgci'   : lambda : self._wipgetvar('bgci'),
            'angle'  : lambda : self._wipgetvar('angle'),
            'color'  : lambda : self._wipgetvar('color'),
            'expand' : lambda : self._wipgetvar('expand'),
            'fill'   : lambda : self._wipgetvar('fill'),
            'font'   : lambda : self._wipgetvar('font'),
            'itf'    : lambda : self._wipgetvar('itf'),
            'lstyle' : lambda : self._wipgetvar('lstyle'),
            'lwidth' : lambda : self._wipgetvar('lwidth'),
            'pstyle' : lambda : self.__dict__['pstyle'],
            'tr'     : lambda : cwip.wipgetr(6),
            'tick'   : cwip.wipgetick,
            'xsubmar': lambda : self._wipgetvar('xsubmar'), # default 2.0 
            'ysubmar': lambda : self._wipgetvar('ysubmar'), # default 2.0
            }
        
        if name not in namedict.keys():
            raise AttributeError
        
        return namedict[name]()

    def __setattr__(self, name, value):
        namedict = { 
            'bgci'    : cwip.wipsetbgci,
            'angle'   : cwip.wipsetangle,
            'color'   : cwip.wipcolor,
            'expand'  : cwip.wipexpand,
           #'fill'    : see fill function
            'font'    : cwip.wipfont,
            'itf'     : cwip.wipsetitf,
            'lstyle'  : cwip.wipltype,
            'lwidth'  : cwip.wiplw,
            'pstyle'  : lambda x : self.__dict__.__setitem__('pstyle', x),
            'tr'      : lambda x : cwip.wipsetr(x) , # command 'transfer'
           #'tick'    : ticksize command to set right now.
           #'xsubmar' : self.submargin, remove fn, and replace with var
           #'ysubmar' : self.submargin
            }

        if name not in namedict.keys():
            raise AttributeError

        namedict[name](value)

    # Below begins reinterpreted wip functions.

    def arc(self, majx, majy, pa=None, extent=360.0, start=0.0):
        """
        Drawn an arc with major axes MAJX, MAJY.

          majx   : (float) - length of the x axis component.
          majy   : (float) - length of the y-axis component.
          pa     : (float) - In degrees, the offset from the +x axis going ccw.
                             By default takes the value of the last angle 
                             setting or 0.
          extent : (float) - default 360.0, how many degrees the arc is drawn
                             through.
          start  : (float) - default 0.0, the angle offset before arc starts
                             being drawn.
        """
        # xfloat = 360.0; yfloat = 0.0;
        # if (argc == 2) {
        #     if (wiparguments(&line, 2, arg) != 2) goto MISTAKE;
        # } else if (argc == 3) {
        #     if (wiparguments(&line, 3, arg) != 3) goto MISTAKE;
        #     xfloat = arg[2];
        # } else {
        #     if (wiparguments(&line, 4, arg) != 4) goto MISTAKE;
        #     xfloat = arg[2]; yfloat = arg[3];
        # }
        # xmax = arg[0]; ymax = arg[1];
        # ymin = wipgetvar("angle", &error);
        # if (error == TRUE) goto MISTAKE;
        # if (wiparc(xmax, ymax, xfloat, ymin, yfloat)) goto MISTAKE;

        # The object self does not exist at function definition time,
        # so we must test and define for it here.
        if pa == None:
            pa = self.angle
        cwip.wiparc(majx, majy, extent, pa, start)

    def arrow(self, x, y, angle=45.0, vent=0.3):
        """
        Draws an arrow.
        """
        # xfloat = 45.0; yfloat = 0.3;
        # if (argc == 2) {
        #     if (wiparguments(&line, 2, arg) != 2) goto MISTAKE;
        # } else if (argc == 3) {
        #     if (wiparguments(&line, 3, arg) != 3) goto MISTAKE;
        #     xfloat = arg[2];
        # } else {
        #     if (wiparguments(&line, 4, arg) != 4) goto MISTAKE;
        #     xfloat = arg[2]; yfloat = arg[3];
        # }
        # xmax = arg[0]; ymax = arg[1];
        # wiparrow(xmax, ymax, xfloat, yfloat);
        cwip.wiparrow(x, y, angle, vent)

    def bin(self, x, y, k=1, gap=None):
        """
        Draws a histogram of (x,y) pairs. 
        NSH - More accurately, it draws a plot in a stairstep model instead 
        of a connected model.

          x   : (array) - Array of X values.
          y   : (array) - Array of Y values.
          k   : (int)   - 1 if data is centered on bin (default)
                          0 if data is aligned to left side of bin
          gap : (float) - Gap in data needed to draw separate graphs
        """
        # narg = 1;                       /* Center bins on the X value. */
        # if (argc == 1) 
        # {
        #     if (wiparguments(&line, 1, arg) != 1) goto MISTAKE;
        #     narg = NINT(arg[0]);        /* User specifies centering. */
        # }
        # else if (argc > 1) 
        # {
        #     if (wiparguments(&line, 2, arg) != 2) goto MISTAKE;
        #     narg = NINT(arg[0]);        /* User specifies centering. */
        #     xfloat = arg[1];            /* Gap value. */
        # }
        # xvec = wipvector("x", &nx, &npts);
        # yvec = wipvector("y", &nx, &ny);
        # npts = MIN(npts, ny);
        # if (npts <= 0) goto MISTAKE;
        # if (argc > 1) 
        # {    /* Use hline routine. */
        #     if (wiphline(npts, xvec, yvec, xfloat, narg)) goto MISTAKE;
        # } 
        # else 
        # {   /* Use cpgbin. */
        #     cpgbin(npts, xvec, yvec, narg);
        # }
        # wipmove(xvec[npts-1], yvec[npts-1]);
        x = numpy.array(x, dtype=numpy.float32)
        y = numpy.array(y, dtype=numpy.float32)
        if gap == None:
            cwip.cpgbin(x, y, k)
        else:
            cwip.wiphline(x, y, gap, k)
        cwip.wipmove(float(x[-1]), float(y[-1]))

    def box(self, xvars='bcnst', yvars='bcnst'):
        """
        Makes a box labeled according to LIMITS and TICKSIZE.

          xvars : x options string.
          yvars : y options string.
        """
        values = self.tick
        cwip.cpgtbox(xvars, values[0], values[1], yvars, values[2], values[3])
        return

    def connect(self, x, y):
        """
        Connects (x,y) pairs with line segments.

          x : (array) - Array of X values.
          y : (array) - Array of Y values.
        """
        # xvec = wipvector("x", &nx, &npts);
        # yvec = wipvector("y", &nx, &ny);
        # npts = MIN(npts, ny);
        # if (npts > 0) 
        # {
        #     cpgline(npts, xvec, yvec);
        #     wipmove(xvec[npts-1], yvec[npts-1]);
        # }
        cwip.cpgline(numpy.array(x, dtype=numpy.float32), 
                     numpy.array(y, dtype=numpy.float32))
        cwip.wipmove(x[-1], y[-1])
    
    def device(self, device='/xs'):
        """
        Initializes output to a graphics device.

          device : PGPLOT device string.
        """
        cwip.wipdevice(device)

    def dot(self):
        """
        Makes a point of the current style at the current location.
        """
        # if (argc > 0) {
        #     if (wiparguments(&line, 2, arg) != 2) goto MISTAKE;
        #     xfloat = arg[0];
        #     yfloat = arg[1];
        # } else {
        #     wipgetcxy(&xfloat, &yfloat);
        # }
        # arg[0] = wipgetvec("pstyle[1]", &error);
        # ny = (error == TRUE) ? 0 : NINT(arg[0]); error = FALSE;
        # cpgpt(1, &xfloat, &yfloat, ny);
        (cx, cy) = cwip.wipgetcxy()
        cwip.cpgpt([cx], [cy], self.pstyle)

    def draw(self, endx, endy):
        """
        Draws a line to (X,Y) from the current coordinate position.
        """
        cwip.wipdraw(float(endx), float(endy))

    def erase(self):
        """
        Erases the graphics screen.
        """
        cwip.cpgpage()

    def errorbar(self, x, y, error, loc):
        """
        Draws error bars on (x,y) pairs in the direction 90(K-1).

          x     : (vector) - 
          y     : (vector) - 
          error : (vector) - 
          loc   : (int)    - 1 along the +x direction; 
                             2 for +y; 
                             3 for -x; 
                             4 for -y 
                             5 +x and -x 
                             6 +y and -y 
        """
        # if (wiparguments(&line, 1, arg) != 1) goto MISTAKE;
        # location = NINT(arg[0]);
        # xvec = wipvector("x", &nx, &npts);
        # yvec = wipvector("y", &nx, &ny);
        # npts = MIN(npts, ny);
        # evec = wipvector("err", &nx, &ny);
        # npts = MIN(npts, ny);
        # if (npts < 1) npts = 0;
        # if (wiperrorbar(location, xvec, yvec, evec, npts)) goto MISTAKE;
        cwip.wiperrorbar(int(loc), numpy.array(x, dtype=numpy.float32), 
                         numpy.array(y, dtype=numpy.float32), 
                         numpy.array(error, dtype=numpy.float32))
        
    def fill(self, style, hatch=45.0, spacing=1.0, phase=0.0):
        """
        Sets the fill area style to N.
        """
        # argc = (argc < 1) ? 1 : ((argc > 4) ? 4 : argc);
        # if (wiparguments(&line, argc, arg) != argc) goto MISTAKE;
        # xfloat = 45.0;                     /* Default hatch angle. */
        # yfloat = 1.0;               /* Default hatch line spacing. */
        # xmin = 0.0;                 /* Default is no phase offset. */
        # switch (argc) {               /* Parse optional arguments. */
        #   case 4:    /* falls through */
        #     xmin = arg[3];         /* User specifies phase offset. */
        #   case 3:    /* falls through */
        #     yfloat = arg[2];            /* User specifies spacing. */
        #   case 2:
        #     xfloat = arg[1];        /* User specifies hatch angle. */
        #     break;
        #   default:                         /* No options supplied. */
        #     break;
        # }
        # narg = NINT(arg[0]);
        # if (argc > 1) cpgshs(xfloat, yfloat, xmin);
        # wipfill(narg);
        cwip.cpgshs(hatch, spacing, phase)
        cwip.wipfill(style)

    def globe(self, longi=5, lat=3):
        """
        Draws a 'globe' with nlong/nlat long/lat lines.
        """
        # nx = 5; ny = 3;
        # if (argc > 0) {
        #     if (wiparguments(&line, 2, arg) != 2) goto MISTAKE;
        #     nx = NINT(arg[0]);
        #     ny = NINT(arg[1]);
        # }
        # wipaitoffgrid(nx, ny);
        cwip.wipaitoffgrid(longi, lat);

    def halftone(self, image):
        """
        Produces a halftone plot of an image.
        """
        # curimage = wipimcur("curimage");
        # if (wipimagexists(curimage) == 0) 
        # {
        #     wipoutput(stderr, "You must specify an image first!\n");
        #     goto MISTAKE;
        # }
        # wipimagenxy(curimage, &nx, &ny);
        # /* bg     fg */
        # wipimageminmax(curimage, &ymin, &ymax, 0);
        # wipgetsub(&sx1, &sx2, &sy1, &sy2);
        # wipgetr(tr);
        # impic = wipimagepic(curimage);
        # wipgetcir(&cmin, &cmax);
        # narg = -1;
        # xfloat = -99.0;
        # if (argc == 2) 
        # {
        #     if (wiparguments(&line, 2, arg) != 2) goto MISTAKE;
        #     ymin = arg[0];
        #     ymax = arg[1];
        # } 
        # else if (argc == 3) 
        # {
        #     if (wiparguments(&line, 3, arg) != 3) goto MISTAKE;
        #     ymin = arg[0];
        #     ymax = arg[1];
        #     narg = NINT(arg[2]);
        # }
        # else if (argc > 3) 
        # {
        #     if (wiparguments(&line, 4, arg) != 4) goto MISTAKE;
        #     ymin = arg[0];
        #     ymax = arg[1];
        #     narg = NINT(arg[2]);
        #     xfloat = arg[3];
        # }
        # if (narg <= 0) narg = cmax - cmin + 1;
        # hmin = ymin;
        # hmax = ymax;
        # if (argc > 2)                /* Only do this if requested. */
        #     wipheq(nx, ny, impic, sx1, sx2, sy1, sy2, xfloat, ymin, ymax, \
        #            narg);
        # if ((cmin + 1) < cmax)
        #    cpgimag(*impic, nx, ny, sx1, sx2, sy1, sy2, ymin, ymax, tr);
        # else
        #    cpggray(*impic, nx, ny, sx1, sx2, sy1, sy2, ymax, ymin, tr);
        imin = float(image.image.min())
        imax = float(image.image.max())
        nx = int(image.axes[0])
        ny = int(image.axes[1])
        #xylimits = cwip.wipgetsub()
        cwip.cpgimag(image.image[0,:,:], 1, nx, 1, ny, imin, imax, self.tr)

    def header(self, image, xdir, ydir=None):
        """
        Loads header information of the image.
        
          xdir : (string) - coordinate system of x axis
          ydir : (string) - coordinate system of y axis, if none is passed
                            defaults to same value as x-axis.

          Valid coordinate system values are:
             rd : Right ascension/declination (absolute coordinates).
             so : Arcsecond offset positions.
             mo : Arcminute offset positions.
             po : Pixel offset positions.
             px : Absolute pixel positions.
             gl : General linear coordinates.
             go : General linear offset coordinates.
    
        This function will need to be ported into python for maximum utility.
        This function may disappear in the future and its abilities rolled into
        functions that use/manipulate the coordinate system (halftone, contour,
        plot, etc.
        """
        if ydir == None:
            ydir = xdir

        coord_values = ['rd', 'so', 'mo', 'po', 'px', 'gl', 'go']

        if xdir not in coord_values:
            raise ValueError("%s is not a valid coordinate system." % xdir)
        if ydir not in coord_values:
            raise ValueError("%s is not a valid coordinate system." % ydir)

        sub = cwip.wipgetsub()

        ### Time to port wipheader is now. UGH!
        # cwip.wipheader(sub[0], sub[2], sub[1], sub[3], xdir, ydir)
        # Code below is based on src/image/header.c in WIP source and
        # includes both wipheader and wipheadlim.

        # blcx = sub[0] # px_xmin
        # trcx = sub[1] # px_xmax
        # blcy = sub[2] # px_ymin
        # trcy = sub[3] # px_ymax

        # For testing force size values to the following:
        blcx = 1
        trcx = image.axes[0]
        blcy = 1
        trcy = image.axes[1]

        # Expand limits to be one half pixel larger in each direction since
        # pixels have definite sise.
        xmin = float(blcx - 0.5)
        xmax = float(trcx + 0.5)
        ymin = float(blcy - 0.5)
        ymax = float(trcy + 0.5)

        # Enter into wipheadlim, xtype - xdir, ytype - ydir
        # Computes transformation matrix which is based on xscale, xoff,
        # yscale, yoff

        if isinstance(image, miriad_tools.MirImage) == True:
            im_type = 'miriad'
            crvalx = image.crval[0]
            crpixx = image.crpix[0]
            cdeltx = image.cdelt[0]
            crvaly = image.crval[1]
            crpixy = image.crpix[1]
            cdelty = image.cdelt[1]
            ctypex = image.ctypes_n[0].lower()
            ctypey = image.ctypes_n[1].lower()
        else:
            im_type = 'pixel'
            crvalx = 0.0
            crpixx = 0.0
            cdeltx = 0.0
            crvaly = 0.0
            crpixy = 0.0
            cdelty = 0.0
            ctypex = 'px'
            ctypey = 'px'

        # If one of the axis is a declination axis, then set the cos factor
        # to that axis value.
        if ctypey == 'dec':
            cosdec = crvaly
        elif ctypex == 'dec':
            cosdec = crvalx
        else:
            cosdec = 0

        # Similarly, if one of the axis is an right ascension axis, that axis
        # must be scaled by 15, (scaling from 24 hrs to 360 degrees).

        if ctypex == 'ra':
            rafacx = 15.0
            rafacy = 1.0
        elif ctypey == 'ra':
            rafacx = 1.0
            rafacy = 15.0
        else:
            rafacx = 1.0
            rafacy = 1.0

        ## Gonna currently skip projection check, MUST ADD IN header.c:107
    
        rpdeg = numpy.pi / 180.0 # Radians per degree

        # Apparently miriad and fits store coordinate data differently.
        # It seems that miriad stores absolute positions in RADIANS.
        # From the code below, it seems that FITS is in decimal degrees
        # (NOT decimal hours).
        
        if im_type == 'miriad':
            xconvert = (3600.0 / rafacx) / rpdeg
            yconvert = (3600.0 / rafacy) / rpdeg
            cosdec = numpy.cos(cosdec)
        elif im_type == 'fits':
            xconvert = 3600.0 / rafacx
            yconvert = 3600.0 / rafacy
            cosdec = numpy.cos(cosdec * rpdeg)
        else:
            xconvert = 1.0
            yconvert = 1.0
            cosdec = numpy.cos(cosdec) # which would be cos(0) = 1

        # Potentially the user could want each axis in a different coordinate
        # system (sigh).
        # X-direction
        if   xdir == 'rd': # RA / Dec
            xscale = xconvert * cdeltx / cosdec
            xoff   = (xconvert * crvalx) - (crpixx * xscale)
        elif xdir == 'so': # Arcsecond offset positions.
            xscale = xconvert * rafacx * cdeltx
            xoff   = -crpixx * xscale
        elif xdir == 'mo': # Arcminute offset positions.
            xscale = xconvert * rafacx * cdeltx / 60.0
            xoff   = -crpixx * xscale
        elif xdir == 'po': # Pixel offset positions.
            xscale = 1.0
            xoff   = -crpixx
        elif xdir == 'go': # General linear offset coordinates.
            xscale = cdeltx
            xoff   = -crpixx * xscale 
        elif xdir == 'gl': # General linear coordinates.
            xscale = cdeltx
            xoff   = crvalx - (crpixx * xscale)
        else: # xdir == 'px' # Absolute pixel positions.
            xscale = 1.0
            xoff   = 0.0

        # Repeat for ydir.
        if   ydir == 'rd': # RA / Dec
            yscale = yconvert * cdelty
            yoff   = (yconvert * crvaly) - (crpixy * yscale)
        elif ydir == 'so': # Arcsecond offset positions.
            yscale = yconvert * rafacy * cdelty
            yoff   = -crpixy * yscale
        elif ydir == 'mo': # Arcminute offset positions.
            yscale = yconvert * rafacy * cdelty / 60.0
            yoff   = -crpixy * yscale
        elif ydir == 'po': # Pixel offset positions.
            yscale = 1.0
            yoff   = -crpixy
        elif ydir == 'go': # General linear offset coordinates.
            yscale = cdelty
            yoff   = -crpixy * yscale
        elif ydir == 'gl': # General linear coordinates.
            yscale = cdelty 
            yoff   = crvaly - (crpixy * yscale)
        else: # xdir == 'px' # Absolute pixel positions.
            yscale = 1.0
            yoff   = 0.0

        # Now scale the coordinates from pixels to chosen scale.
        xmin = (xscale * xmin) + xoff
        xmax = (xscale * xmax) + xoff
        ymin = (yscale * ymin) + yoff
        ymax = (yscale * ymax) + yoff

        # Set the limits to our newly calculated system
        # Equivalent to:
        #   cpgswin(xmin, xmax, ymin, ymax)
        #   wiplimits()
        self.limits(xmin, xmax, ymin, ymax)
        
        # Set the transformation matrix for PGIMAG, etc.
        tr = numpy.array([xoff, xscale, 0.0, yoff, 0.0, yscale], 
                         dtype=numpy.float32)
        self.tr = tr

    def hi2d(self, image, bias, slant=0, center=1, xmin=None, xmax=None,
             ymin=None, ymax=None, autolevels=True):
        """
        Draws a histogram of the data read by IMAGE.
        """
        # curimage = wipimcur("curimage");
        # if (wipimagexists(curimage) == 0) {
        #     wipoutput(stderr, "You must specify an image first!\n");
        #     goto MISTAKE;
        # }
        # wipimagenxy(curimage, &nx, &ny);
        # wipgetsub(&sx1, &sx2, &sy1, &sy2);
        # location = 0; /* no initial slant to successive y-elements. */
        # narg = 1; /* center bins on x value. */
        # if (argc == 1) {
        #     if (wiparguments(&line, 1, arg) != 1) goto MISTAKE;
        # } else if (argc == 2) {
        #     if (wiparguments(&line, 2, arg) != 2) goto MISTAKE;
        #     location = NINT(arg[1]);
        # } else {
        #     if (wiparguments(&line, 3, arg) != 3) goto MISTAKE;
        #     location = NINT(arg[1]);
        #     narg = NINT(arg[2]);
        # }
        # ymax = arg[0];  /* Required bias value. */
        # nxsub = sx2 - sx1 + 1;
        # xvec = vector(nxsub);
        # yvec = vector(nxsub);
        # if ((xvec == (float *)NULL) || (yvec == (float *)NULL)) {
        #     if (xvec) freevector(xvec);
        #     if (yvec) freevector(yvec);
        #     wipoutput(stderr, "Trouble allocating work arrays.\n");
        #     goto MISTAKE;
        # }
        # for (j = 0; j < nxsub; j++) xvec[j] = sx1 + j;
        # impic = wipimagepic(curimage);
        # cpghi2d(*impic, nx, ny, sx1, sx2, sy1, sy2,
        #          xvec, location, ymax, narg, yvec);
        # freevector(xvec);
        # freevector(yvec);
        if xmin == None:
            xmin = 1
        if ymin == None:
            ymin = 1
        if xmax == None:
            xmax = int(image.axes[0])
        if ymax == None:
            ymax = int(image.axes[1])
        xmin = int(xmin)
        xmax = int(xmax)
        ymin = int(ymin)
        ymax = int(ymax)
        xvec = numpy.arange(xmin-1, xmax, dtype=numpy.float32)
        yvec = numpy.zeros(xvec.size, dtype=numpy.float32)

        if (autolevels == True):
            nlevels = ymax-ymin+1
            int_max = nlevels * bias
            self.limits(xmin, xmax, -bias, int_max)

        cwip.cpghi2d(image.image[0, :, :], xmin, xmax, ymin, ymax,
                     xvec, slant, bias, center, yvec) 


    def histogram(self, array, xmin=None, xmax=None, n=5):
        """
        Draws a histogram of the data read by XCOLUMN.
          Note: This function should probably be replaced by a numpy analysis
          routine so levels can be autoset, and for general clenliness.
        
          array : array to histogram
          MIN
          MAX 
          N
        """
        # xvec = wipvector("x", &nx, &npts);
        # if (npts < 1) goto MISTAKE;
        # wiprange(npts, xvec, &xmin, &xmax);
        # narg = 5; /* Number of bins. */
        # if (argc == 2) {
        #     if (wiparguments(&line, 2, arg) != 2) goto MISTAKE;
        #     xmin = arg[0]; xmax = arg[1];
        # } else if (argc > 2) {
        #     if (wiparguments(&line, 3, arg) != 3) goto MISTAKE;
        #     xmin = arg[0]; xmax = arg[1];
        #     narg = NINT(arg[2]);
        # }
        # ny = 1;   /* PGFLAG = 1 ==> no pgenv called. */
        # cpghist(npts, xvec, xmin, xmax, narg, ny);
        # wipgetcxy(&xfloat, &yfloat);
        # wipmove(xvec[npts-1], yfloat);
        if xmin == None:
            xmin = numpy.min(array)
        if xmax == None:
            xmax = numpy.max(array)
        
        cwip.cpghist(array, float(xmin), float(xmax), n, 1)

    def label(self, string):
        """
        Writes the string STR at the current cursor position.
        This is an alias to self.putlabel(string, 0.0)
        """
        self.putlabel(string, 0.0)

    def limits(self, *args):
        """
        Sets the world limits of the plot.
        
        Two ways to call:
        ONE
        ===
          x    : (array) - Auto limits on X array.
          y    : (array) - Auto limits on Y array.

        TWO
        ===
          xmin : (float) - Minimum X value.
          xmax : (float) - Maximum X value.
          ymin : (float) - Minimum Y value.
          ymax : (float) - Maximum Y value.
        """
        # xvec = wipvector("x", &nx, &npts);
        # yvec = wipvector("y", &nx, &ny);
        # npts = MIN(npts, ny);
        # if (npts < 1) npts = 0;
        # wiprange(npts, xvec, &xmin, &xmax);
        # wiprange(npts, yvec, &ymin, &ymax);
        # if (argc > 0) 
        # {
        #     if (wiparguments(&line, 4, arg) != 4) goto MISTAKE;
        #     if (arg[0] != arg[1]) 
        #     {
        #         xmin = arg[0];
        #         xmax = arg[1];
        #     }
        #     if (arg[2] != arg[3]) 
        #     { for a passed variable
        #         ymin = arg[2];
        #         ymax = arg[3];
        #     }
        # }
        # cpgswin(xmin, xmax, ymin, ymax);
        # wiplimits();
        nargs = len(args)

        if (nargs == 2):
            # Make sure input data is an array and extract extrema.
            x_array = numpy.array(args[0])
            y_array = numpy.array(args[1])
            xmin = x_array.min()
            xmax = x_array.max()
            ymin = y_array.min()
            ymax = y_array.max()
            
            # WIP gives 5% padding around each of them.
            xpadd = (xmax - xmin) * 0.05
            ypadd = (ymax - ymin) * 0.05

            xmin -= xpadd
            xmax += xpadd
            ymin -= ypadd
            ymax += ypadd
        elif (nargs == 4):
            xmin = float(args[0])
            xmax = float(args[1])
            ymin = float(args[2])
            ymax = float(args[3])
        else:
            raise TypeError("Error in arguments to 'limits'.")

        cwip.cpgswin(xmin, xmax, ymin, ymax) # Sets the window limits
        cwip.wiplimits() # Grabs limits set with pgswin and also saves them
                         # as wip variables x1, x2, y1, y2.

    def move(self, x, y):
        """
        Sets the current world (user) position to (x,y).

          x : (float) - X position
          y : (float) - Y position
        """
        # if (wiparguments(&line, 2, arg) != 2) goto MISTAKE;
        # xfloat = arg[0];
        # yfloat = arg[1];
        # wipmove(xfloat, yfloat);
        cwip.wipmove(float(x), float(y))

    def mtext(self, side, disp, just, coord, string):
        """
        Writes the string STR relative to SIDE.

          side   : (string) - L(eft), R(ight), T(op), B(ottom)
          disp   : (float)  - Offset from axis
          just   : (float)  - Justification, 0.5 is center, 0 is left/bottom, 
                              1 is right/top
          coord  : (float)  - Alignment of text, 0 is left, 0.5 is center, 
                              1 is right.
          string : (string) - Text to insert
        """
        cwip.wipmtext(side, disp, just, coord, string)

    def palette(self, num, levels=0):
        """
        Sets the color palette to entry K.
        """
        cwip.wippalette(num, levels)

    def panel(self, nx, ny, panel):
        """
        Sets the plot lovation to a subpanel.
        """
        # if (wiparguments(&line, 3, arg) != 3) goto MISTAKE;
        # nx = NINT(arg[0]); ny = NINT(arg[1]); narg = NINT(arg[2]);
        # wippanel(nx, ny, narg);
        cwip.wippanel(nx, ny, panel)

    def paper(self, width, aspect, units='in', px_scale=100):
        """
        Change the size of the view surface.
        """
        # if (wiparguments(&line, 2, arg) != 2) goto MISTAKE;
        # xfloat = arg[0];
        # yfloat = arg[1];
        # cpgpap(xfloat, yfloat);
        if units=='px':
            # px_scale is how many pixels per inch the device has.
            width = width / float(px_scale)
        cwip.cpgpap(float(width), float(aspect))

    def points(self, x=None, y=None, style=[2], color=[]):
        """
        Draws points of the current style at each (x,y).

          x     : (array) - Array of x values to plot.
          y     : (array) - Array of y values to plot.
          style : (array) - default [2] - array of styles at each point.
          color : (array) - default []  - array of color indices at each point.
        """
        # Force cast of array to float32 in order to satisfy C array types.
        cwip.wippoints(style, numpy.array(x, dtype=numpy.float32), 
                       numpy.array(y, dtype=numpy.float32), color)


    def poly(self, x, y):
        """
        Draws a polygon.
        """
        # xvec = wipvector("x", &nx, &npts);
        # yvec = wipvector("y", &nx, &ny);
        # npts = MIN(npts, ny);
        # if (npts < 1) goto MISTAKE;
        # cpgpoly(npts, xvec, yvec);
        # wipmove(xvec[0], yvec[0]);
        cwip.cpgpoly(x, y)
        self.move(x[0], y[0])


    def putlabel(self, string, just=0.5):
        """
        Writes justified text STR at the current location.

          string : (string) - String value to write on screen.
          just   : (float)  - Justification between 0,1. 0.5 is centered
        """
        # if (argc < 2) 
        # {
        #     wipoutput(stderr, "A label (string) is required.\n");
        #     goto MISTAKE;
        # }
        # if (wiparguments(&line, 1, arg) != 1) goto MISTAKE;
        # arg[0] = ABS(arg[0]);
        # wipputlabel(line, arg[0]);
        cwip.wipputlabel(string, just)

    def rect(self, xmin, xmax, ymin, ymax):
        """
        Draw a rectangle, using fill-area attributes.
        """
        # if (wiparguments(&line, 4, arg) != 4) goto MISTAKE;
        # xmin = arg[0]; xmax = arg[1];
        # ymin = arg[2]; ymax = arg[3];
        # cpgrect(xmin, xmax, ymin, ymax);
        cwip.cpgrect(xmin, xmax, ymin, ymax)

    def reset(self):
        """
        Full reset of the graphics state of the current plotting device.
        """
        # float tr[6];
        #
        # tr[0] = 0.0; tr[1] = 1.0; tr[2] = 0.0;
        # tr[3] = 0.0; tr[4] = 0.0; tr[5] = 1.0;
        #
        # wipcolor(1);
        # wipexpand(1.0);
        # wipfill(1);
        # wipfont(1);
        # wipltype(1);
        # wiplw(1);
        # wipsetbgci(-1);
        #
        # wipsetangle(0.0);
        # wipsetr(tr);
        # wipsetick(0.0, 0, 0.0, 0);
        # wipsetitf(0);
        #
        # wippalette(0, 0);
        self.color = 1
        self.expand = 1
        self.fill(1)
        self.font = 1
        self.lstyle = 1
        self.lwidth = 1
        self.bgci = -1
        self.angle = 0.0
        self.tr = numpy.array([0.0, 1.0, 0.0, 0.0, 0.0, 1.0], 
                              dtype=numpy.float32)
        self.ticksize(0.0, 0, 0.0, 0)
        self.itf = 0
        self.palette(0, 0)

    def submargin(self, xsub, ysub):
        """
        Sets the gap between individual panels.
        
        Defaults, xsub, ysub = 2.0
        """
        cwip.wipsetsubmar(xsub, ysub)

    def symbol(self, value):
        """
        Sets the current point symbol to N.
        """
        self.pstyle = value

    def ticksize(self, xtick, nxsub, ytick, nysub):
        """
        Sets tick intervals for the BOX command.
        """
        cwip.wipsetick(xtick, nxsub, ytick, nysub)

    def xlabel(self, string):
        """
        Writes the label STR centered under the X axis.

          string : (string) - Text to place along the x-axis.
        """
        # PGPLOT convenience function equivalent to wip command:
        #   mtext 'B' 3.2 0.5 0.5 "STRING"
        cwip.cpglab(string, '', '')

    def ylabel(self, string):
        """
        Writes the label STR centered under the Y axis.

          string : (string) - Text to place along the y-axis.
        """
        # PGPLOT convenience function equivalent to wip command:
        #   mtext 'L' 2.2 0.5 0.5 "STRING"
        cwip.cpglab('', string, '')

    def winadj(self, xmin, xmax, ymin, ymax):
        """
        Sets limits and viewport to same aspect ratio.
        """
        cwip.cpgwnad(float(xmin), float(xmax), float(ymin), float(ymax))
        cwip.wiplimits()
        cwip.wipviewport()

    def viewport(self, xmin, xmax, ymin, ymax):
        """
        Sets the physical location of the plot.
        """
        if (xmin < 0) or (xmin > 1):
            raise ValueError("Viewport values must be between 0 and 1")
        if (xmax < 0) or (xmax > 1):
            raise ValueError("Viewport values must be between 0 and 1")
        if (ymin < 0) or (ymin > 1):
            raise ValueError("Viewport values must be between 0 and 1")
        if (ymax < 0) or (ymax > 1):
            raise ValueError("Viewport values must be between 0 and 1")

        cwip.cpgsvp(float(xmin), float(xmax), float(ymin), float(ymax))
        cwip.wipviewport()

    def wedge(self, side, disp, thick, min, max, boxarg='bcst'):
        """
        Draws a halftone wedge.

          SIDE      : `B', `L', `T', or `R' to specify Bottom, Left, Top, or 
                      Right side of the viewport. 'P' Uses pgplot wedge fn.
          DISP      : Displacement from the frame edge (in character height 
                      units). If DISP is negative, then the wedge is drawn 
                      inside the viewport. 
          THICK     : Thickness of the wedge (in character height units).
          MIN / MAX : Specify the intensity range of the wedge. By default,
                      MIN and MAX are the values used by the most recent call
                      to the HALFTONE command. Providing the values of MIN and
                      MAX will cause WEDGE to display a different range of 
                      intensities when labeling the wedge box. 
          BOXARG    : Control the box around the wedge is drawn (or omit it).
                      By default, a simple box is drawn sets BOXARG to BCSTN/M
                      (depending on the orientation); to eliminate the box, 
                      set BOXARG to 0 (for more information on permitted box
                      arguments, see the BOX command). The arguments from the
                      most recent call to the TICKSIZE command are used to 
                      draw a box around the wedge and numerically label it.
        """
        if (side.lower() == 'r') or (side.lower() == 't'):
            boxarg += 'm'
        elif (side.lower() == 'l') or (side.lower() == 'b'):
            boxarg += 'n'

        cwip.wipwedge(side, disp, thick, float(min), float(max), boxarg)
        # if ((ptr = wipparse(&line)) == (char *)NULL) goto MISTAKE;
        # if (wiparguments(&line, 2, arg) != 2) goto MISTAKE;
        # xfloat = arg[0]; yfloat = arg[1]; xmin = hmin; xmax = hmax;
        # par = "";
        # if (argc > 3) {
        #     if (wiparguments(&line, 2, arg) != 2) goto MISTAKE;
        #     xmin = arg[0]; xmax = arg[1];
        #     par = line;
        # }
        # if ((Strchr(ptr, 'i') == (char *)NULL) &&
        #     (Strchr(ptr, 'I') == (char *)NULL) &&
        #     (Strchr(ptr, 'g') == (char *)NULL) &&
        #     (Strchr(ptr, 'G') == (char *)NULL)) 
        # {
        #     (void)Strcpy(infile, ptr);
        #     wipgetcir(&cmin, &cmax);
        #     if ((cmin + 1) < cmax)
        #        (void)Strcat(infile, "i");
        #     else
        #        (void)Strcat(infile, "g");
        #     ptr = infile;
        # }
        # if (wipwedge(ptr, xfloat, yfloat, xmin, xmax, par)) goto MISTAKE;
        
    #
    # Below begins list of NotImplemented functions.
    #

    aitoff      = NotImplemented
    """Converts L-b coordinate values to equivalent x-y positions. """

    autolevs    = NotImplemented
    """Sets up the contour levels automatically."""

    bar         = NotImplemented
    """Draws bar graphs on (x,y) pairs in direction 90(K-1)."""

    beam        = NotImplemented
    """Draws a beam."""

    contour     = NotImplemented
    """Makes a contour plot of an array read with IMAGE."""

    environment = NotImplemented
    """Sets the user limits and draws a box."""

    hls         = NotImplemented
    """Sets the color representation using the HLS system."""

    levels      = NotImplemented
    """Sets the contour levels for a contour plot."""

    lookup      = NotImplemented
    """Loads a RGB color lookup table."""

    rgb         = NotImplemented
    """Sets the color represenation using the RGB system."""

    slevel      = NotImplemented
    """Sets the type and value used to scale contour levels."""

    vector      = NotImplemented
    """Draws a vector field as a sequence of arrows."""

    vsize       = NotImplemented
    """Sets the physical location of the plot in inches."""

    vstand      = NotImplemented
    """Sets the standard (default) viewport."""

    #####
    ##### Functions whose purpose isn't clear.
    #####
    # scale       = NotImplemented
    # """Sets the viewport size scale."""
    # id          = NotImplemented
    # """Puts an identification label at the bottom of a plot."""

    #####
    ##### Data read routines that currently will not be implemented.
    #####
    # data        = NotImplemented
    # """Opens the file 'fspec' for reading data."""
    # ecolumn     = NotImplemented
    # """Reads error bar data from column N of the data file."""
    # pcolumn     = NotImplemented
    # """Reads point type data from column N of the current data file."""
    # xcolumn     = NotImplemented
    # """Reads X data from column N of the current file."""
    # ycolumn     = NotImplemented
    # """Reads Y data from column N of the current file."""

    #####
    ##### Image fit routines that currently will not be implemented.
    #####
    # fit         = NotImplemented
    # """Fits a curve to the (x,y) data pairs."""
    # range       = NotImplemented
    # """Limits the range over which to fit."""
    # plotfit     = NotImplemented
    # """Draws a plot of the most recent fit."""

    #####
    ##### Image read routines that currently will not be implemented.
    #####
    # quarter     = NotImplemented
    # """Allows quick selection of a subsection of the current image."""
    # subimage    = NotImplemented
    # """Sets the index range of a subimage."""
    # minmax      = NotImplemented
    # """List the maximum and minimum values of the current image."""
    # logarithm   = NotImplemented
    # """Takes the scaled logarithm of vectors and images."""

    #####
    ##### Interactive commands that will not be implemented.
    #####
    # ask         = NotImplemented
    # """Changes the current device prompt state."""
    # buffer      = NotImplemented
    # """Predefined macro name that refers to the entire command buffer."""
    # cursor      = NotImplemented
    # """Enables cursor and returns x-y location and the key pressed."""
    # define      = NotImplemented
    # """Creates the Macro 'xxx' and enters define mode."""
    # delete      = NotImplemented
    #"""Removes the commands N1-N2 from a macro buffer."""
    # echo        = NotImplemented
    # """Displays the result of EXPRESSION on the screen."""
    # end         = NotImplemented
    # """Terminates define mode, insert mode, or exits from the program."""
    # etxt        = NotImplemented
    # """Erases the text from the view surface without affecting graphics."""
    # free        = NotImplemented
    # """Releases items created with the NEW command."""
    # hardcopy    = NotImplemented
    # """Causes a stored printer plot to be plotted."""
    # help        = NotImplemented
    # """Prints an explanation of the command xxx."""
    # if          = NotImplemented
    # """Executes xxx if EXPRESSION is true."""
    # initialize  = NotImplemented
    # """Sets V to the result of EXPRESSION."""
    # input       = NotImplemented
    # """Reads plot commands from file 'fspec' and executes them."""
    # insert      = NotImplemented
    # """Commands are inserted before command N in a macro."""
    # lcur        = NotImplemented
    # """Draws a line using the cursor."""
    # ldev        = NotImplemented
    # """Lists the devices currently available."""
    # lines       = NotImplemented
    # """Limits the C, Y, E, and PCOLUMN file read to lines L1-L2."""
    # list        = NotImplemented
    # """Lists the commands of macro xxx."""
    # loop        = NotImplemented
    # """Executes the macro XXX COUNT times."""
    # macro       = NotImplemented
    # """Used to define macros using an external file."""
    # ncurse      = NotImplemented
    # """Marks a set of points using the cursor."""
    # new         = NotImplemented
    # """Creates a new string variable, user variable, or vector."""
    # olin        = NotImplemented
    # """Marks a set of points using the cursor."""
    # phard       = NotImplemented
    # """Spool a plot to an alternative device."""
    # playback    = NotImplemented
    # """Replay macro XXX or command in the command buffer."""
    # read        = NotImplemented
    # """Reads plot commands from file 'fspec'."""
    # set         = NotImplemented
    # """Sets the user variable V to result of EXPRESSION."""
    # show        = NotImplemented
    # """Shows current limits and attributes."""
    # string      = NotImplemented
    # """Sets a string variable 'name' from a file."""
    # write       = NotImplemented
    # """Writes macro XXX to file 'fspec'."""
