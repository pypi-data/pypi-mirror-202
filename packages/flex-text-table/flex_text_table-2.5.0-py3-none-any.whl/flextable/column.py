####################################################################
#
# Flex Table
# Fast and flexible Pyhon library for text tables.
#
# Copyright ©2023 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/python-flex-table/
#
####################################################################

from typing import Optional

from flextable.align import Align


class Column(object):
    def __init__(self, title: str,
                 align: Align = Align.AUTO,
                 max_width: int = 0,
                 cell_align: Optional[Align] = Align.AUTO,
                 title_align: Optional[Align] = Align.AUTO,
                 visible: bool = True):
        self._title: str = title
        self._max_width: int = max_width
        self._cell_align: Align = cell_align if cell_align is not None else Align.AUTO
        self._title_align: Align = title_align if title_align is not None else Align.AUTO
        self._visible: bool = visible

    # * ****************************************************************************************** *

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        self._title = value

    # * ****************************************************************************************** *

    @property
    def align(self) -> Align:
        raise RuntimeError('This is not a real property. Query title or cell align instead.')

    @align.setter
    def align(self, value: Align) -> None:
        self.title_align = value
        self.cell_align = value

    # * ****************************************************************************************** *

    @property
    def title_align(self) -> Align:
        return self._title_align

    @title_align.setter
    def title_align(self, value: Align) -> None:
        self._title_align = value

    # * ****************************************************************************************** *

    @property
    def cell_align(self) -> Align:
        return self._cell_align

    @cell_align.setter
    def cell_align(self, value: Align) -> None:
        self._cell_align = value

    # * ****************************************************************************************** *

    @property
    def max_width(self) -> int:
        return self._max_width

    @max_width.setter
    def max_width(self, value: int) -> None:
        self._max_width = value

    @property
    def width(self) -> int:
        return self.max_width

    def update_max_width(self, width: int) -> 'Column':
        if width > self.max_width:
            self.max_width = width
        return self

    # * ****************************************************************************************** *

    @property
    def visible(self) -> bool:
        return self._visible

    @visible.setter
    def visible(self, value: bool) -> None:
        self._visible = value
