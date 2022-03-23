#!/usr/bin/env python
import glob
import sys
from setuptools import setup, Extension
from distutils.command.build_ext import build_ext

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

class build_ext_check_gcc(build_ext):
    def build_extensions(self):
        c = self.compiler

        _compile = c._compile

        def c_compile(obj, src, ext, cc_args, extra_postargs, pp_opts):
            cc_args = cc_args + ['-std=c99'] if src.endswith('.c') else cc_args
            return _compile(obj, src, ext, cc_args, extra_postargs, pp_opts)

        if c.compiler_type == 'unix' and 'gcc' in c.compiler:
            c._compile = c_compile

        elif self.compiler.compiler_type == "msvc":
            if sys.version_info[:2] < (3, 5):
                c.include_dirs.extend(['crfsuite/win32'])

        build_ext.build_extensions(self)


ext_modules = [Extension('pycrfsuite._pycrfsuite',
    include_dirs=includes,
    language='c++',
    sources=sorted(sources)
)]


setup(
    name='python-crfsuite',
    version="0.9.8",
    description="Python binding for CRFsuite",
    long_description=open('README.rst').read(),
    author="Terry Peng, Mikhail Korobov",
    author_email="pengtaoo@gmail.com, kmike84@gmail.com",
    license="MIT",
    url='https://github.com/scrapinghub/python-crfsuite',
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Cython",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Text Processing :: Linguistic",
    ],
    zip_safe=False,
    packages=['pycrfsuite'],
    ext_modules=ext_modules,
    cmdclass={'build_ext': build_ext_check_gcc},
)
