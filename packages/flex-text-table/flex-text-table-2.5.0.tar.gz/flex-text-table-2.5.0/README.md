# Flex Table

Fast and flexible Pyhon library for text tables.

[![Unit tests](https://github.com/MarcinOrlowski/python-flex-table/actions/workflows/unittests.yml/badge.svg?branch=master)](https://github.com/MarcinOrlowski/python-flex-table/actions/workflows/unittests.yml)
[![MD Lint](https://github.com/MarcinOrlowski/python-flex-table/actions/workflows/markdown.yml/badge.svg?branch=master)](https://github.com/MarcinOrlowski/python-flex-table/actions/workflows/markdown.yml)
[![GitHub issues](https://img.shields.io/github/issues/MarcinOrlowski/python-flex-table.svg)](https://github.com/MarcinOrlowski/python-flex-table/issues)

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/flex-table.svg)](https://badge.fury.io/py/flex-table)
[![Downloads](https://img.shields.io/pypi/dm/flex-table)](https://pypi.org/project/flex-table/)
[![Python Version](https://img.shields.io/pypi/pyversions/flex-table.svg)](https://pypi.org/project/flex-table/)
[![Wheel](https://img.shields.io/pypi/wheel/flex-table.svg)](https://pypi.org/project/flex-table/)
[![Format](https://img.shields.io/pypi/format/flex-table.svg)](https://pypi.org/project/flex-table/)
[![Implementation](https://img.shields.io/pypi/implementation/flex-table.svg)](https://pypi.org/project/flex-table/)
[![Status](https://img.shields.io/pypi/status/flex-table.svg)](https://pypi.org/project/flex-table/)

Library is also available as [PHP package](https://github.com/MarcinOrlowski/php-text-table).

---

Table of contents

1. [Features](#features)
1. [Installation & requirements](docs/setup.md)
1. [Examples](docs/examples.md)
1. [License](#license)

---

## Features

1. Simple API, easy to use,
2. Lightweight (no additional dependencies),
3. Production ready.

---

## Usage examples

Simples possible usage:

```python
table = FlexTable(['ID', 'NAME', 'SCORE']);
table.add_rows({
    [1, 'John', 12],
    [2, 'Tommy', 15],
});
print(table.render_as_str())
```

would produce nice text table:

```python
┌────┬───────┬───────┐
│ ID │ NAME  │ SCORE │
├────┼───────┼───────┤
│ 1  │ John  │ 12    │
│ 2  │ Tommy │ 15    │
└────┴───────┴───────┘
```

See more [usage examples](docs/examples.md).

---

## License

* Written and copyrighted &copy;2023 by Marcin Orlowski <mail (#) marcinorlowski (.) com>
* Text Table is open-sourced software licensed under
  the [MIT license](http://opensource.org/licenses/MIT)
