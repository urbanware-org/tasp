#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# ============================================================================
# TaSp - Consitent file indentation tool
# Replacement core module
# Copyright (C) 2018 by Ralf Kilian
# Distributed under the MIT License (https://opensource.org/licenses/MIT)
#
# Website: http://www.urbanware.org
# GitHub: https://github.com/urbanware-org/tasp
# ============================================================================

__version__ = "2.0.10"

import common
import os
import paval as pv
import tempfile

def get_version():
    """
        Return the version of this module.
    """
    return __version__

def replace(directory, file_ext, mode, spaces=8, recursive=False,
            overwrite=False, verbose=True):
    """
        Method to perform the replacement process.
    """
    pv.path(directory, "input", False, True)
    pv.string(file_ext, "file extension", False, None)
    mode = mode.lower()
    pv.compstr(mode, "mode", ["spaces", "tabs"])
    pv.intvalue(spaces, "spaces", True, False, False)

    directory = os.path.abspath(directory)
    spaces = int(spaces)
    num = 1

    if verbose:
        print "\nGathering files to process. Please wait.\n"

    list_files = common.get_files(directory, file_ext, recursive)
    just = len(str(len(list_files)))
    for file_input in list_files:
        if verbose:
            print "Processing file %s of %s: '%s'" % \
                (str(num).rjust(just, " "), str(len(list_files)), file_input)
            num += 1

        if overwrite:
            __replace_file(file_input, mode, spaces)
        else:
            __replace_copy(file_input, mode, spaces)

    if verbose:
        print "\nFinished.\n"

def __replace_copy(file_input, mode, spaces):
    """
        Core method to perform the replacement process without manipulating
        the input file (processed data will be written into a file with the
        same name and the additional suffix ".tasp").
    """
    file_output = file_input + ".tasp"
    fh_input = open(file_input, "r")
    fh_output = open(file_output, "w")
    for line in fh_input:
        fh_output.write(__process_line(line, mode, spaces))
    fh_input.close()
    fh_output.close()

def __replace_file(file_input, mode, spaces):
    """
        Core method to perform the replacement process and overwrite the input
        file with the processed data.
    """
    fd_temp, file_temp = tempfile.mkstemp()
    fh_input = open(file_input, "r")
    fh_temp = open(file_temp, "w")
    for line in fh_input:
        fh_temp.write(__process_line(line, mode, spaces))
    fh_input.close()
    fh_temp.close()
    os.close(fd_temp)
    os.rename(file_temp, file_input)

def __process_line(line, mode, spaces):
    """
        Core method to replace tabs with spaces and vice versa.
    """
    if mode == "spaces":
        return line.replace("\t", (" " * spaces))
    else:
        return line.replace((" " * spaces), "\t")

# EOF

