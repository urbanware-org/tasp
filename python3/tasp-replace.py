#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ============================================================================
# TaSp - Consitent file indentation tool
# Replacement script
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
    from core import replace as r

    try:
        p = clap.Parser()
    except Exception as e:
        print("%s: error: %s" % (os.path.basename(sys.argv[0]), e))
        sys.exit(1)

    p.set_description("Replace tabs inside of files with a user-defined "
                      "amount of spaces and vice versa.")
    p.set_epilog("Further information and usage examples can be found inside "
                 "the documentation file for this script.")

    # Required arguments
    p.add_avalue("-d", "--directory", "directory that contains the files " \
                 "to process", "directory", None, True)
    p.add_avalue("-f", "--file-extension", "file extension of the files to " \
                 "process", "file_ext", None, True)
    p.add_predef("-m", "--indentation-mode", "indentation method to use",
                 "mode", ["spaces", "tabs"], True)
    p.add_avalue("-s", "--spaces", "amount of spaces used to replace a tab " \
                 "or to get replaced by a tab (depending on the "
                 "indentation mode)", "spaces", None, True)

    # Optional arguments
    p.add_switch(None, "--confirm", "skip the confirmation prompt and " \
                 "instantly process the data (in case the '--overwrite' " \
                 "argument was given)", "confirm", True, False)
    p.add_switch("-h", "--help", "print this help message and exit", None,
                 True, False)
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
        print(r.get_version())
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

        r.replace(args.directory, args.file_ext, args.mode, args.spaces,
                  args.recursive, args.overwrite, args.verbose)
    except Exception as e:
        p.error(e)

if __name__ == "__main__":
    main()

# EOF

