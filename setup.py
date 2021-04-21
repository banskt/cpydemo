import sys
import os
import setuptools
import subprocess
import atexit
from setuptools.command.bdist_egg import bdist_egg
from setuptools.command.install import install
from setuptools.command.build_ext import build_ext
from setuptools import Extension

sys.path.append('src')
from version import __version__

# Git version stuff
sha = 'Unknown'
here = os.path.dirname(os.path.abspath(__file__))

try:
    sha = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=here).decode('ascii').strip()
except Exception:
    pass


class Library(Extension):
    def __init__ (self, **kw):
        package = kw.pop('package', None)
        dest_dir = kw.pop('dest_dir', None)
        Extension.__init__(self, **kw)
        self.package = package
        self.dest_dir = dest_dir


class custom_install(install):
    def run(self):
        def _post_install():
            print("Installing C libraries")
            cmd_clean = ['make', 'clean', '-C', 'src/cpydemo/lib']
            cmd_cmake = ['make', '-C', 'src/cpydemo/lib']
            #process = subprocess.Popen(cmd_clean, shell=True)
            #process.communicate()
            #process = subprocess.Popen(cmd_cmake, shell=True)
            #process.communicate()
            subprocess.call(cmd_clean)
            subprocess.call(cmd_cmake)
            #def find_module_path():
            #    for p in sys.path:
            #        if os.path.isdir(p) and my_name in os.listdir(p):
            #            return os.path.join(p, my_name)
            #install_path = find_module_path()
        atexit.register(_post_install)
        install.run(self)


def _post_install():
    print('POST INSTALL')


class new_install(install):
    def __init__(self, *args, **kwargs):
        super(new_install, self).__init__(*args, **kwargs)
        atexit.register(_post_install)


class custom_build_ext(build_ext):
    def build_extensions(self):
        build_ext.build_extensions(self)


## def ext_modules():
##     modules = []
##     csum_dll = dict(
##         name = '',
##         sources = ['lib/cmath.c'],
##         depends = (),
##         configure = ,
##         extra_compile_args = ["-O3"],
##         )
##     modules.append(csum_dll)
##     return modules

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

class bdist_egg_disabled(bdist_egg):
    """Disabled version of bdist_egg
    Prevents setup.py install performing setuptools' default easy_install,
    which it should never ever do.
    """
    def run(self):
        sys.exit("ERROR: aborting implicit building of eggs. Use \"pip install .\" to install from source.")

cmdclass = {'bdist_egg': bdist_egg if 'bdist_egg' in sys.argv else bdist_egg_disabled,
            #'install': custom_install,
            #'install': new_install,
            #'build_ext': custom_build_ext,
           }

def ext_modules():
    modules = list()
    cwd = os.path.abspath(os.path.dirname(__file__))
    compile_args = ["-O3"]
    module1 = dict(
        name = 'cpydemo_sum_lib',
        sources = [os.path.join(cwd, 'src/cpydemo/lib/sum.c')],
        extra_compile_args = compile_args,
    )
    modules.append(module1)
    module2 = dict(
        name = 'cpydemo_diff_lib',
        sources = [os.path.join(cwd, 'src/cpydemo/lib/diff.c')],
        extra_compile_args = compile_args,
    )
    modules.append(module2)
    return [Extension(**ext) for ext in modules]


setuptools.setup(
    name             = "cpydemo",
    version          = __version__,
    author           = "Saikat Banerjee",
    author_email     = "bnrj.saikat@gmail.com",
    description      = "Example for packaging command line tool written in Python and C",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    license          = "MIT",
    url              = "https://github.com/banskt/cpydemo",
    project_urls     = {
        "Bug Tracker": "https://github.com/banskt/cpydemo/issues",
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
    ext_modules      = ext_modules(),
    python_requires  = ">=3.6",
    install_requires = [
        "numpy>=1.19.4",
    ],
    cmdclass         = cmdclass,
)
