import warnings

message = """

The 'dlt' package is deprecated.

Version 0.2.4 is the final release of this package. The 'dlt' name will be
repurposed for the data load tool (dlt) project. Prevent installing
the new 'dlt' project by setting your dependency to 'dlt==0.2.4'.
"""

warnings.warn(message, UserWarning)


__all__ = [
    "utils",
    "cifar",
    "mnist",
    "fashion_mnist"
    ]

from . import utils
from . import cifar
from . import mnist
from . import fashion_mnist

