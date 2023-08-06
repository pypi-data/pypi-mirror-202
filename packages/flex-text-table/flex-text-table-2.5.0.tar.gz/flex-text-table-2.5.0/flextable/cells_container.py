####################################################################
#
# Flex Table
# Fast and flexible Pyhon library for text tables.
#
# Copyright ©2023 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/python-flex-table/
#
####################################################################

from typing import Dict, Union

from flextable.base_container import BaseContainer
from flextable.cell import Cell
from flextable.exceptions import ColumnKeyNotFoundError, DuplicateColumnKeyError


class CellsContainer(BaseContainer[Cell]):
    def __init__(self, items: Dict[Union[str, int, float], Cell] = None):
        super().__init__(items, Cell)

    # * ****************************************************************************************** *

    def add_cell(self, column_key: Union[str, int, float], cell: Cell) -> 'CellsContainer':
        if column_key in self._container:
            raise DuplicateColumnKeyError.for_column_key(column_key)
        self._container[column_key] = cell
        return self

    def get_cell(self, column_key: Union[str, int, float]) -> Cell:
        if column_key not in self._container:
            raise ColumnKeyNotFoundError(f'Column key {column_key} not found')
        return self._container[column_key]
