# batcharray

<p align="center">
    <a href="https://github.com/durandtibo/batcharray/actions">
        <img alt="CI" src="https://github.com/durandtibo/batcharray/workflows/CI/badge.svg">
    </a>
    <a href="https://github.com/durandtibo/batcharray/actions">
        <img alt="Nightly Tests" src="https://github.com/durandtibo/batcharray/workflows/Nightly%20Tests/badge.svg">
    </a>
    <a href="https://github.com/durandtibo/batcharray/actions">
        <img alt="Nightly Package Tests" src="https://github.com/durandtibo/batcharray/workflows/Nightly%20Package%20Tests/badge.svg">
    </a>
    <br/>
    <a href="https://durandtibo.github.io/batcharray/">
        <img alt="Documentation" src="https://github.com/durandtibo/batcharray/workflows/Documentation%20(stable)/badge.svg">
    </a>
    <a href="https://durandtibo.github.io/batcharray/">
        <img alt="Documentation" src="https://github.com/durandtibo/batcharray/workflows/Documentation%20(unstable)/badge.svg">
    </a>
    <br/>
    <a href="https://codecov.io/gh/durandtibo/batcharray">
        <img alt="Codecov" src="https://codecov.io/gh/durandtibo/batcharray/branch/main/graph/badge.svg">
    </a>
    <a href="https://codeclimate.com/github/durandtibo/batcharray/maintainability">
        <img src="https://api.codeclimate.com/v1/badges/9907f3838df3b9a1cba8/maintainability" />
    </a>
    <a href="https://codeclimate.com/github/durandtibo/batcharray/test_coverage">
        <img src="https://api.codeclimate.com/v1/badges/9907f3838df3b9a1cba8/test_coverage" />
    </a>
    <br/>
    <a href="https://github.com/psf/black">
        <img  alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg">
    </a>
    <a href="https://google.github.io/styleguide/pyguide.html#s3.8-comments-and-docstrings">
        <img  alt="Doc style: google" src="https://img.shields.io/badge/%20style-google-3666d6.svg">
    </a>
    <a href="https://github.com/astral-sh/ruff">
        <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff" style="max-width:100%;">
    </a>
    <a href="https://github.com/guilatrova/tryceratops">
        <img  alt="Doc style: google" src="https://img.shields.io/badge/try%2Fexcept%20style-tryceratops%20%F0%9F%A6%96%E2%9C%A8-black">
    </a>
    <br/>
    <a href="https://pypi.org/project/batcharray/">
        <img alt="PYPI version" src="https://img.shields.io/pypi/v/batcharray">
    </a>
    <a href="https://pypi.org/project/batcharray/">
        <img alt="Python" src="https://img.shields.io/pypi/pyversions/batcharray.svg">
    </a>
    <a href="https://opensource.org/licenses/BSD-3-Clause">
        <img alt="BSD-3-Clause" src="https://img.shields.io/pypi/l/batcharray">
    </a>
    <br/>
    <a href="https://pepy.tech/project/batcharray">
        <img  alt="Downloads" src="https://static.pepy.tech/badge/batcharray">
    </a>
    <a href="https://pepy.tech/project/batcharray">
        <img  alt="Monthly downloads" src="https://static.pepy.tech/badge/batcharray/month">
    </a>
    <br/>
</p>

## Overview

