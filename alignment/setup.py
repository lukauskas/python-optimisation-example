from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import numpy

setup(
    cmdclass={'build_ext': build_ext},
    ext_modules=[Extension("align_cythonised", ["align.pyx"],
                           include_dirs=[numpy.get_include()]
    ),
                 Extension("align_cythonised_numpy", ["align_numpy.pyx"],
                           include_dirs=[numpy.get_include()])]
)