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
INC = -I./src/include
HELP = \"wiphelp.dat\"
OBJ = $(SRC:.c=.o)

#Only use -Wl,-rpath on Linux, not on OS X.
UNAME := $(shell uname)
ifeq ($(UNAME), Linux)
  RPATH = -Wl,-rpath,$(MIRLIB)
endif
ifeq ($(UNAME), Darwin)
  #OS X miriad may not build shared pgplot packages.
  RPATH = -lgfortran -lX11 -lcurses
endif

all: wip

.c.o :
	$(CC) $(OPTS) $(CFLAGS) $(INC) -DHELPFILE=$(HELP) -c $< -o $*.o

wip: $(OBJ) 
	$(CC) $(CFLAGS) $(INC) -o wip $(SRC_MAIN) -L$(MIRLIB) \
	   $(RPATH) $(OBJ) \
	   -L/usr/X11R6/lib -lcpgplot -lpgplot -lreadline

clean:
	rm -f *.o wip
	rm -f src/*/*.o
	rm -f .wiphistory
