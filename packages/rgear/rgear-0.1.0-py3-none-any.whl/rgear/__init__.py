#!/usr/bin/env python3
"""
Command line utility to generate various types of helper script for using R in Domino
"""

import argparse
import os.path
import sys

__version__ = "0.1.0"


# TEMPLATES

SHINY_APP_START = """\
# Simple shiny app startup script for use on Domino
# Generated with rgear (https://github.com/sellorm/rgear)
R -e 'shiny::runApp("{}", host="0.0.0.0", port=8888)'
"""

PLUMBER_APP_START = """\
# Simple plumber API startup scriptt for use on Domino
# Generated with rgear (https://github.com/sellorm/rgear)
R -e 'plumber::pr_run(plumber::pr("{}"), host = "0.0.0.0", port = 8888)'
"""

RMARKDOWN_APP_START = """\
# quick web server for serving an Rmarkdown docuent for use on Domino
# Generated with rgear (https://github.com/sellorm/rgear)
python3 -m http.server --bind "0.0.0.0" 8888
"""

RMARKDOWN_APP_INDEX = """\
<!DOCTYPE html>
<!-- redirect to the actual content -->
<!-- Generated with rgear (https://github.com/sellorm/rgear) -->
<html>
    <head>
        <meta http-equiv="refresh" content="0; URL={}" />
    </head>
</html>
"""


## Helper functions


def file_exists(file, print_err=True):
    """Check for a file and print an error if it already exists

    Keyword Arguments:
    file      -- path to a file to check
    print_err -- whether to print an error and exit (default: True)

    Returns:
    Boolean unless print_err is set, in which case it exits before it returns
    """
    if os.path.isfile(file):
        if print_err:
            print(f"Error: The file, {file}, already exists.")
            print("       Please check and try again.")
            sys.exit(1)
        return True
    return False


def file_does_not_exist(file, print_err=True):
    """
    Check for a file and print an error is it does not exist.

    Keyword Arguments:
    file      -- path to a file to check
    print_err -- whether to print an error and exit (default: True)

    Returns:
    Boolean unless print_err is set, in which case it exits before it returns
    """
    if os.path.isfile(file):
        if print_err:
            print(f"Error: The file, {file}, does not exist.")
            print("       Please check and try again.")
            sys.exit(1)
        return True
    return False


# File generator functions


def generate_shiny(shiny_app, overwrite=False, verbose=False):
    """
    Generates helper file for serving shiny apps

    Keyword Arguments:
    shiny_app      -- path to your shiny app
    overwrite      -- whether to overwrite existing helper files
    verbose        -- prints more verbose output

    Generated file:
    * app.sh -- starts the shiny app with Domino specific parameters
    """
    print("Generating app.sh...")
    if not overwrite:
        file_exists("app.sh", print_err=True)
    file_does_not_exist(shiny_app, print_err=True)
    with open("app.sh", "w", encoding="utf8") as file:
        file.write(SHINY_APP_START.format(shiny_app))
    if verbose:
        print("---- app.sh ----")
        print(SHINY_APP_START.format(shiny_app))
    print("Complete.")


def generate_rmarkdown(rmarkdown_html, overwrite=False, verbose=False):
    """
    Generates helper files for serving Rmarkdown documents

    Keyword Arguments:
    rmarkdown_html -- path to your Rmarkdown file's html output
    overwrite      -- whether to overwrite existing helper files
    verbose        -- prints more verbose output

    Generated files:
    * app.sh     -- starts a webserver to serve the generated Rmarkdown html
    * index.html -- Redirects default browser path to the Rmarkdown page
    """
    print("Generating app.sh and index.html...")
    if not overwrite:
        file_exists("app.sh", print_err=True)
    if not overwrite:
        file_exists("index.html", print_err=True)
    file_does_not_exist(rmarkdown_html, print_err=True)
    with open("app.sh", "w", encoding="utf8") as file:
        file.write(RMARKDOWN_APP_START)
    if verbose:
        print("---- app.sh ----")
        print(RMARKDOWN_APP_START)
    with open("index.html", "w", encoding="utf8") as file:
        file.write(RMARKDOWN_APP_INDEX.format(rmarkdown_html))
    if verbose:
        print("---- app.sh ----")
        print(RMARKDOWN_APP_INDEX.format(rmarkdown_html))
    print("Complete.")


def generate_plumber(plumber_file, overwrite=False, verbose=False):
    """
    Generates helper files for serving plumber APIs

    Keyword Arguments:
    plumber_file   -- path to your plumber file to serve
    overwrite      -- whether to overwrite existing helper files
    verbose        -- prints more verbose output

    Generated file:
    * app.sh -- starts the plumber API with Domino specific parameters
    """
    print("Generating app.sh...")
    if not overwrite:
        file_exists("app.sh", print_err=True)
    file_does_not_exist(plumber_file, print_err=True)
    with open("app.sh", "w", encoding="utf8") as file:
        file.write(PLUMBER_APP_START.format(plumber_file))
    if verbose:
        print("---- app.sh ----")
        print(PLUMBER_APP_START.format(plumber_file))
    print("Complete.")


# Main
def cli_arg_parser(args=None):
    """
    CLI argument parsing (extracted from main to make testing easier)
    """
    parser = argparse.ArgumentParser(
        prog="rgear",
        description="Generates R helpers for Domino",
        epilog="For detailed help, please see https://github.com/sellorm/rgear",
    )
    parser.add_argument(
        "content_type",
        help="Choose the application type you want to serve",
        choices=["shiny", "plumber", "rmarkdown"],
    )
    parser.add_argument("path", help="path to the content to serve")
    parser.add_argument(
        "-f",
        "--force",
        help="Forces overwrite if the output file(s) already exist",
        action="store_true",
    )
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument('--version', action='version', version= __version__)
    return parser.parse_args(args)


def main():
    """
    Pulls everything together and runs the command line tool
    """
    args = cli_arg_parser(sys.argv[1:])

    if args.content_type == "shiny":
        generate_shiny(args.path, overwrite=args.force, verbose=args.verbose)

    if args.content_type == "rmarkdown":
        generate_rmarkdown(args.path, overwrite=args.force, verbose=args.verbose)

    if args.content_type == "plumber":
        generate_plumber(args.path, overwrite=args.force, verbose=args.verbose)


if __name__ == "__main__":
    main()
