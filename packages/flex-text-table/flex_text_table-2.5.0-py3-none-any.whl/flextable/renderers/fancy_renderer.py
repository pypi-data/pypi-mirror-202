####################################################################
#
# Flex Table
# Fast and flexible Pyhon library for text tables.
#
# Copyright ©2023 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/python-flex-table/
#
####################################################################

from flextable.renderers.ascii_table_renderer import AsciiTableRenderer


class FancyRenderer(AsciiTableRenderer):
    ROW_FRAME_LEFT = '│ '
    ROW_FRAME_CENTER = ' │ '
    ROW_FRAME_RIGHT = ' │'

    SEGMENT_ROW_FILL = '─'
    SEGMENT_FIRST_ROW_LEFT = '┌─'
    SEGMENT_FIRST_ROW_CENTER = '─┬─'
    SEGMENT_FIRST_ROW_RIGHT = '─┐'
    SEGMENT_ROW_LEFT = '├─'
    SEGMENT_ROW_CENTER = '─┼─'
    SEGMENT_ROW_RIGHT = '─┤'
    SEGMENT_LAST_ROW_LEFT = '└─'
    SEGMENT_LAST_ROW_CENTER = '─┴─'
    SEGMENT_LAST_ROW_RIGHT = '─┘'
