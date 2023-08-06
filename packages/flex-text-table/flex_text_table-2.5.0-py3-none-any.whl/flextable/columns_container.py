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
from flextable.column import Column
from flextable.exceptions import DuplicateColumnKeyError


class ColumnsContainer(BaseContainer[Column]):
    def __init__(self, items: Dict[Union[str, int], Column] = None):
        super().__init__(items, Column)

    # Implement the __setitem__ method to set items using keys
    def __setitem__(self, column_key: str, column: Column) -> None:
        if column_key in self:
            raise DuplicateColumnKeyError.for_column_key(column_key)
        if not isinstance(column, Column):
            raise TypeError(f'column_val must be Column, {type(column)} given.')

        self._container[column_key] = column

        self[column_key].update_max_width(len(column.title))

    # Implement the __getitem__ method to access items using keys
    def __getitem__(self, key: Union[str, int]) -> Column:
        # if it's int then it is INDEX not a key!
        if isinstance(key, int):
            keys = list(self._container.keys())
            return self._container[keys[key]]

        return self._container[key]

    # * ****************************************************************************************** *

    def get_key_by_index(self, index: int) -> str:
        return list(self.container.keys())[index]

    def keys(self):
        return self.container.keys()

    def visible_items(self):
        return {key: column for key, column in self.container.items() if column.visible}
