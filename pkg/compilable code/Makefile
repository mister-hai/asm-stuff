#for GNU make
FILES = LICENSE.txt \
	CHANGE-LOG.txt \
	readme.html \
	readme-jp.html

DC_FILES = LICENSE.txt \
	Makefile \
	mainpage.txt \
	tinymt32dc.0.20.txt \
	tinymt64dc.0.20.txt \
	doxygen.cfg \
	output.hpp \
	tinymt32dc.cpp \
	tinymt64dc.cpp \
	parse_opt.cpp \
	tinymt32search.hpp \
	tinymt64search.hpp \
	getid.cpp \
	parse_opt.h

.PHONY : zip
zip: $(FILES)
	mkdir ${DIR}
	cp ${FILES} ${DIR}
	mkdir ${DIR}/dc
	mkdir ${DIR}/dc/include
	mkdir ${DIR}/dc/src
	(cd dc; cp -r include ../${DIR}/dc)
	(cd dc/src; cp ${DC_FILES} ../../${DIR}/dc/src)
	mkdir ${DIR}/tinymt
	(cd tinymt; cp ${TINYMT_FILES} ../${DIR}/tinymt)
	zip -r ${DIR}.zip ${DIR}/*
	rm -rf ${DIR}

#DDEBUG = -O0 -g -ggdb -DDEBUG=1
CCOPTION = -I. -Wall -Wextra -O3 -std=c99 -Wmissing-prototypes $(DDEBUG)
CC = gcc
#CC = icc
#CC = clang
CC = gcc -Wall -Wextra -Wsign-compare -Wconversion -Wmissing-prototypes \
-O3 -std=c99 $(DDEBUG)
#CC = icc -Wall -O3 -std=c99 -Wmissing-prototypes $(DDEBUG)

all: test_xsadd doc check32 check64

check32:  check32.c tinymt32.o
	${CC} -o $@  check32.c tinymt32.o ${LINKOPT}

check64:  check64.c tinymt64.o
	${CC} -o $@  check64.c tinymt64.o ${LINKOPT}

test_xsadd:  test_xsadd.c xsadd.o
	${CC} ${CCOPTION} -o $@  test_xsadd.c xsadd.o

doc:xsadd.h doxygen.cfg tinymt32.c tinymt64.c tinymt32.h tinymt64.h mainpage.txt
	doxygen doxygen.cfg

xsadd.c: xsadd.h

#.c.o:
#	${CC} -c $<

.c.o:
	${CC} ${CCOPTION} -c $<

clean:
	rm -rf *.o *~ *.dSYM html test_xsadd
