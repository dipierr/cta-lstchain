#!/usr/bin/env python
# Licensed under a 3-clause BSD style license - see LICENSE.rst
# import sys
from setuptools import setup, find_packages
import os
import sys

# Add lstchain folder to path (contains version.py)
# this is needed as lstchain/__init__.py imports dependencies
# that might not be installed before setup runs, so we cannot import
# lstchain.version
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lstchain'))
from version import get_version, update_release_version  # noqa


update_release_version()
version = get_version()


def find_scripts(script_dir, prefix):
    script_list = [
        os.path.splitext(f)[0]
        for f in os.listdir(script_dir) if f.startswith(prefix)
    ]
    script_dir = script_dir.replace('/', '.')
    point_list = []

    for f in script_list:
        point_list.append(f"{f} = {script_dir}.{f}:main")

    return point_list


lstchain_list = find_scripts('lstchain/scripts', 'lstchain_')
onsite_list = find_scripts('lstchain/scripts/onsite', 'onsite_')
tools_list = find_scripts('lstchain/tools', 'lstchain_')

entry_points = {}
entry_points['console_scripts'] = lstchain_list + onsite_list + tools_list

setup(
    version=version,
    packages=find_packages(),
    install_requires=[
        'astropy',
        'ctapipe~=0.7.0',
        'ctaplot~=0.5.2',
        'eventio~=0.20.3',
        'gammapy>=0.17',
        'h5py',
        'matplotlib',
        'numba',
        'numpy',
        'pandas',
        'scipy',
        'seaborn',
        'scikit-learn',
        'tables',
        'joblib',
        'traitlets',
        'joblib',
    ],
    package_data={
        'lstchain': ['data/lstchain_standard_config.json'],
    },
    tests_require=[
        'pytest',
        'pytest-ordering',
    ],
    entry_points=entry_points
)
