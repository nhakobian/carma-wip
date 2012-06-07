# Updated makefile to make it more readable.

SRC_MAIN      = src/branch/wipmain.c
SRC_BRANCH    = execute.c process.c wipinit.c
SRC_DRIVERS   = basic.c fits.c miriad.c
SRC_FIT       = fit.c gaussfit.c lsqfit.c medfit.c polyfit.c
SRC_IMAGES    = extrema.c header.c heq.c image.c smooth.c
SRC_INTERACT  = command.c decode.c help.c ifxecute.c insert.c interpret.c \
	        list.c loopxecute.c macros.c maxecute.c parse.c readinput.c
SRC_PLOT      = aitoff.c arc.c array.c arrow.c cursor.c device.c histo.c \
	        imval.c inquire.c levels.c matrix.c move.c palette.c panel.c \
	        phard.c points.c putlab.c quarter.c reset.c scale.c set.c \
	        show.c wedge.c
SRC_SYSDEP    = filesize.c inoutput.c random.c readata.c spool.c unpack.c
SRC_VARIABLES = evaluate.c find.c pushpop.c str.c var.c vectors.c

SRC1  = $(addprefix branch/, $(SRC_BRANCH)) \
	$(addprefix drivers/, $(SRC_DRIVERS)) \
	$(addprefix fit/, $(SRC_FIT)) \
	$(addprefix images/, $(SRC_IMAGES)) \
	$(addprefix interact/, $(SRC_INTERACT)) \
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

all: wip

.c.o :
	$(CC) $(OPTS) $(CFLAGS) $(INC) -DHELPFILE=$(HELP) -c $< -o $*.o

libwip: $(OBJ)
	$(CC) $(CFLAGS) -shared -Wl,-soname,libwip.so -o libwip.so \
	   $(OBJ) -lcpgplot -lpgplot -lreadline -L$(MIRLIB) \
	   -Wl,-rpath,$(MIRLIB)

wip: libwip
	$(CC) $(CFLAGS) $(INC) -o wip $(SRC_MAIN) -L$(MIRLIB) \
	   -Wl,-rpath,$(MIRLIB) -Wl,-rpath,$(CURDIR) -L. \
	   -L/usr/X11R6/lib -lcpgplot -lpgplot \
	   -lreadline -lwip

pwip: $(OBJ)
	cd pWip; /usr/bin/swig -python wip.i
	$(CC) $(OPTS) $(CFLAGS) -c pWip/wip_wrap.c -o pWip/wip_wrap.o -I/usr/include/python2.7 $(INC)
	ld -rpath $(MIRLIB) -L$(MIRLIB) -lreadline -lcpgplot -lpgplot -shared -o pWip/_wip.so $(OBJ) pWip/wip_wrap.o

clean:
	rm -f libwip.so *.o wip
	rm -f src/*/*.o
	rm -f pWip/wip.py pWip/wip.pyc pWip/_wip.so pWip/wip_wrap.c \
	   pWip/wip_wrap.o
	rm -f .wiphistory

