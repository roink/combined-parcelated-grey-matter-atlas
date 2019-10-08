from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize("atlas_functions.pyx",annotate=True,compiler_directives= {'boundscheck':False,'cdivision':True,'initializedcheck':False}),
)
