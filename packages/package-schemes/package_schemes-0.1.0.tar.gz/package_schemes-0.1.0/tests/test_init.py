# type: ignore


def test_version():
    from package_schemes import __version__

    assert __version__


def test_imports():
    import package_schemes

    assert package_schemes.Package
    assert package_schemes.PoetryLock
    assert package_schemes.UvLockV1
    assert package_schemes.Project

    assert package_schemes.UvLockV1Scheme
    assert package_schemes.PyProjectScheme
