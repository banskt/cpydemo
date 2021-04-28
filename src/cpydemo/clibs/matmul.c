/* 
 * CPyDemo
 *
 * Example of matrix multiplication using CBLAS function
 * 
 */

 /* include npy_cblas.h and let setuptools handle the rest */
#include "npy_cblas.h"

#include <stdbool.h> /* bool type */
#include <stdlib.h> /* calloc, free */

/*
 * ===  FUNCTION  ======================================================================
 *         Name:  matmulAB
 *  Description:  Multiplies matrix A of size m x k
 *                with matrix B of size k x n and returns
 *                matrix C of size m x n
 * =====================================================================================
 */

bool matmulAB( double* A, double* B, double* C, int m, int k, int n)
{
	double alpha = 1.0;
	double beta  = 0.0;

	for (int i = 0; i < (m*n); i++) {
        C[i] = 0.0;
    }

    cblas_dgemm(CblasRowMajor, CblasNoTrans, CblasNoTrans,
                m, n, k, alpha, A, k, B, n, beta, C, n);

    return true;

}


 /*
 * ===  FUNCTION  ======================================================================
 *         Name:  A_vecV
 *  Description:  Multiplies matrix A of size m x n
 *                with vector V of length n x 1
 *                and outputs vector B of size m x 1
 * =====================================================================================
 */
bool A_vecV(double* A, double* v, double* B, int m, int n, int ioff)
{
	bool success;
	double alpha = 1.0;
	double beta  = 0.0;
	double * y;
	y = (double *) calloc( (unsigned long) (m - 1) * sizeof( double ), 64 );
	if (y == NULL) {success = false; goto cleanup_y;}

	for (int i=0; i < m; i++) {
		y[i] = 0.0;
	}

	cblas_dgemv(CblasRowMajor, CblasNoTrans, m, n, alpha, A, n, v, 1, beta, y, 1 );

	for (int i=0; i<m; i++) {
		B[ioff + i] = y[i];
	}
	success = true;

	cleanup_y:
		free(y);
	return success;
}
