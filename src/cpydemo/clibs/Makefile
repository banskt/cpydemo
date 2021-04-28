CC := gcc 
CP := g++ 
LIBFLAGS := -L${MKLROOT}/lib/intel64 -Wl,--no-as-needed -lmkl_intel_ilp64 -lmkl_sequential -lmkl_core -lpthread -lm -ldl -std=c99
INCLUDEFLAGS := -DMKL_ILP64 -m64 -I${MKLROOT}/include 
SHAREFLAGS := -O3 -shared -fPIC

all: cpydemo_sum_lib.so cpydemo_diff_lib.so cpydemo_one_sided_pval_lib.so

cpydemo_sum_lib.so: sum.c
	$(CC) $< $(SHAREFLAGS) $(INCLUDEFLAGS) -o $@

cpydemo_diff_lib.so: diff.c
	$(CC) $< $(SHAREFLAGS) $(INCLUDEFLAGS) -o $@

cpydemo_one_sided_pval_lib.so: one_sided_pval.c
	$(CC) $< ${LIBFLAGS} $(SHAREFLAGS) $(INCLUDEFLAGS) -o $@

clean:
	rm -rf cpydemo_sum_lib.so cpydemo_diff_lib.so cpydemo_one_sided_pval_lib.so
