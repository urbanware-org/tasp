#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# ============================================================================
# TaSp - Consitent file indentation tool
# Indentation script
# Copyright (C) 2018 by Ralf Kilian
# Distributed under the MIT License (https://opensource.org/licenses/MIT)
#
# Website: http://www.urbanware.org
# GitHub: https://github.com/urbanware-org/tasp
# ============================================================================

import os
import sys

def main():
    from core import clap
    from core import common
    from core import indent as i

    try:
        p = clap.Parser()
    except Exception as e:
        print "%s: error: %s" % (os.path.basename(sys.argv[0]), e)
        sys.exit(1)

    p.set_description("Consistently indent messed up files (especially " \
                      "config files) using a user-defined amount of spaces.")
    p.set_epilog("Further information and usage examples can be found inside "
                 "the documentation file for this script.")

    # Required arguments
    p.add_avalue("-d", "--directory", "directory that contains the files " \
                 "to process", "directory", None, True)
    p.add_avalue("-f", "--file-extension", "file extension of the files to " \
                 "process", "file_ext", None, True)
    p.add_avalue("-p", "--padding", "padding (in spaces) used to indent " \
                 "each item inside a line", "padding", None, True)
    p.add_avalue("-s", "--spaces", "amount of leading spaces for each " \
                 "indented line", "spaces", None, True)

    # Optional arguments
    p.add_switch(None, "--confirm", "skip the confirmation prompt and " \
                 "instantly process the data (in case the '--overwrite' " \
                 "argument was given)", "confirm", True, False)
    p.add_switch("-h", "--help", "print this help message and exit", None,
                 True, False)
    p.add_switch("-l", "--left-justify", "left-justify the line if it only " \
                 "consists of a single character", "left_justify", True,
                 False)
    p.add_switch(None, "--overwrite", "overwrite the input file with the " \
                 "processed data (instead of creating an output file with " \
                 "the same name and the additional suffix '.tasp')",
                 "overwrite", True, False)
    p.add_switch("-r", "--recursive", "process the given directory " \
                 "recursively", "recursive", True, False)
    p.add_switch(None, "--verbose", "use verbose mode (print details while " \
                 "processing data)", "verbose", True, False)
    p.add_switch(None, "--version", "print the version number and exit", None,
                 True, False)

    if len(sys.argv) == 1:
        p.error("At least one required argument is missing.")
    elif ("-h" in sys.argv) or ("--help" in sys.argv):
        p.print_help()
        sys.exit(0)
    elif "--version" in sys.argv:
        print i.get_version()
        sys.exit(0)

    args = p.parse_args()
    try:
        if args.overwrite:
            if not args.confirm:
                if not common.confirm_notice():
                    sys.exit(0)
        else:
            if args.confirm:
                p.error("The '--confirm' argument only makes sense in " \
                        "combination with the '--overwrite' argument.")

        i.indent(args.directory, args.file_ext, args.spaces, args.padding,
                 args.left_justify, args.recursive, args.overwrite,
                 args.verbose)
    except Exception as e:
        p.error(e)

if __name__ == "__main__":
    main()

# EOF

