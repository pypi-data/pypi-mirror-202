#!/usr/bin/env python

####################################################################
#
# Flex Table
# Fast and flexible Pyhon library for text tables.
#
# Copyright ©2023 Marcin Orlowski <mail [@] MarcinOrlowski.com>
# https://github.com/MarcinOrlowski/python-flex-table/
#
####################################################################
#
# python -m venv venv
# source venv/activate.fish
# pip install wheel twine
# python setup.py sdist bdist_wheel
# pip install --upgrade dist/flex_table-2.5.0-py3-none-any.whl
# twine upload dist/*
#

from flextable.const import Const
from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
    logo_url = 'https://raw.githubusercontent.com/MarcinOrlowski/python-flex-table/master/artwork/flex-table.png'
    readme = fh.read().replace(r'![flex-table logo](artwork/flex-table-logo.png)',
                               f'![flex-table logo]({logo_url})', 1)

    setup(
        name=Const.APP_NAME,
        version=Const.APP_VERSION,
        packages=find_packages(),

        install_requires=[
            # 'argparse>=1.4.0',
        ],
        python_requires='>=3.8',

        author='Marcin Orlowski',
        author_email='mail@marcinOrlowski.com',
        description=Const.APP_SUMMARY,
        long_description=readme,
        long_description_content_type='text/markdown',
        url=Const.APP_URL,
        keywords='text table ascii command line console shell',
        project_urls={
            'Bug Tracker': 'https://github.com/MarcinOrlowski/python-flex-table/issues/',
            'Documentation': 'https://github.com/MarcinOrlowski/python-flex-table/',
            'Source Code': 'https://github.com/MarcinOrlowski/python-flex-table/',
        },
        # https://choosealicense.com/
        license='MIT License',
        classifiers=[
            'Programming Language :: Python :: 3',
            'License :: OSI Approved :: MIT License',
            'Operating System :: OS Independent',
        ],
    )