`batcharray` is lightweight library built on top of [NumPy](https://numpy.org/doc/stable/index.html)
to manipulate nested data structure with NumPy arrays.
This library provides functions for arrays where the first axis is the batch axis.
It also provides functions for arrays representing a batch of sequences where the first axis
is the batch axis and the second axis is the sequence axis.

- [Motivation](#motivation)
- [Documentation](https://durandtibo.github.io/batcharray/)
- [Installation](#installation)
- [Contributing](#contributing)
- [API stability](#api-stability)
- [License](#license)

## Motivation

Let's imagine you have a batch which is represented by a dictionary with three arrays, and you want
to take the first 2 items.
`batcharray` provides the function `slice_along_batch` that allows to slide all the arrays:

```pycon

>>> import numpy as np
>>> from batcharray.nested import slice_along_batch
>>> batch = {
...     "a": np.array([[2, 6], [0, 3], [4, 9], [8, 1], [5, 7]]),
...     "b": np.array([4, 3, 2, 1, 0]),
...     "c": np.array([1.0, 2.0, 3.0, 4.0, 5.0]),
... }
>>> slice_along_batch(batch, stop=2)
{'a': array([[2, 6], [0, 3]]), 'b': array([4, 3]), 'c': array([1., 2.])}

```

Similarly, it is possible to split a batch in multiple batches by using the
function `split_along_batch`:

```pycon

>>> import numpy as np
>>> from batcharray.nested import split_along_batch
>>> batch = {
...     "a": np.array([[2, 6], [0, 3], [4, 9], [8, 1], [5, 7]]),
...     "b": np.array([4, 3, 2, 1, 0]),
...     "c": np.array([1.0, 2.0, 3.0, 4.0, 5.0]),
... }
>>> split_along_batch(batch, split_size_or_sections=2)
[{'a': array([[2, 6], [0, 3]]), 'b': array([4, 3]), 'c': array([1., 2.])},
 {'a': array([[4, 9], [8, 1]]), 'b': array([2, 1]), 'c': array([3., 4.])},
 {'a': array([[5, 7]]), 'b': array([0]), 'c': array([5.])}]

```

Please check the documentation to see all the implemented functions.

## Documentation

- [latest (stable)](https://durandtibo.github.io/batcharray/): documentation from the latest stable
  release.
- [main (unstable)](https://durandtibo.github.io/batcharray/main/): documentation associated to the
  main branch of the repo. This documentation may contain a lot of work-in-progress/outdated/missing
  parts.

## Installation

We highly recommend installing
a [virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).
`batcharray` can be installed from pip using the following command:

```shell
pip install batcharray
```

To make the package as slim as possible, only the minimal packages required to use `batcharray` are
installed.
To include all the dependencies, you can use the following command:

```shell
pip install batcharray[all]
```

Please check the [get started page](https://durandtibo.github.io/batcharray/get_started) to see how
to install only some specific dependencies or other alternatives to install the library.
The following is the corresponding `batcharray` versions and tested dependencies.

| `batcharray` | `coola`        | `numpy`       | `python`      |
|--------------|----------------|---------------|---------------|
| `main`       | `>=0.8.4,<1.0` | `>=1.22,<3.0` | `>=3.9,<3.14` |
| `0.1.0`      | `>=0.8.4,<1.0` | `>=1.22,<3.0` | `>=3.9,<3.14` |
| `0.0.3`      | `>=0.3,<1.0`   | `>=1.22,<3.0` | `>=3.9,<3.13` |
| `0.0.2`      | `>=0.3,<1.0`   | `>=1.22,<2.0` | `>=3.9,<3.13` |
| `0.0.1`      | `>=0.3,<1.0`   | `>=1.22,<2.0` | `>=3.9,<3.13` |

<sup>*</sup> indicates an optional dependency

## Contributing

Please check the instructions in [CONTRIBUTING.md](.github/CONTRIBUTING.md).

## Suggestions and Communication

Everyone is welcome to contribute to the community.
If you have any questions or suggestions, you can
submit [Github Issues](https://github.com/durandtibo/batcharray/issues).
We will reply to you as soon as possible. Thank you very much.

## API stability

:warning: While `batcharray` is in development stage, no API is guaranteed to be stable from one
release to the next.
In fact, it is very likely that the API will change multiple times before a stable 1.0.0 release.
In practice, this means that upgrading `batcharray` to a new version will possibly break any code
that was using the old version of `batcharray`.

## License

`batcharray` is licensed under BSD 3-Clause "New" or "Revised" license available
in [LICENSE](LICENSE) file.
