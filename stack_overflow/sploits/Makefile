# tools
CC := gcc
LD := $(CC)
RM := rm -f
CP := cp

# flags
CFLAGS := -ggdb
LDFLAGS := $(CFLAGS)
LDLIBS :=

# sources
sources := sploit1.c sploit2.c sploit3.c sploit4.c
targets := $(sources:.c=)

# gmake magic
.PHONY: default all clean

# targets
default: all
all: $(targets)

clean:
	$(RM) $(targets) $(sources:.c=.o)

# dependencies
$(sources:.c=.o): shellcode.h
