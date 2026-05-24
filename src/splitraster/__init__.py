from importlib.metadata import PackageNotFoundError, version

from . import io

try:
    __version__ = version("splitraster")
except PackageNotFoundError:
    __version__ = "0.0.0"

__all__ = ["__version__", "io"]
