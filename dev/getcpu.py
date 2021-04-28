import sys
sys.path.append('../src')
from cpuinfo import cpu

for attr in list(dir(cpu)):
    print(attr)
    print(getattr(cpu, attr))
