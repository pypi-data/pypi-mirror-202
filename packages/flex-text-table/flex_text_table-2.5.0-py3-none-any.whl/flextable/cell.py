####################################################################
#
# Flex Table
# Fast and flexible Pyhon library for text tables.
#
# Copyright ©2023 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/python-flex-table/
#
####################################################################

from typing import Union, Optional

from flextable.align import Align


class Cell(object):
    def __init__(self, value: Optional[Union[str, int, float, bool]] = '', align=Align.AUTO):
        self.value: Optional[Union[str, int, float, bool]] = value
        self.align: Align = align

    # * ****************************************************************************************** *

    @property
    def value(self) -> Optional[Union[str, int, float, bool]]:
        return self._value

    @value.setter
    def value(self, value: Optional[Union[str, int, float, bool]]) -> None:
        if value is None:
            value = 'NONE'
        elif isinstance(value, bool):
            value = str(value).upper()
        else:
            value = str(value)

        self._value = value

    # * ****************************************************************************************** *

    @property
    def align(self) -> Align:
        return self._align

    @align.setter
    def align(self, align: Align) -> None:
        self._align = align
