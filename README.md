# CPyDemo

## About
Demonstration of **packaging** a _command line tool_ written in Python and C.
This minimum working example (MWE) provides implementation of the following features:
  - use native C codes (instead of Cython) for the shared libraries.
  - the shared libraries are loaded in Python using `numpy.ctypes`.
  - use CBLAS routines for linear algebra in the C code.
  - use `mpi4py` for MPI parallelization.
  - call a third-party C library as `include` from the main C library.

Packaging the MWE is done with `setuptools.setup()`.
Compiling the CBLAS routines demands system-specific libraries, 
includes, compile flags and macros.
The `system_info` provided by the setuptools 
in [`numpy`](https://github.com/numpy/numpy) package
is a comprehensive source of such information. 
Here, I have used their implementation.

## Installation
**Prerequisites.**
  - any LAPACK library (MKL, OpenBLAS, libFLAME, Atlas, LAPACK (NetLIB))
  - MPI library.

For a quickstart, try:
```
conda install pip git
pip install git+git://github.com/banskt/cpydemo.git
```
Note this will automatically install the required packages. 
If you want to maintain the dependencies using conda,
you can preinstall the dependencies before running `pip install` for `cpydemo`.
```
conda install numpy mpi4py pandas
pip install git+git://github.com/banskt/cpydemo.git
```
You can also clone the repository, change to the cloned directory and install using pip
```
git clone git@github.com:banskt/cpydemo.git
cd cpydemo
pip install .
```
If you are developing, install using the `-e` flag ("editable"). 
It allows real time changes in the code and the package does not need re-installing every time you make a change.
```
pip install -e .
```

## Check installation
If installation finished without error, the `cpydemo` command line tool will become available.
You can check the command line tool using:
```
cpydemo --test # run all tests 
cpydemo -a 3.2 -b 2.1 # print the sum and difference of the two numbers provided by the flags -a and -b
cpydemo -h # help
```
For testing MPI integration run 
```
mpirun -n 8 cpydemo --test
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
