# HAICU-CTL

## Overview

A python-based command line utility for controlling and sequence programming the MLD1200

The available subcommands are:

- `discover`
- `data`
- `plot`
- `status`
- `read`
- `write`
- `set-config`
- `get-config`

## Installation

The recommended installation method is via pip

  To install:
    `pip install haicu-ctl`

  To upgrade:
    `pip install -U haicu-ctl`

  To run it locally from the source (from the `scripts/haicu-ctl` directory):
    `python -m haicu_ctl`

## Interactive

 Command:
  `haicu-ctl [-h] [-i INI_FILE] [-l LOGFILE] [discover|data|plot|status|read|write|set-config|get-config]`

 Purpose:
  Connects to an esper service located at `url` and opens an interactive shell

 Options:

  `-h` or `--help`
  Print out help for this subcommand

  `--verison`
  Print out current version

  `-i INI_FILE` or  `--ini`
   Ini file to use, will be created if using `get-config`

  `-v` or `--verbose`
   Increase logging level, can be used multiple times

  `-l LOG_FILE` or `--log LOG_FILE`
   Log to file instead of standard out
