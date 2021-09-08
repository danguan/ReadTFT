from src.readtft.services import example_service as sut


def test_example():
    assert sut.example_func() is True
