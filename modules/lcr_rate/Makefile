include ../../Makefile.defs
auto_gen=
NAME=lcr_rate.so

DEFS+=-DKAMAILIO_MOD_INTERFACE -D_GNU_SOURCE
DEFS+=$(shell mysql_config --cflags)
LIBS+=-lswrate

include ../../Makefile.modules
