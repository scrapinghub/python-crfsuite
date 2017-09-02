#!/usr/bin/env bash

# Kill the build if anything errors
set -e -x

# Compile wheels
for PYBIN in /opt/python/*/bin; do
    if [[ "${PYBIN}" == *"cp27"* ]] || \
       [[ "${PYBIN}" == *"cp33"* ]] || \
       [[ "${PYBIN}" == *"cp34"* ]] || \
       [[ "${PYBIN}" == *"cp35"* ]] || \
       [[ "${PYBIN}" == *"cp36"* ]]; 
    then
        "${PYBIN}/pip" install tox
        "${PYBIN}/pip" install -U cython
        export PATH="${PYBIN}:$PATH"
        (cd /io/ && export BIN="${PYBIN}" && bash ./.manylinux-cython.sh && "${PYBIN}/tox" -e manylinux)
        "${PYBIN}/pip" install -e /io/
        "${PYBIN}/pip" wheel /io/ -w wheelhouse/
    fi
done

# Bundle external shared libraries into the wheels
for whl in wheelhouse/*.whl; do
    auditwheel repair "$whl" -w /io/wheelhouse/
done

# Install new wheels and test
for PYBIN in /opt/python/*/bin; do
    if [[ "${PYBIN}" == *"cp27"* ]] || \
       [[ "${PYBIN}" == *"cp33"* ]] || \
       [[ "${PYBIN}" == *"cp34"* ]] || \
       [[ "${PYBIN}" == *"cp35"* ]] || \
       [[ "${PYBIN}" == *"cp36"* ]];
    then
        "${PYBIN}/pip" uninstall -y python-crfsuite
        "${PYBIN}/pip" install python-crfsuite --no-index -f /io/wheelhouse
        "${PYBIN}/pip" install pytest
        "${PYBIN}/pytest" /io/tests --doctest-modules
    fi
done

# If everything works, upload wheels to PyPi
travis=$( cat /io/.travis_tag )
SAMPLE_PYBIN="/opt/python/cp35-cp35m/bin"
if [[ $travis ]]; then
    "${SAMPLE_PYBIN}/pip" install twine;
    "${SAMPLE_PYBIN}/twine" upload --config-file /io/.pypirc /io/wheelhouse/*.whl;
fi
