# Updated makefile to make it more readable.

SRC_DRIVERS   = basic.c fits.c miriad.c
SRC_IMAGES    = image.c
SRC_PLOT      = aitoff.c array.c histo.c \
	        imval.c inquire.c matrix.c move.c palette.c panel.c \
	        points.c reset.c scale.c set.c show.c wedge.c
SRC_SYSDEP    = filesize.c inoutput.c unpack.c
SRC_VARIABLES = evaluate.c var.c vectors.c parse.c

SRC1  =	$(addprefix drivers/, $(SRC_DRIVERS)) \
	$(addprefix images/, $(SRC_IMAGES)) \
	$(addprefix plot/, $(SRC_PLOT)) \
	$(addprefix sysdep/, $(SRC_SYSDEP)) \
	$(addprefix variables/, $(SRC_VARIABLES))
SRC = $(addprefix src/, $(SRC1))

CC = gcc
OPTS = -ansi -Dlinux -fpic -DREADLINE
CFLAGS = -g 
CCMALLOC = -lccmalloc 
INC = -I./src/include -I$(MIRINC)/../pgplot-miriad-remix
HELP = \"wiphelp.dat\"
OBJ = $(SRC:.c=.o)

all: pynwip

.c.o :
	$(CC) $(OPTS) $(CFLAGS) $(INC) -DHELPFILE=$(HELP) -c $< -o $*.o

libwip: $(OBJ)
	$(CC) $(CFLAGS) -shared -Wl,-soname,libwip.so -o libwip.so \
	   $(OBJ) -lcpgplot -lpgplot -lreadline -L$(MIRLIB) \
	   -Wl,-rpath,$(MIRLIB)

pynwip: libwip
	cd pynwip; /usr/bin/swig -python _cwip.i
	$(CC) $(OPTS) $(CFLAGS) -c pynwip/_cwip_wrap.c \
	   -o pynwip/_cwip_wrap.o -I/usr/include/python2.7 $(INC)
	ld -rpath $(MIRLIB) -rpath $(CURDIR) -L$(CURDIR) -L$(MIRLIB) -lwip \
	   -shared -o pynwip/_cwip.so pynwip/_cwip_wrap.o

clean:
	rm -f libwip.so *.o wip
	rm -f src/*/*.o
	rm -f pynwip/cwip.py pynwip/cwip.pyc pynwip/_cwip.so \
	   pynwip/_cwip_wrap.c pynwip/_cwip_wrap.o
	rm -f pynwip/*.pyc
	rm -f .wiphistory
