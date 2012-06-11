#! /usr/bin/python -i

import pynwip
import numpy
import miriad_tools

a = pynwip.wip()
a.device()
a.paper(750, 1/1.5, units='px')

x = (numpy.array(range(100)) / 10.0) - 5.0
y = numpy.sin(x)

#a.winadj(0, 3, 0, 2)
#a.viewport(0.2, 0.8, 0.2, 0.8)

a.panel(-2, 2, -1)
a.limits(x, y)
a.points(x, y)
a.connect(x, y)
a.box()
a.mtext('T', 1.5, 0.5, 0.5, "Sample sin(x) plot.")
a.mtext('L', 2.0, 0.5, 0.5, "sin(x)")
a.mtext('B', 2.3, 0.5, 0.5, "x")

a.panel(-2, 2, -2)
a.limits(x, y)
a.bin(x[::2], y[::2])
a.box(yvars='bcst')
a.mtext('T', 1.5, 0.5, 0.5, "Sample sin(x) plot.")
a.mtext('B', 2.3, 0.5, 0.5, "x")

a.panel(2, 2, -3)
a.limits(-1.1, 1.1, -1.1, 1.1)
a.box()
a.move(-1, -0.5)
a.putlabel("Label test", 0)
a.move(1, 0.5)
a.putlabel("Move test", 1)

qx = numpy.array([-0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75], dtype=numpy.float32)
qy = numpy.array([-0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75], dtype=numpy.float32)
a.points(qx, qy, style=[16])
a.errorbar(qx, qy, numpy.array([.1, 0, 0, 0, 0, 0, 0], dtype=numpy.float32), 1)
a.errorbar(qx, qy, numpy.array([0, .1, 0, 0, 0, 0, 0], dtype=numpy.float32), 2)
a.errorbar(qx, qy, numpy.array([0, 0, .1, 0, 0, 0, 0], dtype=numpy.float32), 3)
a.errorbar(qx, qy, numpy.array([0, 0, 0, .1, 0, 0, 0], dtype=numpy.float32), 4)
a.errorbar(qx, qy, numpy.array([0, 0, 0, 0, .1, 0, 0], dtype=numpy.float32), 5)
a.errorbar(qx, qy, numpy.array([0, 0, 0, 0, 0, .1, 0], dtype=numpy.float32), 6)
a.errorbar(qx, qy, numpy.array([0, 0, 0, 0, 0, 0, .1], dtype=numpy.float32), 5)
a.errorbar(qx, qy, numpy.array([0, 0, 0, 0, 0, 0, .1], dtype=numpy.float32), 6)

a.panel(2, 2, -4)
img = miriad_tools.MirImage('test.image')
a.winadj(0, img.axes[0], 0, img.axes[1])
a.header(img, 'rd', 'rd')
a.halftone(img)
a.box('bcstznh', 'bcstznvd')

a.panel(1, 1, 1)
a.mtext('T', 3, 0.5, 0.5, "Sample multipanel plot.")

a.viewport(0.3, 0.4, 0.15, 0.25)
a.winadj(0, 1, 0, 1)
a.box('bc', 'bc')
a.mtext('B', 1, 0.5, 0.5, "Viewport test")

print a.tr
