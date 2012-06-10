#! /usr/bin/python -i

import pynwip
import numpy

a = pynwip.wip()
a.device()

x = (numpy.array(range(100)) / 10.0) - 5.0
y = numpy.sin(x)
a.limits(x, y)
a.bin(x, y)
a.points(x, y/2.)
a.connect(x, y/2.)
a.box()
a.mtext('T', 1.5, 0.5, 0.5, "Sample sin(x) plot.")
a.mtext('L', 2.0, 0.5, 0.5, "sin(x)")
a.mtext('B', 2.3, 0.5, 0.5, "x")

#a.xlabel('x')
#a.ylabel('sin(x)')
