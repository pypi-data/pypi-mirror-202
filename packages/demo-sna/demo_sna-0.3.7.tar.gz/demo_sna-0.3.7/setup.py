#!/usr/bin/env python

"""The setup script."""

import os
import sys
from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['pip==19.2.3',
'bump2version==0.5.11',
'wheel==0.33.6',
'watchdog==0.9.0',
'flake8==3.7.8',
'tox==3.14.0',
'coverage==4.5.4',
'Sphinx==6.1.3',
'twine==4.0.2',
'torchtext==0.14.0',
'six==1.16.0',
'Django==3.1.7',
'djangorestframework==3.12.2'
 ]

test_requirements = [ ]
VERSION_FILE = os.path.join(os.path.dirname(__file__),
                            'demo_sna',
                            'VERSION')
with open(VERSION_FILE, encoding='utf-8') as version_fp:
    VERSION = version_fp.read().strip()
setup(
    version=VERSION,
    author="Alaa' Omar",
    author_email='alaa.omer2009@gmail.com',
    # classifiers=[
    #     'Development Status :: 2 - Pre-Alpha',
    #     'Intended Audience :: Developers',
    #     'License :: OSI Approved :: MIT License',
    #     'Natural Language :: English',
    #     'Programming Language :: Python :: 3.10' ,
    # ],
    data_files=[('data', ['data/my_data.pickle'])],
    CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'Intended Audience :: Education',
    'Intended Audience :: Information Technology',
    'Intended Audience :: Science/Research',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: Arabic',
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3 :: Only',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Topic :: Scientific/Engineering',
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    'Topic :: Scientific/Engineering :: Information Analysis',
    'Topic :: Text Processing',
    'Topic :: Text Processing :: Linguistic',
     ],
    description="Python Boilerplate contains all the boilerplate you need to create a Python package.",
    entry_points={
        'console_scripts': [
            'demo_sna=demo_sna.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='demo_sna',
    name='demo_sna',
    packages=find_packages(include=['demo_sna', 'demo_sna.*']),
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/eng-aomar/demo',
    python_requires='>=3.7.0, <3.11',
    zip_safe=False,    
)
