# tools
CC := i686-linux-gnu-gcc
LD := $(CC)
RM := rm -f
CP := cp

# flags
CFLAGS := -ggdb -fno-stack-protector -z execstack -fno-pie -no-pie -mpreferred-stack-boundary=2 -static
LDFLAGS := $(CFLAGS)
LDLIBS :=

# sources
sources := target1.c target2.c target3.c target4.c
targets := $(sources:.c=)

# gmake magic
.PHONY: default all clean

# targets
default: all
all: $(targets)

install: $(targets)
	-$(RM) /tmp/target?
	$(CP) $(targets) /tmp

uninstall:
	-$(RM) /tmp/target?

setuid: install
ifeq ($(shell id -u),0)
	chown root:root /tmp/target?
	chmod 4755 /tmp/target?
else
	@echo "'make setuid' must be run as root -- use sudo or a root login!"
endif

clean:
	$(RM) $(targets) $(sources:.c=.o)
