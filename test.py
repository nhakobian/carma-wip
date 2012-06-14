#! /usr/bin/python -i

import pynwip
import numpy
import miriad_tools

a = pynwip.wip()
a.device()
#a.rgb(0, 1, 1, 1)
#a.rgb(1, 0, 0, 0)

a.paper(750, 0.9, units='px')

a.vstand()

x = (numpy.array(range(100)) / 10.0) - 5.0
y = numpy.sin(x)

#a.winadj(0, 3, 0, 3)
#a.viewport(0.2, 0.8, 0.2, 0.8)

a.panel(3, 3, -1)
a.limits(x, y)
a.points(x[::3], y[::3], style=[12])
a.connect(x, y)
a.box()
a.mtext('T', 1.5, 0.5, 0.5, "Sample sin(x) plot.")
a.mtext('L', 2.0, 0.5, 0.5, "sin(x)")
a.mtext('B', 2.3, 0.5, 0.5, "x")
a.bin(x[::2], y[::2]/2.)

#a.submargin(1, 1)

a.panel(3, 3, -2)
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
a.hls(1, 0.75, 0.5, 0.5)
a.arc(0.1, 0.3)
a.rgb(1, 1, 1, 1)
a.move(-0.55, 0.5)
a.arc(0.3, 0.1, 45)
a.move(-0.35, 0.5)
a.arc(0.2, 0.2, start=90, extent=180)

a.move(1, -0.5)
a.putlabel("Reg sized text", 1)
a.expand=a.expand*2
a.move(1, -0.95)
a.putlabel("Big sized text", 1)
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

a.panel(3, 3, -3)
#a.itf=2
#a.palette(2)
r = [0.9, 0.6, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 1.0]
g = [0.9, 0.6, 0.2, 0.4, 0.6, 0.2, 0.4, 0.6, 0.2, 0.6, 1.0]
b = [0.9, 0.6, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 1.0]
l = [0.0, 0.1, 0.11, 0.15, 0.18, 0.22, 0.35, 0.45, 0.55, 0.90, 1.0]
a.lookup(r, g, b, l)

img = miriad_tools.MirImage('test.image')
a.winadj(0, img.axes[0], 0, img.axes[1])
(xmin, xmax, ymin, ymax) = a.header(img, 'rd', 'rd', ret=True)
#a.itf=1
a.halftone(img)
print xmax, ymin
a.move((xmax+xmin)/2., (ymin+ymax)/2.)
a.beam(10, 20, 45, 2.5, -2.5, bgrect=-1)
a.box('bcstznh', 'bcstznvd')
a.wedge('r', 1., 3., img.image.min(), img.image.max())
a.wedge('bp', 2., 3., img.image.min(), img.image.max(), boxarg='0')

a.panel(3, 3, -4)
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

a.panel(3, 3, -5)
a.globe()

a.panel(3, 3, -6)
a.limits(img.image.min(), img.image.max()/4., 0, img.image.size/4.)
a.histogram(img.image.flatten(), n=100)
a.box()

a.panel(3, 3, -7)
#a.limits(80, 160, -.1, 1.1)
a.hi2d(img, .1, ymin=125, ymax=140)
a.box()

a.panel(1, 1, 1)
a.mtext('T', 3, 0.5, 0.5, "Sample multipanel plot.")

a.panel(3, 3, -8)
a.limits(-6, 6, -5, 5)
px = [1.5 , 2   , 1, 2.25, 3, 3.75, 5, 4,     4.5,   3 , 1.5]
py = [1   , 2.25, 3, 3,    4,    3, 3, 2.25,    1, 1.75, 1]
a.fill(2)
a.rgb(1, 1, 0.25, 0.25)
a.poly(px, py)
a.fill(4)
a.poly(px, py)
a.rgb(1, 1, 1, 1)
x = [-5, -4, -3, -2, -1]
y = [3, 4, 1, 2, 4]
a.fill(1)
a.bar(x, y, [2, 3, 4, 5, 6], 2, 0, 0.7)
a.fill(0)
a.bar(x, y, [], 2, 0, 0.7)
a.box('an', 'an')

x = [-5, -4, -3, -2, -1, -5, -4, -3, -2, -1, -5, -4, -3, -2, -1, -5, -4, -3,
      -2, -1, -5, -4, -3, -2, -1]
y = [-1, -1, -1, -1, -1, -2, -2, -2, -2, -2, -3, -3, -3, -3, -3, -4, -4, -4, 
      -4, -4, -5, -5, -5, -5, -5]
r = [ 0.6, 0.6, 0.6, 0.6, 0.6, 0.8, 0.8, 0.8, 0.8, 0.8, 1.0, 1.0, 1.0, 1.0, 
      1.0, 1.2, 1.2, 1.2, 1.2, 1.2, 1.4, 1.4, 1.4, 1.4, 1.4]
p = [ 0, 15, 30, 45, 60, 5, 20, 35, 50, 65, 10, 25, 40, 55, 70, 15, 30, 45, 60,
      75, 20, 35, 50, 65, 80]
a.vector(x, y, r, p, 0, 0)

a.viewport(0.8, 0.9, 0.5, 0.6)
a.winadj(0, 1, 0, 1)
a.lwidth=5
a.box('bc', 'bc')
a.lwidth=1
a.mtext('B', 1, 0.5, 0.5, "Viewport test")

print a.tr
