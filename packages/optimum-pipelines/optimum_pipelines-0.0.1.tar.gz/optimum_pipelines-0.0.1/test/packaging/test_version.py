from packaging import version

from optimum.pipelines import __version__


def test_package_version():
    pkg_version = version.parse(__version__)
    assert pkg_version.major >= 0
    assert pkg_version.minor >= 0
    assert pkg_version.micro > 0
