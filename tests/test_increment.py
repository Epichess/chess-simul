from src.testpkg.testfile import increment


def test_increment():
    assert increment(3) == 4
