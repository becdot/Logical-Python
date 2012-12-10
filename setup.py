from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [Extension("bitc", ["bitc.pyx"]), Extension("multic", ["multic.pyx"]), Extension("sequentialc", ["sequentialc.pyx"]),\
    Extension("ctest_combinational", ["ctest_combinational.pyx"]), Extension("ctest_sequential", ["ctest_sequential.pyx"])]

setup(
  name = 'Bit, Multi and test classes',
  cmdclass = {'build_ext': build_ext},
  ext_modules = ext_modules
)