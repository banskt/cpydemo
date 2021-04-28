# CPyDemo

Demonstration of packaging a command line tool using Python and ctypes.
It creates shared libraries from C code and calls the shared libraries using `numpy.ctypes`.
```
pip install git+git://github.com/banskt/cpydemo.git
```
Or, clone the repository and install from the root directory
```
pip install .
```
For development version, install using the `-e` flag ("editable").
```
pip install -e .
```

Check the installation by running `cpydemo` from the command line:
```
cpydemo --test # run all tests 
cpydemo -a 3.2 -b 2.1 # print the sum and difference of the two numbers provided by the flags -a and -b
cpydemo -h # help
```

## Directory structure
```
$ tree . -I "__pycache__|*.egg-info"

.
├── configs.ini
├── dev
│   ├── getcpu.py
│   ├── setup-old.py
│   └── showmkl.py
├── LICENSE
├── MANIFEST.in
├── pyproject.toml
├── README.md
├── setup.py
└── src
    ├── cpuinfo.py
    ├── cpydemo
    │   ├── clibs
    │   │   ├── dcdflib
    │   │   │   ├── doc
    │   │   │   │   ├── dcdflib.chs
    │   │   │   │   ├── dcdflib.fdoc
    │   │   │   │   └── dcdflib.h
    │   │   │   ├── README
    │   │   │   └── src
    │   │   │       ├── cdflib.h
    │   │   │       ├── dcdflib.c
    │   │   │       └── ipmpar.c
    │   │   ├── diff.c
    │   │   ├── __init__.py
    │   │   ├── Makefile
    │   │   ├── Makefile.openblas
    │   │   ├── matmul.c
    │   │   ├── npy_cblas_base.h
    │   │   ├── npy_cblas.h
    │   │   ├── one_sided_pval.c
    │   │   └── sum.c
    │   ├── hellompi.py
    │   ├── __init__.py
    │   ├── main.py
    │   ├── stats
    │   │   ├── cmath.py
    │   │   ├── __init__.py
    │   │   ├── __init__.pyc
    │   │   └── tests
    │   │       ├── __init__.py
    │   │       ├── __init__.pyc
    │   │       └── test_cmath.py
    │   ├── unittest_tester.py
    │   └── utils
    │       ├── __init__.py
    │       └── logs.py
    ├── system_info.py
    └── version.py

```

## Resources
1. Documentations
 - [Where does Python look for modules?](https://bic-berkeley.github.io/psych-214-fall-2016/sys_path.html)
 - [`setuptools` documentation](https://setuptools.readthedocs.io/en/latest/index.html)
 - `setuptools` is under-documented. [Here is the documentation of the old `distutils.core`](https://docs.python.org/3/distutils/apiref.html)
 - [Wrapping C/C++ library as a Python extension module](https://martinsosic.com/development/2016/02/08/wrapping-c-library-as-python-module.html)
2. Stackoverflow discussions
 - [Compile C library on pip install](https://stackoverflow.com/questions/47360113/compile-c-library-on-pip-install)
 - [Post-install scripts with Python setuptools](https://stackoverflow.com/questions/20288711/post-install-script-with-python-setuptools?answertab=votes#tab-top)
3. Example packaing
 - [`jasmcaus/caer`](https://github.com/jasmcaus/caer)
 - [`numpy/numpy`](https://github.com/numpy/numpy)
 - [`mpi4py/mpi4py`](https://github.com/mpi4py/mpi4py)
