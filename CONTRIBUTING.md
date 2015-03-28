# Contributing

[![Build Status](https://travis-ci.org/photoshell/photoshell.svg)](https://travis-ci.org/photoshell/photoshell)
[![Coverage Status](https://img.shields.io/coveralls/photoshell/photoshell.svg)](https://coveralls.io/r/photoshell/photoshell)

The source for **photoshell** can be found on [GitHub][source]. Or simply:

    git clone git://github.com/photoshell/photoshell

All code must follow PEP8 standards. Before doing anything, be sure to install
and configure [pre-commit][precommit]. If your code doesn't pass our pre-commit
tests, it won't be merged. It should also have full test coverage, and build
(obviously).

Finally, your code should be compatible with Python 3 (see `tox.ini` for the
versions we actually test against; needless to say, the entire test matrix
should pass).

[source]: https://github.com/photoshell/photoshell
[precommit]: http://pre-commit.com/
