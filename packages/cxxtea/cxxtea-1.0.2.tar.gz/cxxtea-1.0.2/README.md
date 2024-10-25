# cxxtea

`cxxtea` is a Python package for decrypting data, using a custom XXTEA decryption algorithm implemented in C, and supporting ABI3-compatible wheels for multiple operating systems and architectures.

## Features

- Provides efficient XXTEA decryption functionality, based on C implementation.
- Supports Python 3.7+, and uses the [Python Limited API (abi3)](https://docs.python.org/3/c-api/stable.html) to ensure compatibility of binary wheels across multiple Python versions.
- Automatically build and publish via GitHub Actions, supporting Windows, macOS, and Linux (including musllinux and manylinux).

## Installation

Install the latest version of `cxxtea` from PyPI:

```bash
pip install cxxtea
