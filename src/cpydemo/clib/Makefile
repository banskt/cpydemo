CC := gcc 
CP := g++ 
LIBFLAGS := -L${MKLROOT}/lib/intel64 -Wl,--no-as-needed -lmkl_intel_ilp64 -lmkl_sequential -lmkl_core -lpthread -lm -ldl -std=c99
INCLUDEFLAGS := -DMKL_ILP64 -m64 -I${MKLROOT}/include 
SHAREFLAGS := -O3 -shared -fPIC

all: sum.so

sum.so: sum.c
	$(CC) $< ${LIBFLAGS} $(SHAREFLAGS) $(INCLUDEFLAGS) -o $@

clean:
	rm -rf sum.so
