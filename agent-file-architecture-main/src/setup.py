# setup.py
from setuptools import setup, Extension
from Cython.Build import cythonize

# 여러 개의 확장 모듈 정의
ext_modules = [
    Extension("add", ["add_module.pyx"]),
    Extension("subtract", ["subtract_module.pyx"]),
    Extension("multiply", ["multiply_module.pyx"]),
    Extension("divide", ["divide_module.pyx"]),
]

setup(
    name="math_operations",
    ext_modules=cythonize(ext_modules),
)
