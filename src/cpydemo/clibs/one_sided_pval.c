/* 
 * CPyDemo
 *
 * Example of including MKL special functions.
 * These functions are not available in CBLAS routines
 * of other implementations such as LAPACK.
 * Including "mkl.h" is not possible as it is not provided
 * by Python MKL 
 * Hence, the header needs to be defined in place as shown here.
 */

#include <stdlib.h>

/* default MKL macro from numpy */
#ifdef SCIPY_MKL_H
    /*
     * cannot include mkl.h
     * because miniconda/mkl does not provide this include
     * include <mkl.h>
     *
     * Define the header manually
     */
    typedef size_t  INT;
    #define MKL_INT INT // this tells MKL about user's MKL_INT type
    void vdCdfNorm(const MKL_INT *n, const double a[], double r[]);

    void my_cdfnorm( double* X, double* P) {
    	vdCdfNorm( 1, X, P );
    }
/* default CBLAS macro from numpy */
#elif HAVE_CBLAS
    #include "npy_cblas.h"
    #include "dcdflib/src/dcdflib.c"
    #include "dcdflib/src/ipmpar.c"
    void my_cdfnorm( double* X, double* P) {
    	int which[1] = {1}; // iwhich = 1 : Calculate P and Q from X,MEAN and SD
    	double Q[1] = {0.0};
    	double MEAN[1] = {0.0};
    	double SD[1] = {1.0};
    	int status[1] = {0};
    	double bound[1];
        cdfnor(which, P, Q, X, MEAN, SD, status, bound);
    }
#endif


double one_sided_pval ( double x, double mu, double sigma ) {

	double pval;

	double *QS = (double *) calloc( 1 * sizeof( double ), 64);
	if (QS == NULL) {goto cleanup_QS;}

	double *P = (double *) calloc( 1 * sizeof( double ), 64);
	if (P == NULL) {goto cleanup_P;}

    QS[0] = (x - mu) / sigma;
    P[0] = 0;
    my_cdfnorm( QS, P );
    pval = (1 - P[0]);

cleanup:
cleanup_QS:
	free(QS);
cleanup_P:
	free(P);

	return pval;
}
