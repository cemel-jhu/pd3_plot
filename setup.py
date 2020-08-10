# Adapted from Tensorflow under http://www.apache.org/licenses/LICENSE-2.0
"""pd3_plot is a utility for visulizing simulations from pd3.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import fnmatch
import os
import re
import sys

from glob import glob

from setuptools import setup
from setuptools.command.install import install as InstallCommandBase
from setuptools.dist import Distribution

# This version string is semver compatible, but incompatible with pip.
# For pip, we will remove all '-' characters from this string, and use the
# result for pip.
_VERSION = '1.0.1'

REQUIRED_PACKAGES = [
    'absl-py >= 0.7.0',
    'numpy >= 1.16.0, < 2.0',
    'protobuf >= 3.9.2',
    'wheel >= 0.26',
    'six >= 1.12.0',
    'typing-extensions >= 3.7.4',
    # scipy < 1.4.1 causes segfaults due to pybind11
    'scipy == 1.4.1',
    'seaborn==0.10.1',
    'ipyvolume==0.5.2',
    'matplotlib==3.3.0',
    'pd3 == 0.0.1'
]

project_name = 'pd3_plot'
DOCLINES = __doc__.split('\n')

setup(
    name=project_name,
    version=_VERSION.replace('-', ''),
    description=DOCLINES[0],
    long_description='\n'.join(DOCLINES[2:]),
    url='https://github.com/cemel-jhu/pd3_plot',
    download_url='https://github.com/cemel-jhu/pd3_plot/tags',
    authors='pd3 authors',
    author_emails=['madisetti@jhu.edu'],
    # Contained modules and scripts.
    packages=['pd3_plot'],
    install_requires=REQUIRED_PACKAGES,
    tests_require=REQUIRED_PACKAGES,
    # Add in any packaged data, but not that this is not bound to be respected
    # by bdist_wheel
    include_package_data=True,
    # PyPI package information.
    classifiers=[
        'Development Status :: 1 - Planning',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Intended Audience :: Science/Research',
    ],
    license='MIT',
    keywords='pd3 discrete dislocation dynamics ddd',
)
