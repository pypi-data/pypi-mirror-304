import sys

import mymath_pybind11.bindings as mymath
import numpy as np
import pytest


def test_dot():

    v1 = [1.0, 2, 3, -5.5, 42]
    v2 = [-3.2, 0, 13, 6, -3.14]

    result = mymath.dot(vector1=v1, vector2=v2)
    assert pytest.approx(result) == np.dot(v1, v2)


def test_normalize():

    v = [1.0, 2, 3, -5.5, 42]

    result = mymath.normalize(data=v)
    assert pytest.approx(result) == np.array(v) / np.linalg.norm(v)


def test_dot_numpy():

    v1 = np.array([1.0, 2, 3, -5.5, 42])
    v2 = np.array([-3.2, 0, 13, 6, -3.14])

    result = mymath.dot(vector1=v1, vector2=v2)
    assert pytest.approx(result) == np.dot(v1, v2)


def test_normalize_numpy():

    v = np.array([1.0, 2, 3, -5.5, 42])

    result = mymath.normalize_numpy(data=v)

    assert isinstance(result, np.ndarray)
    assert pytest.approx(result) == np.array(v) / np.linalg.norm(v)


@pytest.mark.skipif(
    sys.platform == "win32", reason="fails with the error: access violation"
)
def test_assertion():

    v1 = np.array([1.0, 2, 3, -5.5])
    v2 = np.array([42.0])

    with pytest.raises(RuntimeError):
        _ = mymath.dot(vector1=v1, vector2=v2)


@pytest.mark.skipif(
    sys.version_info < (3, 7), reason="capture_output and text require Python 3.7"
)
def test_executable():

    import subprocess

    result = subprocess.run("print_answer_pybind11", capture_output=True, text=True)
    assert result.stdout.strip() == "42"

    result = subprocess.run(
        [sys.executable, "-m", "mymath_pybind11.bin", "print_answer_pybind11"],
        capture_output=True,
        text=True,
    )
    assert result.stdout.strip() == "42"
