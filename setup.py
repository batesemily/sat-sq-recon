'''
Copyright (c) 2023 SLAB Group
Author: Tae Ha "Jeff" Park (tpark94@stanford.edu)
'''

# from distutils.core import setup, find_packages
from setuptools import setup, find_packages
from Cython.Build import cythonize
from distutils.extension import Extension

import numpy as np

def setup_package():
    setup(
        name="sampler",
        ext_modules=cythonize([
            Extension(
                "core.utils.libmesh.triangle_hash",
                [
                    "core/utils/libmesh/triangle_hash.pyx"
                ],
                language="c++11",
                libraries=["stdc++"],
                include_dirs=[np.get_include()],
                extra_compile_args=["-std=c++11", "-O3"]
            ),
        ])
    )


if __name__ == "__main__":
    # setup_package()
    setup(
        name="satsq",
        # version="1",
        packages=['configs', 'dataset', 'nets', 'solver', 'utils'],
        package_dir={'configs': 'core/',
                    'dataset': 'core/',
                    'solver': 'core/',
                    'utils': 'core/'}
    )
