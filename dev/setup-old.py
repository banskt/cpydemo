import sys
import os
import subprocess
import setuptools
import copy
import textwrap

from setuptools.command.bdist_egg import bdist_egg
from setuptools.command.install   import install
from setuptools.command.build_ext import build_ext
from setuptools                   import Extension
from distutils                    import log

#from numpy.distutils.system_info import get_info
IS_RELEASE_BRANCH = False

sys.path.append('src')
from version import __version__

# Git version stuff
#sha = 'Unknown'
#here = os.path.dirname(os.path.abspath(__file__))
#
#try:
#    sha = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=here).decode('ascii').strip()
#except Exception:
#    pass


'''
Redefine the library class to include package and destination directory (dest_dir).
This is not used yet, but the idea is to send the C libraries to the destination directory.
'''
class Library(Extension):
    def __init__ (self, **kw):
        package = kw.pop('package', None)
        dest_dir = kw.pop('dest_dir', None)
        Extension.__init__(self, **kw)
        self.package = package
        self.dest_dir = dest_dir


'''
Redefine the build_ext to have fine-grained control on building C libraries.
Not used in this demo, but is provided for more complex projects.
'''
class custom_build_ext(build_ext):

    def build_extensions(self):
        # self.compiler - the system compiler identified by setuptools / distutils
        #print(dir(self.compiler))
        #for compiler_arg in dir(self.compiler):
        #    print (compiler_arg)
        #    print (getattr(self.compiler, compiler_arg))

        log.info("Building C modules")
        for ext in self.extensions:
            log.info(ext.name)
            for k, v in numpy_get_lapack_info.__dict__.items():
                print (k, v)
        #    for compile_arg in extra_compile_args:
        #        ext.extra_compile_args += [compile_arg]
                #print(compile_arg)
                #print(ext.extra_compile_args)
                #ext.extra_compile_args += f" {compile_arg}"
        #    print (dir(ext))
            property_list = ['define_macros', 'depends', 'export_symbols', 'extra_compile_args', 'extra_link_args', 'extra_objects', 'include_dirs', 'libraries', 'library_dirs', 'runtime_library_dirs', 'sources', 'swig_opts', 'undef_macros']
            #log.info("Name: ", ext.name)
            #log.info("Language: " , ext.language)
            #log.info("py_limited_api: ", ext.py_limited_api)
            #for info in property_list:
            #    log.info(f"{info}: " + ", ".join(getattr(ext, info)))
        build_ext.build_extensions(self)



with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


class bdist_egg_disabled(bdist_egg):
    """Disabled version of bdist_egg
    Prevents setup.py install performing setuptools' default easy_install,
    which it should never ever do.
    """
    def run(self):
        sys.exit("ERROR: aborting implicit building of eggs. Use \"pip install .\" to install from source.")


def pythonlib_dir():
    """return path where libpython* is."""
    if sys.platform == 'win32':
        return os.path.join(sys.prefix, "libs")
    else:
        return get_config_var('LIBDIR')


def get_linalg_compile_args():
    args = list()
    system_linalg = find_system_linalg_lib()
    if system_linalg == 'PY_MKL':
        libflags = ["-lmkl_intel_ilp64", "-lmkl_sequential", "-lmkl_core", "-lpthread", "-lm", "-ldl"]
        args = libflags
    elif system_linalg == 'INTEL_MKL':
        libflags = ["-L${MKLROOT}/lib/intel64", "-Wl,--no-as-needed", "-lmkl_intel_ilp64", "-lmkl_sequential", "-lmkl_core", "-lpthread", "-lm", "-ldl"]
        includeflags = ["-DMKL_ILP64", "-m64", "-I${MKLROOT}/include"]
        args = libflags + includeflags
    elif system_linalg == 'PY_CBLAS':
        args = ["-lcblas"]
    return args


def get_extension(name, sources, libraries, compile_args, **kw):

    local_path = os.path.abspath(os.path.dirname(__file__))

    def dict_append(d, **kws):
        for k, v in kws.items():
            if k in d:
                ov = d[k]
                if isinstance(ov, str):
                    d[k] = v
                else:
                    d[k].extend(v)
            else:
                d[k] = v

    ext_args = copy.copy(kw)
    ext_args['name'] = name
    ext_args['sources'] = sources

    if 'extra_info' in ext_args:
        extra_info = ext_args['extra_info']
        del ext_args['extra_info']
        if isinstance(extra_info, dict):
            extra_info = [extra_info]
        for info in extra_info:
            dict_append(ext_args, **info)

    # Add other libraries
    libnames = ext_args.get('libraries', [])
    ext_args['libraries'] = libnames + libraries
    ext_args['extra_compile_args'] = compile_args

    return Extension(**ext_args)


