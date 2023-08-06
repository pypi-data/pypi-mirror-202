# rgear - Generate R helper files

The aim of `rgear` is to provide simple tooling to create the necessary helper
files used by Domino Data Lab when serving R based content.

Supported content types:

* Shiny apps
* Rmarkdown html output
* Plumber APIs

## Installation

`rgear` is written in Python, and can be installed directly from PyPI:

```bash
# python3 -m pip install rgear
```

## Usage

```bash
rgear --help
```

```output
usage: rgear [-h] [-f] [-v] [--version] {shiny,plumber,rmarkdown} path

Generates R helpers for Domino

positional arguments:
  {shiny,plumber,rmarkdown}
                        Choose the application type you want to serve
  path                  path to the content to serve

optional arguments:
  -h, --help            show this help message and exit
  -f, --force           Forces overwrite if the output file(s) already exist
  -v, --verbose
  --version             show program's version number and exit

For detailed help, please see https://github.com/sellorm/rgear
```

Using the above options, various files -- mostly `app.sh` -- will be written to
the working directory with the required parameters already populated.

Domino Data Lab can then use these files to serve your content as a DDL "app".

## License

MIT License Copyright (c) 2023 Mark Sellors

See the `LICENSE` file for the full text of the license.

