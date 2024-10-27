import numpy as np
from pgvector.utils import HalfVector
import pytest


class TestHalfVector:
    def test_list(self):
        assert HalfVector([1, 2, 3]).to_list() == [1, 2, 3]

    def test_list_str(self):
        with pytest.raises(ValueError, match='could not convert string to float'):
            HalfVector([1, 'two', 3])

    def test_tuple(self):
        assert HalfVector((1, 2, 3)).to_list() == [1, 2, 3]

    def test_ndarray(self):
        arr = np.array([1, 2, 3])
        assert HalfVector(arr).to_list() == [1, 2, 3]
        assert HalfVector(arr).to_numpy() is not arr

    def test_ndarray_same_object(self):
        arr = np.array([1, 2, 3], dtype='>f2')
        assert HalfVector(arr).to_list() == [1, 2, 3]
        assert HalfVector(arr).to_numpy() is arr

    def test_ndim_two(self):
        with pytest.raises(ValueError) as error:
            HalfVector([[1, 2], [3, 4]])
        assert str(error.value) == 'expected ndim to be 1'

    def test_ndim_zero(self):
        with pytest.raises(ValueError) as error:
            HalfVector(1)
        assert str(error.value) == 'expected ndim to be 1'

    def test_repr(self):
        assert repr(HalfVector([1, 2, 3])) == 'HalfVector([1.0, 2.0, 3.0])'
        assert str(HalfVector([1, 2, 3])) == 'HalfVector([1.0, 2.0, 3.0])'

    def test_dimensions(self):
        assert HalfVector([1, 2, 3]).dimensions() == 3
