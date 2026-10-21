import os
import subprocess
import sys
import sysconfig

import pytest


def test_version():
    from pycrfsuite import CRFSUITE_VERSION

    assert bool(CRFSUITE_VERSION), CRFSUITE_VERSION


@pytest.mark.skipif(
    not sysconfig.get_config_var("Py_GIL_DISABLED"),
    reason="requires a free-threaded interpreter",
)
def test_import_preserves_free_threading():
    env = os.environ.copy()
    env.pop("PYTHON_GIL", None)
    subprocess.run(
        [
            sys.executable,
            "-W",
            "error",
            "-c",
            "import sys; assert not sys._is_gil_enabled(); "
            "import pycrfsuite; assert not sys._is_gil_enabled()",
        ],
        env=env,
        check=True,
        timeout=30,
    )
