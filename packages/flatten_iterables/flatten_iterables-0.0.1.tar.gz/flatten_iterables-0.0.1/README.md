# Flatten Iterables

## Introduction

Flatten Iterables uses iteration (no recursion) in order to flatten iterables into a dictionary where each key is a reference path and each value is the value at the respective path.

## Features

- Produces valid Python reference paths for string and numeric keys.
- Raises `ValueError` on circular references.
- Iterative algorithm; hence no call stack overflow.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Test](#test)

## <h2 id="installation">Installation</h2>

```bash
pip install flatten_iterables
```

## <h2 id="usage">Usage</h2>

In this example, an object named `data` will be flattened into a dictionary of reference paths and their respective values. The resulting dictionary will be dumped to a JSON string.

```python
import json
from flatten_iterables import flatten, mappables, iterables

data = {
    "dict": {"a": 42},
    "list": [42],
    "nested_dicts": {"a0": {"b0": 42, "b1": 23}},
    "nested_lists": [
        [
            42,
        ],
    ],
    ...: 42,
}

print(json.dumps(flatten(data), indent=2))
```

```bash
{
  "['dict']['a']": 42,
  "['list'][0]": 42,
  "['nested_dicts']['a0']['b0']": 42,
  "['nested_dicts']['a0']['b1']": 23,
  "['nested_lists'][0][0]": 42,
  "[Ellipsis]": 42
}
```

## <h2 id="test">Test</h2>

Clone the repository.

```bash
git clone https://github.com/faranalytics/flatten_iterables.git
```

Change directory into the root of the repository.

```bash
cd flatten_iterables
```

Run the tests.

```bash
python tests/test.py -v
```
