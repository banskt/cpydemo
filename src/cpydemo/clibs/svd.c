
#include <stdbool.h>
#include "svd.h"
#include "utils.h"                              /* min, transpose */

bool svd(double* GX, double* S, double* U, double* VT, int ngene, int nsample){

    bool success;
    int nS;

    success = false;
    nS = min(ngene, nsample);

    double *GXT = (double *) calloc( (unsigned long)  ngene * nsample  * sizeof( double ), 64 );
    if (GXT == NULL) {success = false; goto cleanup_GXT;}

    //success = transpose(GX, ngene, nsample, GXT);
    //if ( success == false ) goto cleanup;

    //success = dsvd (GXT, nsample, ngene, S, U, VT);
    success = dsvd (GX, ngene, nsample, S, U, VT);
    //if ( success == false ) goto cleanup;

cleanup:
cleanup_GXT:
    free(GXT);

    return success;
}
