####################################################################
#
# Flex Table
# Fast and flexible Pyhon library for text tables.
#
# Copyright ©2023 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/python-flex-table/
#
####################################################################

from enum import Enum


class Align(str, Enum):
    """
    Table cell content alignment.
    """

    # Automated alignment (decided at runtime; default).
    AUTO = 'auto'

    # Content is aligned to left.
    LEFT = 'left'

    # Content is aligned to right.
    RIGHT = 'right'

    # Content is centered.
    CENTER = 'center'
