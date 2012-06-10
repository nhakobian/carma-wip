import cwip

class wip():
    def __init__(self):
        pass
    
    def NotImplemented(self):
        """Signifies that a function is not implemented. """
        raise NotImplementedError

    # Below begins reinterpreted wip functions.
    
    def device(self, device='/xw'):
        cwip.wipdevice(device)

    aitoff      = NotImplemented
    """Converts L-b coordinate values to equivalent x-y positions. """

    angle       = NotImplemented
    """Sets angle of text or points to D degrees."""

    arc         = NotImplemented
    """Drawn an arc with major axes MAJX, MAJY."""

    arrow       = NotImplemented
    """Draws an arrow."""

    #ask         = NotImplemented
    #"""Changes the current device prompt state."""

    autolevs    = NotImplemented
    """Sets up the contour levels automatically."""

    bar         = NotImplemented
    """Draws bar graphs on (x,y) pairs in direction 90(K-1)."""

    beam        = NotImplemented
    """Draws a beam."""

    bgci        = NotImplemented
    """Sets the text background color index to N."""

    bin         = NotImplemented
    """Draws a histogram of (x,y) pairs. 
    NSH - More accurately, it draws a plot in a stairstep model instead of a
          connected model."""

    box         = NotImplemented
    """Makes a box labeled according to LIMITS and TICKSIZE."""

    buffer      = NotImplemented
    """Predefined macro name that refers to the entire command buffer."""

    color       = NotImplemented
    """Select color for lines and characters."""

    connect     = NotImplemented
    """Connects (x,y) pairs with line segments."""

    contour     = NotImplemented
    """Makes a contour plot of an array read with IMAGE."""

    cursor      = NotImplemented
    """Enables cursor and returns x-y location and the key pressed."""

    data        = NotImplemented
    """Opens the file 'fspec' for reading data."""

    define      = NotImplemented
    """Creates the Macro 'xxx' and enters define mode."""

    delete      = NotImplemented
    """Removes the commands N1-N2 from a macro buffer."""

    device      = NotImplemented
    """Initializes output to a graphics device."""

    dot         = NotImplemented
    """Makes a point of the current style at the current location."""

    draw        = NotImplemented
    """Draws a line to (X,Y) from the current coordinate position."""

    echo        = NotImplemented
    """Displays the result of EXPRESSION on the screen."""

    ecolumn     = NotImplemented
    """Reads error bar data from column N of the data file."""

    # end         = NotImplemented
    # """Terminates define mode, insert mode, or exits from the program."""
    
    environment = NotImplemented
    """Sets the user limits and draws a box."""

    erase       = NotImplemented
    """Erases the graphics screen."""

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

    # free        = NotImplemented
    # """Releases items created with the NEW command."""

    globe       = NotImplemented
    """Draws a 'globe' with nlong/nlat long/lat lines."""

    halftone    = NotImplemented
    """Produces a halftone plot of an image."""

    # hardcopy    = NotImplemented
    # """Causes a stored printer plot to be plotted."""

    header      = NotImplemented
    """Loads header information of the current image."""

    # help        = NotImplemented
    # """Prints an explanation of the command xxx."""

    hi2d        = NotImplemented
    """Draws a histogram of the data read by IMAGE."""

    histogram   = NotImplemented
    """Draws a histogram of the data read by XCOLUMN."""

    hls         = NotImplemented
    """Sets the color representation using the HLS system."""

    id          = NotImplemented
    """Puts an identification label at the bottom of a plot."""

    # if          = NotImplemented
    # """Executes xxx if EXPRESSION is true."""

    image       = NotImplemented
    """Reads in an image from file 'fspec'."""

    # initialize  = NotImplemented
    # """Sets V to the result of EXPRESSION."""

    # input       = NotImplemented
    # """Reads plot commands from file 'fspec' and executes them."""

    # insert      = NotImplemented
    # """Commands are inserted before command N in a macro."""

    itf         = NotImplemented
    """Sets the current image transfer function to N."""

    label       = NotImplemented
    """Writes the string STR at the current cursor position."""

    # lcur        = NotImplemented
    # """Draws a line using the cursor."""

    ldev        = NotImplemented
    """Lists the devices currently available."""

    levels      = NotImplemented
    """Sets the contour levels for a contour plot."""

    limits      = NotImplemented
    """Sets the world limits of the plot."""

    lines       = NotImplemented
    """Limits the C, Y, E, and PCOLUMN file read to lines L1-L2."""

    # list        = NotImplemented
    # """Lists the commands of macro xxx."""

    logarithm   = NotImplemented
    """Takes the scaled logarithm of vectors and images."""

    lookup      = NotImplemented
    """Loads a RGB color lookup table."""

    # loop        = NotImplemented
    # """Executes the macro XXX COUNT times."""

    lstyle      = NotImplemented
    """Sets the current line style to N."""

    lwidth      = NotImplemented
    """Sets the current line width attribute to N."""

    # macro       = NotImplemented
    # """Used to define macros using an external file."""

    minmax      = NotImplemented
    """List the maximum and minimum values of the current image."""

    move        = NotImplemented
    """Sets the current world (user) position to (x,y)."""

    mtext       = NotImplemented
    """Writes the string STR relative to SIDE."""

    # ncurse      = NotImplemented
    # """Marks a set of points using the cursor."""

    # new         = NotImplemented
    # """Creates a new string variable, user variable, or vector."""

    # olin        = NotImplemented
    # """Marks a set of points using the cursor."""

    palette     = NotImplemented
    """Sets the color palette to entry K."""

    panel       = NotImplemented
    """Sets the plot lovation to a subpanel."""

    paper       = NotImplemented
    """Change the size of the view surface."""

    pcolumn     = NotImplemented
    """Reads point type data from column N of the current data file."""

    # phard       = NotImplemented
    # """Spool a plot to an alternative device."""

    # playback    = NotImplemented
    # """Replay macro XXX or command in the command buffer."""

    plotfit     = NotImplemented
    """Draws a plot of the most recent fit."""

    points      = NotImplemented
    """Draws points of the current style at each (x,y)."""

    poly        = NotImplemented
    """Draws a polygon."""

    putlabel    = NotImplemented
    """Writes justified text STR at the current location."""

    quarter     = NotImplemented
    """Allows quick selection of a subsection of the current image."""

    range       = NotImplemented
    """Limits the range over which to fit."""

    # read        = NotImplemented
    # """Reads plot commands from file 'fspec'."""

    rect        = NotImplemented
    """Draw a rectangle, using fill-area attributes."""

    reset       = NotImplemented
    """Full reset of the graphics state of the current plotting device."""

    rgb         = NotImplemented
    """Sets the color represenation using the RGB system."""

    scale       = NotImplemented
    """Sets the viewport size scale."""

    # set         = NotImplemented
    # """Sets the user variable V to result of EXPRESSION."""

    # show        = NotImplemented
    # """Shows current limits and attributes."""

    slevel      = NotImplemented
    """Sets the type and value used to scale contour levels."""

    # string      = NotImplemented
    # """Sets a string variable 'name' from a file."""

    subimage    = NotImplemented
    """Sets the index range of a subimage."""

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

    # write       = NotImplemented
    # """Writes macro XXX to file 'fspec'."""

    xcolumn     = NotImplemented
    """Reads X data from column N of the current file."""

    xlabel      = NotImplemented
    """Writes the label STR centered under the X axis."""

    ycolumn     = NotImplemented
    """Reads Y data from column N of the current file."""

    ylabel      = NotImplemented
    """Writes the label STR centered left of the Y axis."""

class Figure():
    def __init__(self):
        cwip.wipinit()

    def __del__(self):
        # This is an alias to cpgend(), possibly update in the future to this?
        cwip.wipclose()


    def box(self, xvars='bcnst', yvars='bcnst'):
        values = cwip.wipgetick()
        cwip.cpgtbox(xvars, values[0], values[1], yvars, values[2], values[3])
        return

    def erase(self):
        cwip.cpgpage()

    def mtext(self, side, disp, just, coord, line):
        # side - L(eft), R(ight), T(op), B(ottom)
        # disp - Offset from axis
        # just - Justification, 0.5 is center, 0 is left/bottom, 1 is right/top
        # coord- Alignment of text, 0 is left, 0.5 is center, 1 is right.
        # line - Text to place
        cwip.wipmtext(side, disp, just, coord, line)
