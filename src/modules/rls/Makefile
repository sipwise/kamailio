#
# rls: Resource List Server
#
#
# WARNING: do not run this directly, it should be run by the main Makefile

include ../../Makefile.defs
auto_gen=
NAME=rls.so

ifeq ($(CROSS_COMPILE),)
XML2CFG=$(shell which xml2-config)
ifeq ($(XML2CFG),)
XML2CFG=$(shell \
	if pkg-config --exists libxml-2.0; then \
		echo 'pkg-config libxml-2.0'; \
	fi)
endif
ifeq ($(OS), darwin)
ICU_BUILDER = $(shell \
	if pkg-config --exists icu-uc; then \
		echo 'pkg-config icu-uc'; \
	fi)
endif
endif

ifneq ($(XML2CFG),)
	DEFS += $(shell $(XML2CFG) --cflags )
	LIBS += $(shell $(XML2CFG) --libs)
else
	DEFS+=-I$(LOCALBASE)/include/libxml2 \
		-I$(LOCALBASE)/include
	LIBS+=-L$(LOCALBASE)/lib -lxml2
endif

ifneq ($(ICU_BUILDER),)
	DEFS += $(shell $(ICU_BUILDER) --cflags )
	LIBS += $(shell $(ICU_BUILDER) --libs)
endif

include ../../Makefile.modules
