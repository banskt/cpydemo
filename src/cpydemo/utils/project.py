import os

def version():
    ## Get the version from version.py without importing the package
    vfn = os.path.join(os.path.dirname(__file__), '../version.py')
    exec(compile(open(vfn).read(), vfn, 'exec'))
    res = locals()['__version__']
    return res 
