#!/usr/bin/env python
import glob
from setuptools import setup, Extension

sources = ['pycrfsuite/_pycrfsuite.cpp', 'pycrfsuite/trainer_wrapper.cpp']

# crfsuite
sources += glob.glob('crfsuite/lib/crf/src/*.c')
sources += glob.glob('crfsuite/swig/*.cpp')

sources += ['crfsuite/lib/cqdb/src/cqdb.c']
sources += ['crfsuite/lib/cqdb/src/lookup3.c']

# lbfgs
sources += glob.glob('liblbfgs/lib/*.c')

includes = [
    'crfsuite/include/',
    'crfsuite/lib/cqdb/include',
    'liblbfgs/include',
    'pycrfsuite',
]

ext_modules = [Extension('pycrfsuite._pycrfsuite',
    include_dirs=includes,
    language='c++',
    sources=sources
)]

setup(
    name='python-crfsuite',
    version="0.8.1",
    description="Python binding for CRFsuite",
    long_description=open('README.rst').read(),
    author="Terry Peng, Mikhail Korobov",
    author_email="pengtaoo@gmail.com, kmike84@gmail.com",
    url='https://github.com/tpeng/python-crfsuite',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Cython",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Text Processing :: Linguistic",
    ],
    zip_safe=False,
    packages=['pycrfsuite'],
    ext_modules=ext_modules
)
