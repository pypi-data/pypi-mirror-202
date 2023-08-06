from . import print_utils
from . import colored_prints as colored

__all__ = [
    "debug_prints",
    "colored_prints",
    "colors"
]

debug_prints = print_utils.debugPrints()
colored_prints = colored.coloredPrint()
colors = colored.colors
