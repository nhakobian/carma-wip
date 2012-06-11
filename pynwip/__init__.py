import cwip
import numpy
import miriad_tools

class wip():
    def __init__(self):
        """
        Wip Interface initialization routine. Currently calls built-in wip
        initialization.
        """
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

    # Below begins reinterpreted wip functions.

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
        values = cwip.wipgetick()
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
        tr = cwip.wipgetr(6)
        cwip.cpgimag(image.image[0,:,:], 1, nx, 1, ny, imax, imin, tr)

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
        blcx = 0
        trcx = image.axes[0]
        blcy = 0
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
        cwip.wipsetr(tr)

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
        #     {
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
        
    #
    # Below begins list of NotImplemented functions.
    #

    aitoff      = NotImplemented
    """Converts L-b coordinate values to equivalent x-y positions. """

    angle       = NotImplemented
    """Sets angle of text or points to D degrees."""

    arc         = NotImplemented
    """Drawn an arc with major axes MAJX, MAJY."""

    arrow       = NotImplemented
    """Draws an arrow."""

    autolevs    = NotImplemented
    """Sets up the contour levels automatically."""

    bar         = NotImplemented
    """Draws bar graphs on (x,y) pairs in direction 90(K-1)."""

    beam        = NotImplemented
    """Draws a beam."""

    bgci        = NotImplemented
    """Sets the text background color index to N."""

    color       = NotImplemented
    """Select color for lines and characters."""

    contour     = NotImplemented
    """Makes a contour plot of an array read with IMAGE."""

    dot         = NotImplemented
    """Makes a point of the current style at the current location."""

    draw        = NotImplemented
    """Draws a line to (X,Y) from the current coordinate position."""

    environment = NotImplemented
    """Sets the user limits and draws a box."""

    etxt        = NotImplemented
    """Erases the text from the view surface without affecting graphics."""

    expand      = NotImplemented
    """Expands all characters and points by a factor E."""

    fill        = NotImplemented
    """Sets the fill area style to N."""

    fit         = NotImplemented
    """Fits a curve to the (x,y) data pairs."""

    font        = NotImplemented
    """Sets the font type to type N."""

    globe       = NotImplemented
    """Draws a 'globe' with nlong/nlat long/lat lines."""

    hi2d        = NotImplemented
    """Draws a histogram of the data read by IMAGE."""

    histogram   = NotImplemented
    """Draws a histogram of the data read by XCOLUMN."""

    hls         = NotImplemented
    """Sets the color representation using the HLS system."""

    id          = NotImplemented
    """Puts an identification label at the bottom of a plot."""

    itf         = NotImplemented
    """Sets the current image transfer function to N."""

    label       = NotImplemented
    """Writes the string STR at the current cursor position."""

    levels      = NotImplemented
    """Sets the contour levels for a contour plot."""

    logarithm   = NotImplemented
    """Takes the scaled logarithm of vectors and images."""

    lookup      = NotImplemented
    """Loads a RGB color lookup table."""

    lstyle      = NotImplemented
    """Sets the current line style to N."""

    lwidth      = NotImplemented
    """Sets the current line width attribute to N."""

    minmax      = NotImplemented
    """List the maximum and minimum values of the current image."""

    palette     = NotImplemented
    """Sets the color palette to entry K."""

    plotfit     = NotImplemented
    """Draws a plot of the most recent fit."""

    poly        = NotImplemented
    """Draws a polygon."""

    range       = NotImplemented
    """Limits the range over which to fit."""

    rect        = NotImplemented
    """Draw a rectangle, using fill-area attributes."""

    reset       = NotImplemented
    """Full reset of the graphics state of the current plotting device."""

    rgb         = NotImplemented
    """Sets the color represenation using the RGB system."""

    scale       = NotImplemented
    """Sets the viewport size scale."""

    slevel      = NotImplemented
    """Sets the type and value used to scale contour levels."""

    submargin   = NotImplemented
    """Sets the gap between individual panels."""

    symbol      = NotImplemented
    """Sets the current point symbol to N."""

    ticksize    = NotImplemented
    """Sets tick intervals for the BOX command."""

    transfer    = NotImplemented
    """Specifies the image coordinate transformation."""

    vector      = NotImplemented
    """Draws a vector field as a sequence of arrows."""

    vsize       = NotImplemented
    """Sets the physical location of the plot in inches."""

    vstand      = NotImplemented
    """Sets the standard (default) viewport."""

    wedge       = NotImplemented
    """Draws a halftone wedge."""

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
    ##### Image read routines that currently will not be implemented.
    #####
    # quarter     = NotImplemented
    # """Allows quick selection of a subsection of the current image."""
    # subimage    = NotImplemented
    # """Sets the index range of a subimage."""

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
