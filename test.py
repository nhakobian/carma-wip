#! /usr/bin/python -i

import pynwip
import numpy

a = pynwip.wip()
a.device()

x = (numpy.array(range(100)) / 10.0) - 5.0
y = numpy.sin(x)

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
a.box()
a.panel(2, 2, -4)
a.box()

a.panel(1, 1, 1)
a.mtext('T', 3, 0.5, 0.5, "Sample multipanel plot.")
