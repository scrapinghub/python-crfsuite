#!/usr/bin/env python
import glob
import sys
from distutils.command.build_ext import build_ext

from Cython.Build import cythonize
from setuptools import Extension, setup

sources = ["pycrfsuite/_pycrfsuite.pyx", "pycrfsuite/trainer_wrapper.cpp"]

# crfsuite
sources += glob.glob("crfsuite/lib/crf/src/*.c")
sources += glob.glob("crfsuite/swig/*.cpp")

sources += ["crfsuite/lib/cqdb/src/cqdb.c"]
sources += ["crfsuite/lib/cqdb/src/lookup3.c"]

# lbfgs
sources += glob.glob("liblbfgs/lib/*.c")

includes = [
    "crfsuite/include/",
    "crfsuite/lib/cqdb/include",
    "liblbfgs/include",
    "pycrfsuite/",
]


class build_ext_check_gcc(build_ext):
    def build_extensions(self):
        c = self.compiler

        _compile = c._compile

        def c_compile(obj, src, ext, cc_args, extra_postargs, pp_opts):
            cc_args = (
                cc_args + ["-D_POSIX_C_SOURCE=200112L"]
                if src.startswith("crfsuite/")
                else cc_args
            )
            cc_args = cc_args + ["-std=c99"] if src.endswith(".c") else cc_args
            return _compile(obj, src, ext, cc_args, extra_postargs, pp_opts)

        if c.compiler_type == "unix" and any(
            item == "gcc" or item.endswith("-gcc") for item in c.compiler
        ):
            c._compile = c_compile

        elif self.compiler.compiler_type == "msvc":
            if sys.version_info[:2] < (3, 5):
                c.include_dirs.extend(["crfsuite/win32"])

        build_ext.build_extensions(self)


setup(
    ext_modules=cythonize(
        [
            Extension(
                "pycrfsuite._pycrfsuite",
                include_dirs=includes,
                language="c++",
                sources=sorted(sources),
            )
        ]
    ),
    cmdclass={"build_ext": build_ext_check_gcc},
)
