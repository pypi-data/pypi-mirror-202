# This file will be called first whenever any file from within this directory is imported.
# Thus, we'll test dependencies only here, once.
try:
    import torch  # noqa: F401
except ImportError as exc:
    raise ModuleNotFoundError(str(exc) + ". Please install `classiq-qml`.") from exc

from ..qnn import datasets, types
from ..qnn.qlayer import QLayer

__all__ = ["datasets", "types", "QLayer"]


def __dir__():
    return __all__
