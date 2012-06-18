CC = gcc
OPTS = -ansi -Dlinux -fpic
CFLAGS =
INC = -I$(MIRINC)/../pgplot-miriad-remix

all: pyn

pyn:
	cd pynwip; /usr/bin/swig -python _cwip.i
	$(CC) $(OPTS) $(CFLAGS) -c pynwip/_cwip_wrap.c \
	   -o pynwip/_cwip_wrap.o -I/usr/include/python2.7 $(INC)
	ld -rpath $(MIRLIB) -rpath $(CURDIR) -L$(CURDIR) -L$(MIRLIB) \
	   -lpgplot -lcpgplot -shared -o pynwip/_cwip.so pynwip/_cwip_wrap.o

clean:
	rm -f pynwip/cwip.py pynwip/cwip.pyc pynwip/_cwip.so \
	   pynwip/_cwip_wrap.c pynwip/_cwip_wrap.o
	rm -f pynwip/*.pyc
