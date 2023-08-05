# Django MUID
    
[![Build Status](https://travis-ci.org/bradleyayers/django-muid.svg?branch=master)](https://travis-ci.org/bradleyayers/django-muid)
[![Coverage Status](https://coveralls.io/repos/github/bradleyayers/django-muid/badge.svg?branch=master)](https://coveralls.io/github/bradleyayers/django-muid?branch=master)
[![PyPI version](https://badge.fury.io/py/django-muid.svg)](https://badge.fury.io/py/django-muid)
[![PyPI](https://img.shields.io/pypi/pyversions/django-muid.svg)](https://pypi.python.org/pypi/django-muid)
[![PyPI](https://img.shields.io/pypi/l/django-muid.svg)](https://pypi.python.org/pypi/django-muid)

A package for generating and validating MUIDs (Micro Unique IDs) in Django.

MUID objects are immutable, hashable, and usable as dictionary keys. Converting a MUID to a string with str() yields something in the form '8OV50-Qalh-x6ygB'.

## Features

- Generate MUIDs with MUID()
- Validate MUIDs with muid_validator()
- Use MUIDs as primary keys in Django models
- Use MUIDField to store MUIDs in Django models
- Generate MicroQrCode images with MUID.to_micro_qr_code()
- Generate AztecCode images with MUID.to_aztec_code()

## Installation

`pip install django-muid`

## Usage

Import the MUID class, MUIDField, and muid_validator from the package and use them in your Django project.

## Contributing

Contributions to Django MUID are welcome! To contribute, fork the repository and create a pull request. Please make sure to follow the guidelines in CONTRIBUTING.md.

## License

Django MUID is licensed under the MIT License. See LICENSE.md for more information.