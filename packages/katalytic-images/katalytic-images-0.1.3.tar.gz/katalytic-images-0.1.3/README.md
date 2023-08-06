## Description
TODO: Let people know what your project can do specifically. Provide context and add a link to any reference visitors might be unfamiliar with. A list of Features or a Background subsection can also be added here. If there are alternatives to your project, this is a good place to list differentiating factors.

[![version](https://img.shields.io/pypi/v/katalytic-images)](https://pypi.org/project/katalytic-images/)
[![Build Status](https://app.travis-ci.com/katalytic/katalytic-images.svg?branch=main)](https://app.travis-ci.com/gitlab/katalytic/katalytic-images)
[![Test Results](https://img.shields.io/travis/com/katalytic/katalytic-images?label=tests)](https://app.travis-ci.com/gitlab/katalytic/katalytic-images)
[![Coverage Status](https://coveralls.io/repos/gitlab/katalytic/katalytic-images/badge.svg?branch=main)](https://coveralls.io/gitlab/katalytic/katalytic-images?branch=main)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Installation
By itself
```bash
pip install katalytic-images
```

As part of the [katalytic](https://gitlab.com/katalytic/katalytic) collection
```bash
pip install katalytic
```

## Usage
TODO: Use examples liberally, and show the expected output if you can. It's helpful to have inline the smallest example of usage that you can demonstrate, while providing links to more sophisticated examples if they are too long to reasonably include in the README.

## Roadmap
- make pillow an optional dependency.
	- setup_load_image() should pick opencv if pillow is not available
- drawing on images with a declarative interface
- image thresholding and masking operations
- interactive data exploration widgets (maybe as part of another package)
- higher level API on top of opencv

## Contributing
Contributions can be made in a number of ways:
- Propose architectural or API improvements
- Propose new features
- Propose packaging, building, or deployment improvements
- Report and fix bugs
	- you can also submit an xfail test
- Submit code and tests
- Tell me what I'm doing wrong or when I'm not following best practices
- Update the documentation

