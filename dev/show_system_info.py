import sys
sys.path.append('../src')
import system_info as sysinfo

for opt in ['lapack_opt', 'blas_opt']:
    print("==================")
    print(opt)
    res = sysinfo.get_info(opt)
    print (res)