'''
Piggyback on the numpy setuptools.

It provides information about various resources (libraries, library directories,
include directories, etc.) in the system. Usage:
    info_dict = get_info(<name>)
  where <name> is a string 'atlas','x11','fftw','lapack','blas',
  'lapack_src', 'blas_src', etc. For a complete list of allowed names,
  see the definition of get_info() function below.
  Returned info_dict is a dictionary which is compatible with
  distutils.setup keyword arguments. If info_dict == {}, then the
  asked resource is not available (system_info could not find it).
  Several *_info classes specify an environment variable to specify
  the locations of software. When setting the corresponding environment
  variable to 'None' then the software will be ignored, even when it
  is available in system.

Defer numpy import until after numpy is installed.
'''
class numpy_get_lapack_info(object):
    def __init__(self):
        from numpy.distutils.system_info import get_info
        lapack_info = get_info('lapack_opt', 0)
        for k, v in lapack_info:
            setattr(self, k, v)

class numpy_setup(object):
    def get_info(self):
        from numpy.distutils.system_info import get_info
        return get_info('lapack_opt', 0)


def ext_modules():
    #from numpy.distutils.system_info import get_info
    cwd = os.path.abspath(os.path.dirname(__file__))
    clib_dir = os.path.join(cwd, "src/cpydemo/clib")
    '''
    Obtain information about system Lapack. 
    The default order for the libraries are:
     - MKL
     - OpenBLAS
     - libFLAME
     - ATLAS
     - LAPACK (NetLIB)
    '''
    lapack_info = numpy_get_lapack_info()
    compile_args = ['-O3']
    #compile_args = ["-O3"] +  ["-lpthread", "-lm", "-ldl", "-std=c99"] + ["-lmkl_intel_ilp64", "-lmkl_sequential", "-lmkl_core", "-L${MKLROOT}/lib/intel64"]

    module_src = ['sum.c', 
                  'one_sided_pval.c', 
                  'diff.c']

    modules = []
    extra_libraries = []
    for msrc in module_src:
        filebase = os.path.splitext(os.path.basename(msrc))[0]
        module_name = "{:s}_{:s}_lib".format('cpydemo', filebase)
        filesrc = [os.path.join(clib_dir, msrc)]
        module = get_extension(module_name, filesrc, extra_libraries, compile_args, **dict())
        modules.append(module)

    return modules


def check_setuppy_command():
    run_build = parse_setuppy_commands()
    if run_build:
        try:
            import numpy
            import pybind11
        except ImportError as exc:  # We do not have our build deps installed
            print(textwrap.dedent(
                    """Error: '%s' must be installed before running the build.
                    """
                    % (exc.name,)))
            sys.exit(1)

    return run_build



def parse_setuppy_commands():
    """Check the commands and respond appropriately.  Disable broken commands.
    Return a boolean value for whether or not to run the build or not (avoid
    parsing Cython and template files if False).
    """
    args = sys.argv[1:]

    if not args:
        # User forgot to give an argument probably, let setuptools handle that.
        return True

    info_commands = ['--help-commands', '--name', '--version', '-V',
                     '--fullname', '--author', '--author-email',
                     '--maintainer', '--maintainer-email', '--contact',
                     '--contact-email', '--url', '--license', '--description',
                     '--long-description', '--platforms', '--classifiers',
                     '--keywords', '--provides', '--requires', '--obsoletes']

    for command in info_commands:
        if command in args:
            return False

    # Note that 'alias', 'saveopts' and 'setopt' commands also seem to work
    # fine as they are, but are usually used together with one of the commands
    # below and not standalone.  Hence they're not added to good_commands.
    good_commands = ('develop', 'sdist', 'build', 'build_ext', 'build_py',
                     'build_clib', 'build_scripts', 'bdist_wheel', 'bdist_rpm',
                     'bdist_wininst', 'bdist_msi', 'bdist_mpkg')

    for command in good_commands:
        if command in args:
            return True

    # The following commands are supported, but we need to show more
    # useful messages to the user
    if 'install' in args:
        print(textwrap.dedent("""
            Note: for reliable uninstall behaviour and dependency installation
            and uninstallation, please use pip instead of using
            `setup.py install`:
              - `pip install .`       (from a git repo or downloaded source
                                       release)
              - `pip install scipy`   (last SciPy release on PyPI)
            """))
        return True

    if '--help' in args or '-h' in sys.argv[1]:
        print(textwrap.dedent("""
            SciPy-specific help
            -------------------
            To install SciPy from here with reliable uninstall, we recommend
            that you use `pip install .`. To install the latest SciPy release
            from PyPI, use `pip install scipy`.
            For help with build/installation issues, please ask on the
            scipy-user mailing list.  If you are sure that you have run
            into a bug, please report it at https://github.com/scipy/scipy/issues.
            Setuptools commands help
            ------------------------
            """))
        return False


    # The following commands aren't supported.  They can only be executed when
    # the user explicitly adds a --force command-line argument.
    bad_commands = dict(
        test="""
            `setup.py test` is not supported.  Use one of the following
            instead:
              - `python runtests.py`              (to build and test)
              - `python runtests.py --no-build`   (to test installed scipy)
              - `>>> scipy.test()`           (run tests for installed scipy
                                              from within an interpreter)
            """,
        upload="""
            `setup.py upload` is not supported, because it's insecure.
            Instead, build what you want to upload and upload those files
            with `twine upload -s <filenames>` instead.
            """,
        upload_docs="`setup.py upload_docs` is not supported",
        easy_install="`setup.py easy_install` is not supported",
        clean="""
            `setup.py clean` is not supported, use one of the following instead:
              - `git clean -xdf` (cleans all files)
              - `git clean -Xdf` (cleans all versioned files, doesn't touch
                                  files that aren't checked into the git repo)
            """,
        check="`setup.py check` is not supported",
        register="`setup.py register` is not supported",
        bdist_dumb="`setup.py bdist_dumb` is not supported",
        bdist="`setup.py bdist` is not supported",
        flake8="`setup.py flake8` is not supported, use flake8 standalone",
        build_sphinx="`setup.py build_sphinx` is not supported, see doc/README.md",
        )
    bad_commands['nosetests'] = bad_commands['test']
    for command in ('upload_docs', 'easy_install', 'bdist', 'bdist_dumb',
                     'register', 'check', 'install_data', 'install_headers',
                     'install_lib', 'install_scripts',):
        bad_commands[command] = "`setup.py %s` is not supported" % command

    for command in bad_commands.keys():
        if command in args:
            print(textwrap.dedent(bad_commands[command]) +
                  "\nAdd `--force` to your command to use it anyway if you "
                  "must (unsupported).\n")
            sys.exit(1)

    # Commands that do more than print info, but also don't need Cython and
    # template parsing.
    other_commands = ['egg_info', 'install_egg_info', 'rotate', 'dist_info', 'build_wheel']
    for command in other_commands:
        if command in args:
            return False

    # If we got here, we didn't detect what setup.py command was given
    log.warn("Unrecognized setuptools command ('{}'), proceeding with "
                  "generating Cython sources and expanding templates".format(
                  ' '.join(sys.argv[1:])))
    return True


