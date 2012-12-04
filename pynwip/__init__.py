import cwip
import numpy
import miriad_tools
import palettes

rpdeg = numpy.pi/180.

class wip():
    def __init__(self, device_spec='/xs'):
        """
        Wip Interface initialization routine. Currently calls built-in wip
        initialization.
        """
        self.device(device_spec)
        self.reset()

    def reset(self):
        """
        Full reset of the graphics state of the current plotting device.
        """
        self.angle = 0.0
        self.bgci = -1
        self.color = 1
        self.expand = 1
        self.font = 1
        self.itf = 0
        self.lstyle = 1
        self.lwidth = 1
        self.pstyle = 1
        self.paneldata = {'oldnx' : 0, 'oldny' : 0}
        self.tr = numpy.array([0.0, 1.0, 0.0, 0.0, 0.0, 1.0], 
                              dtype=numpy.float32)
        self.ticksize(0.0, 0, 0.0, 0) # Sets xtick, nxsub, ytick, nysub
        self.submargin(2.0, 2.0)      # sets xsubmar, ysubmar
        self.fill(1, 45.0, 1.0, 0.0)  # Sets fstyle, and default hatching style


        self.palette(0, 0)

        # Reset the panel.
        self.panel(1, 1, 1)

    def __del__(self):
        """
        Wip Interface destruction routine. The called function is an alias to
        cpgend(), possibly update in the future to this?
        """
        cwip.cpgend()
    
    def __getattr__(self, name):
        namedict = { 
            'angle'     : lambda : self.__dict__['angle'],
            'bgci'      : cwip.cpgqtbg,
            'color'     : cwip.cpgqci,
            'expand'    : cwip.cpgqch,
            'font'      : cwip.cpgqcf,
            'fstyle'    : cwip.cpgqfs,
            'itf'       : cwip.cpgqitf,
            'lstyle'    : cwip.cpgqls,
            'lwidth'    : cwip.cpgqlw,
            'paneldata' : lambda : self.__dict__['paneldata'],
            'pstyle'    : lambda : self.__dict__['pstyle'],
            'tr'        : lambda : self.__dict__['tr'],
            ####                ticksize variables                    ####
            #### Can be set/retrieved with ticksize function as well. ####
            'xtick'     : lambda : self.__dict__['xtick'],
            'nxsub'     : lambda : self.__dict__['nxsub'],
            'ytick'     : lambda : self.__dict__['ytick'],
            'nysub'     : lambda : self.__dict__['nysub'],
            ####                 submargin variables                   ####
            #### Can be set/retrieved with submargin function as well. ####
            'xsubmar'   : lambda : self.__dict__['xsubmar'],
            'ysubmar'   : lambda : self.__dict__['ysubmar'],
            }
        
        if name not in namedict.keys():
            raise AttributeError
        
        return namedict[name]()

    def __setattr__(self, name, value):
        namedict = { 
            'angle'     : lambda x : self.__dict__.__setitem__('angle', x),
            'bgci'      : cwip.cpgstbg,
            'color'     : cwip.cpgsci,
            'expand'    : cwip.cpgsch,
            'font'      : cwip.cpgscf,
            'fstyle'    : cwip.cpgsfs,
            'itf'       : cwip.cpgsitf,
            'lstyle'    : cwip.cpgsls,
            'lwidth'    : cwip.cpgslw,
            'paneldata' : lambda x : self.__dict__.__setitem__('paneldata', x),
            'pstyle'    : lambda x : self.__dict__.__setitem__('pstyle', x),
            'tr'        : lambda x : self.__dict__.__setitem__('tr', x),
            ####                ticksize variables                    ####
            #### Can be set/retrieved with ticksize function as well. ####
            'xtick'     : lambda x : self.__dict__.__setitem__('xtick', x),
            'nxsub'     : lambda x : self.__dict__.__setitem__('nxsub', x),
            'ytick'     : lambda x : self.__dict__.__setitem__('ytick', x),
            'nysub'     : lambda x : self.__dict__.__setitem__('nysub', x),
            ####                 submargin variables                   ####
            #### Can be set/retrieved with submargin function as well. ####
            'xsubmar'   : lambda x : self.__dict__.__setitem__('xsubmar', x),
            'ysubmar'   : lambda x : self.__dict__.__setitem__('ysubmar', x),
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
        # The object self does not exist at function definition time,
        # so we must test and define for it here.
        if pa == None:
            pa = self.angle

        (ox1, ox2, oy1, oy2) = self.limits()
        (ocx, ocy) = self.move()
        expand = self.expand

        a = majx / 2.0
        b = majy / 2.0

        alpha = start * rpdeg
        theta = pa * rpdeg
        costheta = numpy.cos(theta)
        sintheta = numpy.sin(theta)

        step = extent
        if (abs(extent) > 360.0):
            step -= (360.0 * int(extent / 360.0))
        division = 360.0 * expand
        step *= (rpdeg / division)
        nstep = int(division + 1.0)

        # To make sure the angle of the arc is clockwise always (even when
        # the axis direction is reversed), reset the limits.
        x1 = 0.0
        x2 = abs(ox2 - ox1)
        y1 = 0.0
        y2 = abs(oy2 - oy1)
        cx = (ocx - ox1) * x2 / (ox2 - ox1)
        cy = (ocy - oy1) * y2 / (oy2 - oy1)
        self.limits(x1, x2, y1, y2)
        self.move(cx, cy)

        # To reduce the number of calls to sin and cos, use the identities:
        # cos(alpha+step) = cos(alpha)cos(step) - sin(alpha)sin(step)
        # sin(alpha+step) = sin(alpha)cos(step) + cos(alpha)sin(step)
        # This lets the angle "alpha" to be incremented by an amount
        # "step" and the new cos(alpha) & sin(alpha) to be computed
        # without having to call cos() or sin() again.
        sinstep = numpy.sin(step)
        cosstep = numpy.cos(step)
        sinalpha = numpy.sin(alpha)
        cosalpha = numpy.cos(alpha)

        xarc = numpy.zeros(nstep, dtype=numpy.float32)
        yarc = numpy.zeros(nstep, dtype=numpy.float32)
        
        # Perhaps port this to full array math if possible? Should gain some
        # speed that way.
        # Fill the arrays
        for j in xrange(0, nstep):
            delx = a * cosalpha
            dely = b * sinalpha
            # Rotate from prime coordinates to viewport (x, y)
            xarc[j] = cx + ((delx * costheta) - (dely * sintheta))
            yarc[j] = cy + ((delx * sintheta) + (dely * costheta))
            savecos = (cosalpha * cosstep) - (sinalpha * sinstep)
            sinalpha = (sinalpha * cosstep) + (cosalpha * sinstep)
            cosalpha = savecos

        fill = self.fstyle
        if fill == 2:
            cwip.cpgline(xarc, yarc)
        else:
            cwip.cpgpoly(xarc, yarc)

        # Reset original coords
        self.limits(ox1, ox2, oy1, oy2)
        self.move(ocx, ocy)
        return

    def arrow(self, x, y, angle=45.0, vent=0.3):
        """
        Draws an arrow.
        """
        (ocx, ocy) = self.move()
        fill = self.fstyle
        cwip.cpgsah(int(fill), angle, vent)
        cwip.cpgarro(ocx, ocy, x, y)

    def bar(self, x, y, color, location, threshold=None, gap=0):
        """
        Draws bar graphs on (x,y) pairs in direction 90(K-1).
        """
        if threshold == None:
            narg = 0
            threshold = 0
        else:
            narg = 1

        if ((gap > 0.0) and (len(x) < 0)):
            return
        elif ((gap <= 0) and (len(x) < 2)):
            return

        saveColor = self.color
        (cmin, cmax) = cwip.cpgqcol()

        lastColor = saveColor
        defaultColor = saveColor
        if ((len(color) > 0) and (color[0] >= cmin) and (color[0] <= cmax)):
            defaultColor = color[0]

        ibar = (location - 1) % 4

        (xleft, xright, ybot, ytop) = self.limits()
        if (narg != 0):
            if ibar == 0:
                xleft = threshold
            elif ibar == 1:
                ybot = threshold
            elif ibar == 2:
                xright = threshold
            elif ibar == 3:
                ytop = threshold

        cwip.cpgbbuf() # Start buffered output

        npts = len(x)

        if (gap > 0.0):
            halfwidth = gap / 2.0
            for j in xrange(0, npts):
                x1 = x[j] - halfwidth
                x2 = x[j] + halfwidth
                y1 = y[j] - halfwidth
                y2 = y[j] + halfwidth

                if ibar == 0:
                    x1 = xleft
                    x2 = x[j]
                elif ibar == 1:
                    y1 = ybot
                    y2 = y[j]
                elif ibar == 2:
                    x1 = x[j]
                    x2 = xright
                elif ibar == 3:
                    y1 = y[j]
                    y2 = ytop

                ic = j
                if ((len(color) > 0) and (ic < len(color)) and 
                    (color[ic] >= cmin) and (color[ic] <= cmax)):
                    newColor = color[ic]
                else:
                    newColor = defaultColor

                if (newColor != lastColor):
                    self.color = newColor
                lastColor = newColor

                self.rect(x1, x2, y1, y2)
        else:
            xlast = 0.5 * ((3.0 * x[0]) - x[1])
            ylast = 0.5 * ((3.0 * y[0]) - y[1])
            for j in xrange(1, npts):
                if (j < npts):
                    xave = 0.5 * (x[j] + x[j - 1])
                    yave = 0.5 * (y[j] + y[j - 1])
                else:
                    xave = 0.5 * ((3.0 * x[npts - 1]) - x[npts - 2])
                    yave = 0.5 * ((3.0 * y[npts - 1]) - y[npts - 2])

                if ibar == 0:
                    x1 = xleft
                    x2 = x[j-1]
                    y1 = ylast
                    y2 = yave
                elif ibar == 1:
                    x1 = xlast
                    x2 = xave
                    y1 = ybot
                    y2 = y[j-1]
                elif ibar == 2:
                    x1 = x[j-1]
                    x2 = xright
                    y1 = ylast
                    y2 = yave
                elif ibar == 3:
                    x1 = xlast
                    x2 = xave
                    y1 = y[j-1]
                    y2 = ytop
                
                ic = j - 1
                if ((len(color) > 0) and (ic < len(color)) and 
                    (color[ic] >= cmin) and (color[ic] <= cmax)):
                    newColor = color[ic]
                else:
                    newColor = defaultColor

                if (newColor != lastColor):
                    self.color = newColor
                lastColor = newColor

                self.rect(x1, x2, y1, y2)
                xlast = xave
                ylast = yave
        
        if saveColor != lastColor:
            self.color = saveColor

        cwip.cpgebuf()

    def beam(self, majx, majy, pa, offx=0, offy=0, scale=-1, fillcolor=15, \
                 bgrect=0, fill=1):
        """
        Draws a beam.

        MAJ
        MIN
        PA
        [OFFX]
        [OFFY] 
        [SCALE] 
        [FILLCOLOR] 
        [BGRECT]
        """
        # cwip.wipbeam(majx, majy, pa, offx, offy, fillcolor, scale, bgrect)
        
        # Ported version:
        (ox1, ox2, oy1, oy2) = self.limits()
        (ocx, ocy) = self.move()
        color = self.color
        ofill = self.fstyle
        style = self.lstyle

        # Determine the extent in the X and Y directions of the beam.
        sp = numpy.sin(rpdeg * (90 + pa))
        cp = numpy.cos(rpdeg * (90 + pa))
        x1 = majx * cp
        x2 = majy * sp
        y1 = majx * sp
        y2 = majy * cp
        sx = numpy.sqrt((x1 * x1) + (x2 * x2))
        sy = numpy.sqrt((y1 * y1) + (y2 * y2))

        if scale > 0:
            factor = scale
        else:
            factor = 15.0 * numpy.cos(rpdeg * (oy1 + oy2) / (2.0 * 3600.0))

        x1 = 0.0
        x2 = (ox2 - ox1) * factor
        y1 = 0.0
        y2 = oy2 - oy1
        cx = (ocx - ox1) * factor
        cy = ocy - oy1

        self.limits(x1, x2, y1, y2)

        if x2 < 0:
            xtmp = -1
        else:
            xtmp = 1
        cx += (sx * offx * xtmp)
        if y2 < 0:
            ytmp = -1
        else:
            ytmp = 1
        cy += (sy * offy * ytmp)

        self.move(cx, cy)
        self.fill(fill)
        self.lstyle = 1
        
        if bgrect >= 0:
            rectx1 = cx - (sx / 2.0)
            rectx2 = rectx1 + sx
            recty1 = cy - (sy / 2.0)
            recty2 = recty1 + sy
            self.color = bgrect
            self.rect(rectx1, rectx2, recty1, recty2)

        self.move(cx, cy)
        self.color = fillcolor
        self.arc(majx, majy, (90 + pa), 360.0, 0.0)

        self.color = color
        self.fill(2)
        self.arc(majx, majy, (90 + pa), 360.0, 0.0)

        self.fill(ofill)
        self.lstyle = style
        self.limits(ox1, ox2, oy1, oy2)
        self.move(ocx, ocy)
        return

    def bin(self, x, y, k=1):
        """
        Draws a histogram of (x,y) pairs. 
        NSH - More accurately, it draws a plot in a stairstep model instead 
        of a connected model.

          x   : (array) - Array of X values.
          y   : (array) - Array of Y values.
          k   : (int)   - 1 if data is centered on bin (default)
                          0 if data is aligned to left side of bin
          gap : (float) - Gap in data needed to draw separate graphs
                          CURRENTLY NOT IMPLEMENTED
        """
        x = numpy.array(x, dtype=numpy.float32)
        y = numpy.array(y, dtype=numpy.float32)
        cwip.cpgbin(x, y, k)
        self.move(float(x[-1]), float(y[-1]))

    def box(self, xvars='bcnst', yvars='bcnst'):
        """
        Makes a box labeled according to LIMITS and TICKSIZE.

          xvars : x options string.
          yvars : y options string.
        """
        values = self.ticksize()
        cwip.cpgtbox(xvars, values[0], values[1], yvars, values[2], values[3])
        return

    def connect(self, x, y):
        """
        Connects (x,y) pairs with line segments.

          x : (array) - Array of X values.
          y : (array) - Array of Y values.
        """
        cwip.cpgline(numpy.array(x, dtype=numpy.float32), 
                     numpy.array(y, dtype=numpy.float32))
        self.move(x[-1], y[-1])
    
    def contour(self, image, plane, subregion=None, shade=False, label=False,
                levels=None, nlevels=5, line=True, scolor=0.2, absolute=False):
        """
        Makes a contour plot of an array read with IMAGE.

        Possible subfeatures to be expanded on:
          autolevs - 
            Sets up the contour levels automatically.
          levels - 
            Sets the contour levels for a contour plot.
          slevel - 
            Sets the type and value used to scale contour levels.
        """
        # This function needs to be expanded to support user levels and
        # possibly a more intelligent auto levels feature.
        if subregion == None:
            nx = image.axes[0]
            ny = image.axes[1]
            subregion = (1, int(nx), 1, int(ny))

        immin = image.image.min()
        immax = image.image.max()

        if absolute == True:
            immax = 1

        if levels == None:
            levels = numpy.arange(0, immax, (immax-immin)/(nlevels+1), 
                                  dtype=numpy.float32)
        else:
            levels = numpy.array(levels, dtype=numpy.float32) * immax

        contlev = numpy.array(levels, dtype=numpy.float32)

        if (shade == True):
            oldcolor = self.color
            maxcontlev = numpy.append(contlev, immax+1)
            # set color range from 50 to 125. color steps is:
            # 150-50 / levels.size
            (cmin, cmax) = cwip.cpgqcol()
            cmin = 16
            coff = (cmax - cmin) * scolor
            cmin = coff + cmin
            step = (cmax-cmin+1) / float(levels.size)
            for i in xrange(contlev.size):
                self.color = int(cmin + i*step)
                cwip.cpgconf(image.image[plane,:,:], subregion[0], 
                             subregion[1], subregion[2], subregion[3], 
                             float(maxcontlev[i]), float(maxcontlev[i+1]), 
                             self.tr)
            self.color = int(oldcolor)

        if line==True:
            cwip.cpgcont(image.image[plane,:,:], subregion[0], subregion[1], 
                         subregion[2], subregion[3], contlev, self.tr)

        if (label == True):
            self.expand=0.5
            for i in xrange(contlev.size):
                cwip.cpgconl(image.image[plane,:,:], subregion[0], 
                             subregion[1], subregion[2], subregion[3], 
                             float(contlev[i]), self.tr, "%4.2f" % contlev[i], 
                             999, 15)

    def device(self, device='/xs'):
        """
        Initializes output to a graphics device.

          device : PGPLOT device string.
        """
        # cpgldev prints out a list of available devices (sigh).

        if cwip.cpgopen(device) <= 0:
            raise IOError("Cannot open PGPLOT device.")

        # Set a variable storing the opened device name?
        cwip.cpgask(0)
        self.reset()

        # Set up local color table?
        (cx, cy) = cwip.cpgqcol()
        cx = 16
        if (cy < cx):
            cy = 0
        cwip.cpgscir(cx, cy) # Set range of possible image color indices.

    def dot(self):
        """
        Makes a point of the current style at the current location.
        """
        (cx, cy) = self.move()
        cwip.cpgpt([cx], [cy], self.pstyle)

    def draw(self, endx, endy):
        """
        Draws a line to (X,Y) from the current coordinate position.
        """
        cwip.cpgdraw(float(endx), float(endy))

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
        #cwip.wiperrorbar(int(loc), numpy.array(x, dtype=numpy.float32), 
        #                 numpy.array(y, dtype=numpy.float32), 
        #                 numpy.array(error, dtype=numpy.float32))
        
        if len(x) < 1:
            return

        cwip.cpgbbuf() # Set up buffered output.

        expsize = self.expand
        expsize = expsize / 10.0
        cwip.cpgerrb(loc, x, y, error, expsize)
        
        cwip.cpgebuf()

    def fill(self, style=None, angle=None, spacing=None, phase=None):
        """
        Sets the fill area style to N.
        """
        if style != None:
            self.fstyle = style

        if (angle != None) or (spacing != None) or (phase != None):
            (qangle, qspacing, qphase) = cwip.cpgqhs()
            if angle != None:
                qangle = angle
            if spacing != None:
                qspacing = spacing
            if phase != None:
                qphase = phase
            cwip.cpgshs(qangle, qspacing, qphase)

        (qangle, qspacing, qphase) = cwip.cpgqhs()

        return (self.fstyle, qangle, qspacing, qphase)

    def halftone(self, image, plane=0, imin=None, imax=None, subregion=None):
        """
        Produces a halftone plot of an image.
        """
        if ('mirimg' in image.__dict__.keys()):
            # this is a miriad image
            if (imin != None) or (imax != None):
                imin = float(imin)
                imax = float(imax)
            else:
                imin = float(image.image.min())
                imax = float(image.image.max())

            nx = int(image.axes[0])
            ny = int(image.axes[1])
            print nx, ny
            if subregion == None:
                subregion = (1, nx, 1, ny)
            cwip.cpgimag(image.image[plane,:,:], subregion[0], subregion[1], 
                         subregion[2], subregion[3], imin, imax, self.tr)
        else:
            #consider this a raw image
            imin = float(image.min())
            imax = float(image.max())
            nx = int(image.shape[0])
            ny = int(image.shape[1])
            cwip.cpgimag(image, 1, nx, 1, ny, imin, imax, self.tr)

    def header(self, image, xdir, ydir=None, subregion=None, noset=False):
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

        ### Time to port wipheader is now. UGH!
        # cwip.wipheader(sub[0], sub[2], sub[1], sub[3], xdir, ydir)
        # Code below is based on src/image/header.c in WIP source and
        # includes both wipheader and wipheadlim.

        # sub = cwip.wipgetsub()

        # blcx = sub[0] # px_xmin
        # trcx = sub[1] # px_xmax
        # blcy = sub[2] # px_ymin
        # trcy = sub[3] # px_ymax

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
            # For testing force size values to the following:
            blcx = 1
            trcx = image.axes[0]
            blcy = 1
            trcy = image.axes[1]
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
            blcx = 1
            trcx = image.shape[0]
            blcy = 1
            trcy = image.shape[1]

        if subregion != None:
            blcx = subregion[0]
            trcx = subregion[1]
            blcy = subregion[2]
            trcy = subregion[3]

        # Expand limits to be one half pixel larger in each direction since
        # pixels have definite sise.
        xmin = float(blcx - 0.5)
        xmax = float(trcx + 0.5)
        ymin = float(blcy - 0.5)
        ymax = float(trcy + 0.5)

        # If one of the axis is a declination axis, then set the cos factor
        # to that axis value.
        if ctypey == 'dec':
            cosdec = crvaly
        elif ctypex == 'dec':
            cosdec = crvalx
        else:
            cosdec = 0.0

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
        if noset == False:
            self.limits(xmin, xmax, ymin, ymax)
        
        # Set the transformation matrix for PGIMAG, etc.
        tr = numpy.array([xoff, xscale, 0.0, yoff, 0.0, yscale], 
                         dtype=numpy.float32)
        if noset == False:
            self.tr = tr

        return (xmin, xmax, ymin, ymax, tr)

    def hi2d(self, image, bias, slant=0, center=1, xmin=None, xmax=None,
             ymin=None, ymax=None, autolevels=True):
        """
        Draws a histogram of the data read by IMAGE.
        """
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
        if xmin == None:
            xmin = numpy.min(array)
        if xmax == None:
            xmax = numpy.max(array)
        
        cwip.cpghist(array, float(xmin), float(xmax), n, 1)

    def hls(self, k, h, l, s):
        """
        Sets the color representation using the HLS system.
        """
        cwip.cpgshls(k, h, l, s)

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
        elif (nargs == 0):
            pass
        else:
            raise ValueError("Incorrect number of arguments to limits fn.")

        if (nargs > 0):
            cwip.cpgswin(xmin, xmax, ymin, ymax) # Sets the window limits

        (xmin, xmax, ymin, ymax) = cwip.cpgqwin()
        return (xmin, xmax, ymin, ymax)

    def lookup(self, r, g, b, l, n=1):
        """
        Loads a RGB color lookup table.
        """
        cwip.cpgctab(l, r, g, b, n, 0.5)

    def move(self, *args):
        """
        Sets the current world (user) position to (x,y).

          x : (float) - X position
          y : (float) - Y position
        """
        nargs = len(args)

        if (nargs == 2):
            x = args[0]
            y = args[1]
            cwip.cpgmove(float(x), float(y))
        elif (nargs == 0):
            pass
        else:
            raise ValueError("Invalid number of arguments to move command.")

        (x, y) = cwip.cpgqpos()
        return (x, y)

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
        if (side.lower() not in ['l', 'r', 't', 'b']):
            raise ValueError("mtext side must be: l, r, t, b.")
        cwip.cpgmtxt(side, disp, coord, just, string);

    def palette(self, num, levels=0):
        """
        Sets the color palette to entry K.
        """
        pmap = {
           1 : palettes.gray,
           2 : palettes.rainbow,
           3 : palettes.heat,
           4 : palettes.iraf,
           5 : palettes.aips,
           6 : palettes.tjp,
           7 : palettes.saoA,
           8 : palettes.saoBB,
           9 : palettes.saoHE,
           10: palettes.saoI8,
           11: palettes.ds,
           12: palettes.cyclic
           }

        #cwip.wippalette(num, levels)

        if (num < 0):
            pal = -num
            contrast = -1.0
        else:
            pal = num
            contrast = 1.0

        if (pal == 0):
            (rd0, gd0, bd0) = cwip.cpgqcr(0)
            (rd1, gd1, bd1) = cwip.cpgqcr(1)
            newpal = { 
                'l' : palettes.gray['l'],
                'r' : [rd0, rd1],
                'g' : [gd0, gd1],
                'b' : [bd0, bd1]
                }
        elif pal in pmap.keys():
            newpal = pmap[pal]
        else:
            raise ValueError("Specified palette number is out of range.")

        n = len(newpal['l'])
        if (n > 0):
            if (levels == 0):
                (cmin, cmax) = cwip.cpgqcol()
                cmin = 16
                if (cmax < cmin):
                    cmax = 0
                cwip.cpgscir(cmin, cmax)
            elif (levels > 0):
                (cmin, cmax) = cwip.cpgqcir()
                cmin = 16
                cmax = cmin + levels - 1
                cwip.cpgscir(cmin, cmax)
            cwip.cpgctab(newpal['l'], newpal['r'], newpal['g'], newpal['b'], 
                         contrast, 0.5)

    def panel(self, nx, ny, k):
        """
        Sets the plot lovation to a subpanel.
        """
        # This is a straight up port from the C code. I think this can be
        # cleaned up / simplified a bit, but this *does* work properly.

        if ((nx == 0) or (ny == 0)):
            raise ValueError("CWIP.panel nx, ny values must not be 0")

        reset = False
        if ((nx != self.paneldata['oldnx']) or 
            (ny != self.paneldata['oldny'])):
            reset = True

        # Panel 1 1 K or RESET == True resets location to stored values.
        if (((nx == 1) and (ny == 1)) or (reset == True)):
            if ((self.paneldata['oldnx'] != 0) and 
                (self.paneldata['oldny'] != 0)):
                self.expand = self.paneldata['oldsize']
                self.viewport(self.paneldata['oldvx1'], 
                              self.paneldata['oldvx2'], 
                              self.paneldata['oldvy1'], 
                              self.paneldata['oldvy2'])
            self.paneldata['oldnx'] = 0
            self.paneldata['oldny'] = 0
            if (nx == 1) and (ny == 1):
                return
        self.paneldata['oldnx'] = nx
        self.paneldata['oldny'] = ny
        
        # Get parameters needed for the rest.
        chsize = self.expand
        (vx1, vx2, vy1, vy2) = self.viewport()
        (xmarg, ymarg) = self.submargin()

        # If nx/ny are negative or either is equal to 1, set a variable so
        # that adjacent sides touch (or equals the full viewport).

        if (nx < 2):
            touchx = True
        else:
            touchx = False
        if (ny < 2):
            touchy = True
        else:
            touchy = False
        nx = abs(nx)
        ny = abs(ny)

        # Panel M N K means save the old location values and set new ones.

        if ( ((nx != 1) or (ny != 1)) and (reset == True) ):
            self.paneldata['oldvx1'] = vx1
            self.paneldata['oldvx2'] = vx2
            self.paneldata['oldvy1'] = vy1
            self.paneldata['oldvy2'] = vy2
            self.paneldata['oldsize'] = chsize

        if (touchx == True):
            left = self.paneldata['oldvx1']
            right = self.paneldata['oldvx2']
        else:
            left = self.paneldata['oldvx1'] - (0.025 * xmarg * 
                                               self.paneldata['oldsize'])
            right = self.paneldata['oldvx2'] + (0.025 * xmarg * 
                                                self.paneldata['oldsize'])

        if (touchy == True):
            bottom = self.paneldata['oldvy1']
            top = self.paneldata['oldvy2']
        else:
            bottom = self.paneldata['oldvy1'] - (0.025 * ymarg * 
                                                 self.paneldata['oldsize'])
            top = self.paneldata['oldvy2'] + (0.025 * ymarg * 
                                              self.paneldata['oldsize'])

        chsize = self.paneldata['oldsize'] * numpy.power((1.0/nx/ny), 0.3333)

        deltax = (right - left) / nx
        if (touchx == True):
            offx = 0.0
        else:
            offx = 0.025 * xmarg * chsize

        deltay = (top - bottom) / ny
        if (touchy == True):
            offy = 0.0
        else:
            offy = 0.025 * ymarg * chsize

        if (k > 0):
            indx = (k - 1) % nx
            indy = (k - 1) / nx
        elif (k < 0):
            indx = (-k - 1) % nx
            indy = ny - 1 - ((-k - 1) / nx)
        else:
            indx = 0
            indy = 0

        vx1 = left + offx + (indx * deltax)
        vx2 = vx1 + deltax - (2.0 * offx)
        vy1 = bottom + offy + (indy * deltay)
        vy2 = vy1 + deltay - (2.0 * offy)
        self.expand = chsize
        self.viewport(vx1, vx2, vy1, vy2)

    def paper(self, width, aspect, units='in', px_scale=100):
        """
        Change the size of the view surface.
        """
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

        # Direct port, this routine I think can be simplified and expanded.

        cwip.cpgbbuf()

        savexp = self.expand
        saveColor = self.color
        (cmin, cmax) = cwip.cpgqcol()

        lastColor = saveColor
        defcolor = saveColor
        if ((len(color) > 0) and (color[0] >= cmin) and (c[0] <= cmax)):
            defcolor = c[0]

        for j in xrange(0, len(x)):
            if j < len(style):
                temp = style[j] + 0.001
            else:
                temp = style[0] + 0.001
            symbol = int(temp)

            expfrac = temp - symbol
            if (expfrac < 0.01):
                expfrac = 1.0
            expfrac = expfrac * savexp
            self.expand = expfrac

            if ((j < len(color)) and (c[j] >= cmin) and (c[j] <= cmax)):
                ccolor = c[j]
            else:
                ccolor = defcolor

            if (lastColor != ccolor):
                self.color = ccolor

            lastColor = ccolor

            cwip.cpgpt([x[j]], [y[j]], symbol)

        self.move(x[-1], y[-1])
        self.expand = savexp
        if (lastColor != saveColor):
            self.color = saveColor

        cwip.cpgebuf()
        
    def poly(self, x, y):
        """
        Draws a polygon.
        """
        cwip.cpgpoly(x, y)
        self.move(x[0], y[0])

    def putlabel(self, string, just=0.5):
        """
        Writes justified text STR at the current location.

          string : (string) - String value to write on screen.
          just   : (float)  - Justification between 0,1. 0.5 is centered
        """
        (x, y) = self.move()
        
        # get angle
        angle = self.angle
        cwip.cpgptxt(x, y, angle, just, string)

        # Move the current position to the end point of the label
        (nx, ny) = cwip.cpglen(4, string)
        angle = angle * rpdeg
        nx = nx * (1 - just)
        ny = ny * (1 - just)
        
        x2 = x + (nx * numpy.cos(angle))
        y2 = y + (ny * numpy.sin(angle))

        self.move(x2, y2)

    def rect(self, xmin, xmax, ymin, ymax):
        """
        Draw a rectangle, using fill-area attributes.
        """
        cwip.cpgrect(xmin, xmax, ymin, ymax)

    def rgb(self, k, r, g, b):
        """
        Sets the color represenation using the RGB system.
        """
        cwip.cpgscr(k, r, g, b)

    def submargin(self, xsubmar=None, ysubmar=None):
        """
        Sets the gap between individual panels.
        
        Defaults, xsub, ysub = 2.0
        """
        if xsubmar != None:
            self.xsubmar = xsubmar
        if ysubmar != None:
            self.ysubmar = ysubmar

        return (self.xsubmar, self.ysubmar)

    def symbol(self, value):
        """
        Sets the current point symbol to N.
        """
        self.pstyle = value

    def ticksize(self, xtick=None, nxsub=None, ytick=None, nysub=None):
        """
        Sets tick intervals for the BOX command.
        
        Convenience function for quickly accessing and retrieving 
        xtick, nxsub, ytick, and nysub
        """
        if xtick != None:
            self.xtick = xtick
        if ytick != None:
            self.ytick = ytick
        if nxsub != None:
            self.nxsub = nxsub
        if nysub != None:
            self.nysub = nysub

        return (self.xtick, self.nxsub, self.ytick, self.nysub)

    def vector(self, x, y, length, direction, angle=45.0, vent=0.3):
        """
        Draws a vector field as a sequence of arrows.
        """
        if isinstance(x, numpy.ndarray) == False:
            x = numpy.array(x, dtype=numpy.float32)
        if isinstance(y, numpy.ndarray) == False:
            y = numpy.array(y, dtype=numpy.float32)
        if isinstance(length, numpy.ndarray) == False:
            length = numpy.array(length, dtype=numpy.float32)
        if isinstance(direction, numpy.ndarray) == False:
            direction = numpy.array(direction, dtype=numpy.float32)

        nx = x.size
        ny = y.size
        nl = length.size
        nd = direction.size

        if ((nx != ny) or (nx != nl) or (nx != nd)):
            raise ValueError("Length of x, y, length, and direction arrays must be equal")

        fill = self.fstyle
        
        cwip.cpgbbuf()
        cwip.cpgsah(int(fill), angle, vent)
        
        for i in xrange(0, nx):
            # x1 = x[i]
            # y2 = y[i]
            x2 = x[i] + (length[i] * numpy.cos(direction[i] * rpdeg))
            y2 = y[i] + (length[i] * numpy.sin(direction[i] * rpdeg))
            cwip.cpgarro(float(x[i]), float(y[i]), float(x2), float(y2))

        cwip.cpgebuf()
        
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

    def viewport(self, *args):
        """
        Sets the physical location of the plot.
        """
        nargs = len(args)
        
        if (nargs == 4):
            xmin = args[0]
            xmax = args[1]
            ymin = args[2]
            ymax = args[3]

            if (xmin < 0) or (xmin > 1):
                raise ValueError("Viewport values must be between 0 and 1")
            if (xmax < 0) or (xmax > 1):
                raise ValueError("Viewport values must be between 0 and 1")
            if (ymin < 0) or (ymin > 1):
                raise ValueError("Viewport values must be between 0 and 1")
            if (ymax < 0) or (ymax > 1):
                raise ValueError("Viewport values must be between 0 and 1")

            cwip.cpgsvp(float(xmin), float(xmax), float(ymin), float(ymax))
        elif (nargs == 0):
            pass
        else:
            raise ValueError("Incorrect number of arguments to viewport fn.")

        (xmin, xmax, ymin, ymax) = cwip.cpgqvp(0)
        return (xmin, xmax, ymin, ymax)

    def vstand(self):
        """
        Sets the standard (default) viewport.
        """
        cwip.cpgvstd()

    def wedge(self, cside, disp, thick, min, max, boxarg='bcst'):
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
        min = float(min)
        max = float(max)
        cside = cside.lower()

        # if ('p' in cside):
        #    cpg = True
        # else:
        #    cpg = False
        cside = cside.replace('p', '')

        #if cpg == True:
        #    cwip.cpgwedg(cside+'I', disp, thick, min, max, boxarg)
        #    return

        if ('r' in cside) or ('t' in cside):
            boxarg += 'm'
        elif ('l' in cside) or ('b' in cside):
            boxarg += 'n'

        # Directly ported wipPwedge below

        txtfrc = 0.6
        txtsep = 2.2
        wdgpix = 100
        tr = [0.0, 1.0, 0.0, 0.0, 0.0, 1.0]

        NONE = 0
        LEFT = 1
        RIGHT = 2
        TOP = 3
        BOTTOM = 4

        side = None
        image = True

        if ('t' in cside):
            side = TOP
        elif ('l' in cside):
            side = LEFT
        elif ('r' in cside):
            side = RIGHT
        elif ('b' in cside):
            side = BOTTOM
        elif ('i' in cside):
            image = True
        elif ('g' in cside):
            image = False

        if side == None:
            raise ValueError("No valid side.")
        
        if ((side == BOTTOM) or (side == TOP)):
            horiz = True
        else:
            horiz = False

        # Store the current world and viewport coords and the character height.
        cwip.cpgbbuf()
        (wxa, wxb, wya, wyb) = self.limits()
        (xa, xb, ya, yb) = self.viewport()
        oldch = self.expand

        # Determine the unit character height in NDC coords.
        self.expand = 1.0
        (xch, ych) = cwip.cpgqcs(0)
        if horiz == True:
            ndcsize = ych
        else:
            ndcsize = xch

        # Convert 'WIDTH' and 'DISP' into viewport units.
        vwidth = thick * ndcsize * oldch
        vdisp = disp * ndcsize * oldch

        # Determine and set the character height required to fit the wedge
        # annotation text within the area allowed for it.
        newch = txtfrc * vwidth / (txtsep * ndcsize)
        self.expand = newch

        # Determine the width of the wedge part of the plot minus the 
        # annotation. (NDC Units)
        wedwid = vwidth * (1.0 - txtfrc)

        # Determine the viewport coordinates for the wedge + annotation.
        vxa = xa
        vxb = xb
        vya = ya
        vyb = yb
        if side == TOP:
            vya = yb + vdisp
            vyb = vya + wedwid
        elif side == LEFT:
            vxb = xa - vdisp
            vxa = vxb - wedwid
        elif side == RIGHT:
            vxa = xb + vdisp
            vxb = vxa + wedwid
        elif side == BOTTOM:
            vyb = ya - vdisp
            vya = vyb - wedwid

        # Set the viewport for the wedge
        self.viewport(vxa, vxb, vya, vyb)
        if (min > max):
            fg1 = min
        else:
            fg1 = max
        if (min < max):
            bg1 = min
        else:
            bg1 = max

        # Create the dummy wedge array to be plotted.
        wdginc = (fg1 - bg1) / (wdgpix - 1)
        if horiz == True:
            wedgeArray = numpy.zeros((wdgpix,1), dtype=numpy.float32)
            for i in xrange(wdgpix):
                wedgeArray[i,0] = bg1 + (i * wdginc)
        else:
            wedgeArray = numpy.zeros((1,wdgpix), dtype=numpy.float32)
            for i in xrange(wdgpix):
                wedgeArray[0,i] = bg1 + (i * wdginc)
    
        (xtick, nxtick, ytick, nytick) = self.ticksize()

        if '0' in boxarg:
            otherLabel = "0"
            boxarg = '0'
        else:
            otherLabel = "BC"

        wlabel = boxarg

        # Draw the wedge then change the world coordinates for labelling.
        # Also, draw a labelled frame around the wedge.
        if (horiz == True):
            self.limits(1.0, float(wdgpix), 0.9, 1.1)
            if (image == True):
                cwip.cpgimag(wedgeArray, 1, wdgpix, 1, 1, min, max, tr)
            else:
                cwip.cpggray(wedgeArray, 1, wdgpix, 1, 1, min, max, tr)
            self.limits(bg1, fg1, 0.0, 1.0)
            cwip.cpgtbox(wlabel, xtick, nxtick, otherLabel, 0.0, 0)
        else:
            self.limits(0.9, 1.1, 1.0, float(wdgpix))
            if (image == True):
                cwip.cpgimag(wedgeArray, 1, 1, 1, wdgpix, min, max, tr)
            else:
                cwip.cpggray(wedgeArray, 1, 1, 1, wdgpix, min, max, tr)
            self.limits(0.0, 1.0, bg1, fg1)
            cwip.cpgtbox(otherLabel, 0.0, 0,wlabel, ytick, nytick)
            
        # Reset the original viewport and world coordinates.
        self.viewport(xa, xb, ya, yb)
        self.limits(wxa, wxb, wya, wyb)
        self.expand = oldch
        cwip.cpgebuf()
        return
