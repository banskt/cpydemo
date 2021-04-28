import sys
sys.path.append('../src')
import system_info as sysinfo
res = sysinfo.get_info('mkl')
print (res)