def setup_package():
    np_minversion = '1.16.5'
    np_maxversion = '9.9.99'
    python_minversion = '3.7'
    python_maxversion = '3.10'
    if IS_RELEASE_BRANCH:
        req_np = 'numpy>={},<{}'.format(np_minversion, np_maxversion)
        req_py = '>={},<{}'.format(python_minversion, python_maxversion)
    else:
        req_np = 'numpy>={}'.format(np_minversion)
        req_py = '>={}'.format(python_minversion)

    # Rewrite the version file every time
    #write_version_py()

    cmdclass = {'bdist_egg': bdist_egg if 'bdist_egg' in sys.argv else bdist_egg_disabled,
                'build_ext': custom_build_ext,
               }


    metadata = dict(
        name             = "cpydemo",
        version          = __version__,
        author           = "Saikat Banerjee",
        author_email     = "bnrj.saikat@gmail.com",
        description      = "Example for packaging command line tool written in Python and C",
        long_description = long_description,
        long_description_content_type = "text/markdown",
        license          = "MIT",
        url              = "https://github.com/banskt/cpydemo",
        download_url     = "https://github.com/banskt/cpydemo",
        project_urls     = {
            "Bug Tracker":   "https://github.com/banskt/cpydemo/issues",
            "Documentation": "https://github.com/banskt/cpydemo",
            "Source Code" :  "https://github.com/banskt/cpydemo",
        },
        classifiers      = [
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        packages         = setuptools.find_packages(where = "src"),
        package_dir      = {"": "src"},
        entry_points     = {'console_scripts': ['cpydemo = cpydemo.main:main']},
        #ext_modules      = [Extension(**ext) for ext in ext_modules()],
        #ext_modules      = ext_modules(),
        python_requires  = req_py,
        install_requires = [req_np],
        #cmdclass         = cmdclass,
    )

    if "--force" in sys.argv:
        run_build = True
        sys.argv.remove('--force')
    else:
        # Raise errors for unsupported commands, improve help output, etc.
        run_build = check_setuppy_command()

    # Disable OSX Accelerate, it has too old LAPACK
    os.environ['ACCELERATE'] = 'None'

    # This import is here because it needs to be done before importing setup()
    # from numpy.distutils, but after the MANIFEST removing and sdist import
    # higher up in this file.
    from setuptools import setup

    if run_build:
        from numpy.distutils.core import setup

        # Customize extension building
        #cmdclass['build_ext'] = get_build_ext_override()
        #cmdclass['build_clib'] = get_build_clib_override()

        #cwd = os.path.abspath(os.path.dirname(__file__))
        #if not os.path.exists(os.path.join(cwd, 'PKG-INFO')):
        #    # Generate Cython sources, unless building from source release
        #    generate_cython()

        #metadata['configuration'] = configuration
    else:
        # Don't import numpy here - non-build actions are required to succeed
        # without NumPy for example when pip is used to install Scipy when
        # NumPy is not yet present in the system.

        # Version number is added to metadata inside configuration() if build
        # is run.
        metadata['version'] = __version__

    setup(**metadata)


if __name__ == '__main__':
    setup_package()
