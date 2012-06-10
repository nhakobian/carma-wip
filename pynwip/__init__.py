import cwip
import numpy

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

    errorbar    = NotImplemented
    """Dears error bars on (x,y) pairs in the direction 90(K-1)."""

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

    halftone    = NotImplemented
    """Produces a halftone plot of an image."""

    header      = NotImplemented
    """Loads header information of the current image."""

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

    move        = NotImplemented
    """Sets the current world (user) position to (x,y)."""

    palette     = NotImplemented
    """Sets the color palette to entry K."""

    paper       = NotImplemented
    """Change the size of the view surface."""

    plotfit     = NotImplemented
    """Draws a plot of the most recent fit."""

    poly        = NotImplemented
    """Draws a polygon."""

    putlabel    = NotImplemented
    """Writes justified text STR at the current location."""

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

    viewport    = NotImplemented
    """Sets the physical location of the plot."""

    vsize       = NotImplemented
    """Sets the physical location of the plot in inches."""

    vstand      = NotImplemented
    """Sets the standard (default) viewport."""

    wedge       = NotImplemented
    """Draws a halftone wedge."""

    winadj      = NotImplemented
    """Sets limits and viewport to same aspect ratio."""

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
    # image       = NotImplemented
    # """Reads in an image from file 'fspec'."""
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
