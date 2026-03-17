from app.math_utils import add
from app.math_utils import subtract

def test_add_two_numbers():
    assert add(2, 3) == 5

def test_subtract_numbers():
    assert subtract(10, 4) == 6