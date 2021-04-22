#ifdef INTEL_MKL_VERSION
    #include <mkl.h>
    void my_cdfnorm( double* X, double* P) {
    	vdCdfNorm( 1, X, P );
    }
#else
    #include <cblas.h>
    #include <cblas_f77.h>
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
