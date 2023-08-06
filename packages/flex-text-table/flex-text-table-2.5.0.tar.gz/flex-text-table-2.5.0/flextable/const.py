####################################################################
#
# Flex Table
# Fast and flexible Pyhon library for text tables.
#
# Copyright ©2023 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/python-flex-table/
#
####################################################################

from typing import List


class Const(object):
    APP_NAME: str = 'flex-text-table'
    APP_VERSION: str = '2.5.0'
    APP_URL: str = 'https://github.com/MarcinOrlowski/python-flex-table/'
    APP_SUMMARY = 'Fast and flexible Pyhon library for text tables.'
    APP_INITIAL_YEAR: int = 2023

    APP_DESCRIPTION: List[str] = [
        f'{APP_NAME} v{APP_VERSION} * Copyright {APP_INITIAL_YEAR} by Marcin Orlowski.',
        f'{APP_SUMMARY}',
        f'{APP_URL}',
    ]
