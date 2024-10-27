from importlib import metadata as _metadata

from package_schemes.interfaces import *  # noqa: F403
from package_schemes.schemes import *  # noqa: F403

try:
    __version__ = _metadata.version('package-schemes')

except _metadata.PackageNotFoundError:
    __version__ = '0.0.0'
