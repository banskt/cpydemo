import mpi4py
mpi4py.rc.initialize = False
mpi4py.rc.finalize = False
from mpi4py import MPI

MPI.Init()
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
ncore = comm.Get_size()

if rank == 0:
    print ("Using MPI in {:d} cores".format(ncore))

print ("Reporting from node: {:d}".format(rank))

MPI.Finalize()
