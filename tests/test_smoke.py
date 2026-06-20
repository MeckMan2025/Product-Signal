import product_signal


def test_version_present():
    assert product_signal.__version__.startswith("2.")
