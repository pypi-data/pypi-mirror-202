####################################################################
#
# Flex Table
# Fast and flexible Pyhon library for text tables.
#
# Copyright ©2023 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/python-flex-table/
#
####################################################################

from typing import List, Union, Dict, Optional

from flextable.align import Align
from flextable.column import Column
from flextable.columns_container import ColumnsContainer
from flextable.exceptions import UnsupportedColumnTypeError
from flextable.renderers.contracts import RendererContract
from flextable.renderers.fancy_renderer import FancyRenderer
from flextable.row import Row
from flextable.rows_container import RowsContainer


class FlexTable(object):
    def __init__(self, header_columns: Optional[List[Union[str, Column]]] = None):  # noqa: WPS234
        """
        Initializes a new instance of the FlexTable class with an optional list of header columns.

        :param header_columns: A list of header columns.
        """
        self.init(header_columns)

    def init(self, header_columns: Optional[List[str]] = None):
        """
        Initializes the FlexTable instance with an optional list of header columns.

        :param header_columns: A list of header columns.
        """
        self.columns = ColumnsContainer()
        self.rows = RowsContainer()
        if header_columns is not None:
            self.add_columns(header_columns)

    # * ****************************************************************************************** *

    @property
    def header(self) -> List[str]:
        """
        Returns the header of the FlexTable instance.

        :return: The header of the FlexTable instance.
        """
        return self._header

    @header.setter
    def header(self, header: List[str]) -> None:
        """
        Sets the header of the FlexTable instance.

        :param header: A list of strings representing the header of the FlexTable instance.
        """
        self._header = header

    # * ****************************************************************************************** *

    @property
    def columns(self) -> ColumnsContainer:
        """
        Returns the columns of the FlexTable instance.

        :return: The columns of the FlexTable instance.
        """
        return self._columns

    @columns.setter
    def columns(self, columns: ColumnsContainer) -> None:
        """
        Sets the ColumnsContainer instance containing the table columns.

        :param columns: ColumnsContainer instance containing the table columns.
        """
        self._columns = columns

    def add_column(self, column_key: Union[str, int], column_val: Union[Column, str]) -> 'FlexTable':
        """
        Adds a new column to the FlexTable instance.

        :param column_key: The key of the new column.
        :param column_val: A string or Column object representing the new column.
        :return: The updated FlexTable instance.
        """
        if isinstance(column_val, str):
            column_val = Column(column_val)
        elif isinstance(column_val, Column):
            column_key = column_val.title
        else:
            raise UnsupportedColumnTypeError.for_column_key_val(column_key, column_val)

        self.columns[column_key] = column_val

        return self

    def add_columns(self,  # noqa: WPS234
                    columns: Optional[Union[List[Union[str, Column]], Dict[str, Union[str, Column]]]]) -> 'FlexTable':
        """
        Adds multiple columns at once. Note columns are registered in the order they are present in source data.

        Note that this method **auto-creates** column keys for all **non-string** table keys. For such case,
        the key will be derived either from passed `str` for from `Column`'s title string. All explicitly
        specified `str` keys will be preserved and used.

        :param columns The `Columns` to be added, given either via instance of `Column` or as string to be
               used as column title (for which instance of `Column` will be automatically created).
        """
        if columns is None:
            return self

        if isinstance(columns, list):
            self.add_columns_from_list(columns)
        elif isinstance(columns, dict):
            self.add_columns_from_dict(columns)
        else:
            raise TypeError(f'Unsupported columns data type: {type(columns)}')

        return self

    def add_columns_from_list(self, columns: List):
        for column_val in columns:
            self.add_column(column_val, column_val)

    def add_columns_from_dict(self, columns: Dict[str, Union[str, Column]]):
        for column_key, column_val in columns.items():
            if isinstance(column_key, int):
                if isinstance(column_val, str):
                    pass
                elif isinstance(column_val, Column):
                    column_val = column_val.title
                else:
                    raise TypeError(f'Unsupported column data type: {type(column_val)}')

            self.add_column(column_key, column_val)

    # * ****************************************************************************************** *

    @property
    def column_count(self) -> int:
        """
        The number of columns in the table.

        :return: The number of columns.
        """
        return len(self.columns)

    # * ****************************************************************************************** *

    @property
    def rows(self) -> RowsContainer:
        return self._rows

    @rows.setter
    def rows(self, rows: RowsContainer) -> None:
        self._rows = rows

    @property
    def row_count(self) -> int:
        return len(self.rows)

    def add_row(self, src_row: Optional[Union[Row, List, Dict]]) -> None:
        """
        Appends new row to the end of table.

        :param src_row: When a list or dictionary is given, it is expected that each of the columns represents
                        the row's cell value. The elements should be either instances of the Cell class or string|int.
                        If a primitive is given, an instance of Cell will automatically be created. The dictionary
                        elements can be in the form columnKey => value or can be provided as a list without their
                        own keys. In the latter case, the proper columnKey will be selected based on the table column
                        definitions (i.e., for srcRow being ['a', 'b'], the b value will be placed into the cell of
                        the second column). This auto-assignment works only when srcRow is a list with no custom keys
                        and table column definitions all use string keys. In all other cases, an explicit column's key
                        must be given. Passing None as src_row has no effect.
        """
        if src_row is None:
            return

        column_keys = list(self.columns.keys())

        row = src_row
        if isinstance(src_row, list):
            row = self.add_row_from_list(src_row, column_keys)
        elif isinstance(src_row, dict):
            row = self.add_row_from_dict(src_row, column_keys)
        else:
            row.add_cells(src_row)

        for column_key, cell in row.items():
            self.columns[column_key].update_max_width(len(cell.value))

        row_id = len(self.rows)
        self.rows[row_id] = row

    def add_row_from_list(self, src_row: List, column_keys: List) -> Row:
        row = Row()

        for list_idx, item in enumerate(src_row):
            column_key = self.columns.get_key_by_index(list_idx)
            row.add_cell(column_key, item)
            if list_idx >= len(column_keys):
                # FIXME: add option to configure FlexTable to raise an error in such case
                break
        return row

    def add_row_from_dict(self, src_row: Dict, column_keys: List) -> Row:
        row = Row()

        src_row_keys = list(src_row)
        items_to_add_count = len(src_row)

        # If src_row is a dict and has only numeric keys, and column definitions are using non-numeric keys,
        # then it is assumed that source elements are to be treated as organized in sequence. They will be
        # automatically assigned to cell at position matching their index in source dataset.
        int_keys_count = len(list(filter(lambda key: isinstance(key, int), src_row_keys)))
        src_has_num_keys_only = items_to_add_count == int_keys_count

        columns_str_keys_count = len(list(filter(lambda key: isinstance(key, str), column_keys)))
        columns_have_string_keys_only = columns_str_keys_count == len(column_keys)

        if src_has_num_keys_only and columns_have_string_keys_only:
            item_idx = 0
            for column_key, column_val in src_row.items():
                row.add_cell(column_key, column_val)

                if (item_idx + 1) >= len(column_keys):
                    # FIXME: add option to configure FlexTable to raise an error in such case
                    break
                item_idx += 1
        else:
            row.add_cells(src_row)

        return row

    def add_rows(self, rows: List[Union[Row, List, Dict]]) -> 'FlexTable':
        """
        Adds multiple rows in a batch.
        """
        for row in rows:
            self.add_row(row)

        return self

    # * ****************************************************************************************** *

    def render(self, renderer: Optional[RendererContract] = None) -> str:
        return self.render_as_str(renderer)

    def render_as_str(self, renderer: Optional[RendererContract] = None, end='\n') -> str:
        if renderer is None:
            renderer = FancyRenderer()
        return renderer.render_as_str(self, end)

    def render_as_list(self, renderer: Optional[RendererContract] = None) -> List[str]:
        if renderer is None:
            renderer = FancyRenderer()
        return renderer.render_as_list(self)

    def __repr__(self):
        return self.render_as_str()

    # * ****************************************************************************************** *

    def __contains__(self, column_key: Union[str, int]) -> bool:
        return column_key in self.columns

    def get_column(self, column_key: Union[str, int]) -> Column:
        return self.columns[column_key]

    # * ****************************************************************************************** *

    def set_column_align(self, column_key: Union[str, int], align: Align) -> 'FlexTable':
        """
        Helper method that sets both cell and title alignment for a specific column.

        :param Union[str, int] column_key: Table column ID, referring to the column you want to target.
        :param align: Target alignment to apply to the whole column (title and data cells)
        """
        self.set_title_align(column_key, align)
        self.set_cell_align(column_key, align)
        return self

    def set_title_align(self, column_key: Union[str, int], align: Align) -> 'FlexTable':
        """
        Sets title alignment for a specific column.

        ::param Union[str, int] column_key: Table column ID, referring to the column you want to target.
        :param Align align: Target alignment to apply to the column title header.
        """
        self.columns[column_key].title_align = align
        return self

    def set_cell_align(self, column_key: Union[str, int], align: Align) -> 'FlexTable':
        """
        Sets cell alignment for a specific column.

        :param Union[str, int] column_key: Table column ID, referring to the column you want to target.
        :param Align align: Target alignment to apply to the data cells of the columns.
        """
        self.columns[column_key].align = align
        return self

    def set_column_max_width(self, column_key: Union[str, int], max_width: int) -> 'FlexTable':
        """
        Sets the maximum width for a specific column.

        :param Union[str, int] column_key: Table column ID, referring to the column you want to target.
        :param int max_width: Maximum width to apply to the column. Cell exceeding this value will be truncated.
        """
        self.columns[column_key].max_width = max_width
        return self

    def hide_column(self, column_key: Union[str, int, List]) -> 'FlexTable':
        """
        Hides one or multiple columns in the table. Attempt to hide hidden column is safe.

        :param Union[str, int] column_key: Table column ID, referring to the column you want to target.
        """
        keys = column_key if isinstance(column_key, list) else [column_key]
        for key in keys:
            self.set_column_visibility(key, visible=False)
        return self

    def show_column(self, column_key: Union[str, int, List]) -> 'FlexTable':
        """
        Reveals formerly hidden columns in the table. Attempt to show visible column is safe.

        :param Union[str, int] column_key: Table column ID, referring to the column you want to target.
        """
        keys = column_key if isinstance(column_key, list) else [column_key]
        for key in keys:
            self.set_column_visibility(key, visible=True)
        return self

    def set_column_visibility(self, column_key: Union[str, int], visible: bool) -> 'FlexTable':
        """
        Sets the visibility of a specific column.

        :param Union[str, int] column_key: Table column ID, referring to the column you want to target.
        :param visible: True to make the column visible, False to hide it.
        """
        self.columns[column_key].visible = visible
        return self

    @property
    def visible_column_count(self) -> int:
        """
        Returns the number of visible columns
        """
        return len(list(filter(lambda column: column.visible, self.columns.values())))
