#! /usr/bin/python -i

import pynwip
import numpy
import miriad_tools

a = pynwip.wip()
a.device()
a.paper(750, 0.9, units='px')

x = (numpy.array(range(100)) / 10.0) - 5.0
y = numpy.sin(x)

#a.winadj(0, 3, 0, 3)
#a.viewport(0.2, 0.8, 0.2, 0.8)

a.panel(-3, 3, -1)
a.limits(x, y)
a.points(x, y)
a.connect(x, y)
a.box()
a.mtext('T', 1.5, 0.5, 0.5, "Sample sin(x) plot.")
a.mtext('L', 2.0, 0.5, 0.5, "sin(x)")
a.mtext('B', 2.3, 0.5, 0.5, "x")

a.panel(-3, 3, -2)
a.limits(x, y)
a.bin(x[::2], y[::2])
a.box(yvars='bcst')
a.mtext('T', 1.5, 0.5, 0.5, "Sample sin(x) plot.")
a.mtext('B', 2.3, 0.5, 0.5, "x")

#a.submargin(1, 1)

a.panel(3, 3, -3)
a.limits(-1.1, 1.1, -1.1, 1.1)
a.ticksize(1,1,1,1)
a.box()
a.ticksize(0,0,0,0)
a.move(-1, -0.4)
a.angle = 45
a.putlabel("Angle test", 0)
a.angle = 0
a.move(-1, -0.5)
a.putlabel("Label test", 0)
a.move(1, 0.5)
a.putlabel("Move test", 1)
a.move(-0.75, 0.5)
a.arc(0.1, 0.3)
a.move(-0.55, 0.5)
a.arc(0.3, 0.1, 45)
a.move(-0.35, 0.5)
a.arc(0.2, 0.2, start=90, extent=180)

a.move(0.5, -0.5)
a.putlabel("Reg sized text", 0)
a.expand=a.expand*2
a.move(0.5, -0.75)
a.putlabel("Big sized text", 0)
a.expand=a.expand/2.

a.move(0, -0.6)
a.fill(3, spacing=0.5)
a.arc(0.3, 0.3)
a.fill(1)

qx = numpy.array([-0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75], dtype=numpy.float32)
qy = numpy.array([-0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75], dtype=numpy.float32)
a.points(qx, qy, style=[16])
a.expand=2
a.errorbar(qx, qy, numpy.array([.1, 0, 0, 0, 0, 0, 0], dtype=numpy.float32), 1)
a.errorbar(qx, qy, numpy.array([0, .1, 0, 0, 0, 0, 0], dtype=numpy.float32), 2)
a.errorbar(qx, qy, numpy.array([0, 0, .1, 0, 0, 0, 0], dtype=numpy.float32), 3)
a.errorbar(qx, qy, numpy.array([0, 0, 0, .1, 0, 0, 0], dtype=numpy.float32), 4)
a.errorbar(qx, qy, numpy.array([0, 0, 0, 0, .1, 0, 0], dtype=numpy.float32), 5)
a.errorbar(qx, qy, numpy.array([0, 0, 0, 0, 0, .1, 0], dtype=numpy.float32), 6)
a.errorbar(qx, qy, numpy.array([0, 0, 0, 0, 0, 0, .1], dtype=numpy.float32), 5)
a.errorbar(qx, qy, numpy.array([0, 0, 0, 0, 0, 0, .1], dtype=numpy.float32), 6)
a.expand=1

a.panel(3, 3, -4)
#a.itf=2
a.palette(2)
img = miriad_tools.MirImage('test.image')
a.winadj(0, img.axes[0], 0, img.axes[1])
a.header(img, 'rd', 'rd')
#a.itf=1
a.halftone(img)
a.box('bcstznh', 'bcstznvd')
a.wedge('r', 1., 3., img.image.min(), img.image.max())
a.wedge('bp', 2., 3., img.image.min(), img.image.max(), boxarg='0')

a.panel(3, 3, -5)
a.limits(0, 5, 0, 5)
a.box()
a.move(0.5, 4)
a.arrow(1, 1, 90, 0)
a.move(1, 4)
a.expand=1.25
a.lstyle=2
a.arrow(1.5, 1, 45, 0)
a.lstyle=1
print a.lstyle
print a.lwidth
a.expand=1

a.move(2,2)
a.dot()
a.symbol(14)
a.move(2.2,2)
a.dot()

a.move(0.5, 0.5)
a.draw(2, 4)

a.move(3, 4)
a.bgci=3
a.putlabel("bgci test", 0.5)
a.bgci=0

a.expand=0.7
a.move(4, 4.5)
a.font=1
a.putlabel("font1", 0)
a.move(4, 4)
a.font=2
a.color=4
a.putlabel("font2", 0)
a.color=1
a.move(4, 3.5)
a.font=3
a.color=5
a.putlabel("font3", 0)
a.color=1
a.move(4, 3)
a.font=4
a.putlabel("font4", 0)
a.font=1
a.expand=1

a.fill(3)
a.rect(2.5, 4.5, 0.5, 1.5)
a.fill(2)
a.rect(2.5, 4.5, 0.5, 1.5)
a.fill(1)

a.panel(3, 3, -6)
a.globe()

a.panel(3, 3, -7)
a.limits(img.image.min(), img.image.max()/4., 0, img.image.size/4.)
a.histogram(img.image.flatten(), n=100)
a.box()

a.panel(1, 1, 1)
a.mtext('T', 3, 0.5, 0.5, "Sample multipanel plot.")

a.viewport(0.32, 0.42, 0.125, 0.2)
a.winadj(0, 1, 0, 1)
a.lwidth=5
a.box('bc', 'bc')
a.lwidth=1
a.mtext('B', 1, 0.5, 0.5, "Viewport test")

print a.tr
