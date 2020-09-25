import numpy as np

# run python script like this to implement cython build:
# python regens_LD_cgetter_setup.py build_ext --inplace

import pyximport
pyximport.install()
import distutils.core
import Cython.Build
distutils.core.setup(
    ext_modules = Cython.Build.cythonize('regens_LD_cgetter.pyx'),
    include_dirs = [np.get_include()])