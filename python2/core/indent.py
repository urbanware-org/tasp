#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# ============================================================================
# TaSp - Consitent file indentation tool
# Indentation core module
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

def indent(directory, file_ext, spaces=4, padding=12, left_justify=False,
           recursive=False, overwrite=False, verbose=False):
    """
        Method to perform the indentation process.
    """
    pv.path(directory, "input", False, True)
    pv.string(file_ext, "file extension", False, None)
    pv.intvalue(spaces, "spaces", True, False, False)
    pv.intvalue(padding, "padding", True, False, False)

    directory = os.path.abspath(directory)
    spaces = int(spaces)
    padding = int(padding)
    num = 1

    if verbose:
        print "\nGathering files to process. Please wait.\n"

    list_files = common.get_files(directory, file_ext, recursive)

    if len(list_files) == 0:
        if verbose:
            print "No files to process.\n"
            return

    just = len(str(len(list_files)))
    for file_input in list_files:
        if verbose:
            print "Processing file %s of %s: '%s'" % \
                (str(num).rjust(just, " "), str(len(list_files)), file_input)
            num += 1

        if overwrite:
            __indent_file(file_input, spaces, padding, left_justify)
        else:
            __indent_copy(file_input, spaces, padding, left_justify)

    if verbose:
        print "\nFinished.\n"

def __indent_copy(file_input, spaces, padding, left_justify):
    """
        Core method to perform the indentation process without manipulating
        the input file (processed data will be written into a file with the
        same name and the additional suffix ".tasp").
    """
    file_output = file_input + ".tasp"
    fh_input = open(file_input, "r")
    fh_output = open(file_output, "w")
    for line in fh_input:
        fh_output.write(__process_line(line, spaces, padding, left_justify))
    fh_input.close()
    fh_output.close()

def __indent_file(file_input, spaces, padding, left_justify):
    """
        Core method to perform the indentation process and overwrite the input
        file with the processed data.
    """
    fd_temp, file_temp = tempfile.mkstemp()
    fh_input = open(file_input, "r")
    fh_temp = open(file_temp, "w")
    for line in fh_input:
        fh_temp.write(__process_line(line, spaces, padding, left_justify))
    fh_input.close()
    fh_temp.close()
    os.close(fd_temp)
    os.rename(file_temp, file_input)

def __process_line(line, spaces, padding, left_justify):
    """
        Core method to indent each line.
    """
    while (" " * 3) in line:
        line = line.replace((" " * 3), (" " * 2))

    temp = line.strip()
    if left_justify and len(temp) == 1:
        newline = temp + "\r\n"
    else:
        list_line = line.split("  ")
        newline = ""
        for i in range(len(list_line)):
            sp_remain = padding - len(list_line[i])
            if sp_remain < 1:
                newline += list_line[i] + (" " * spaces)
            else:
                newline += list_line[i] + (" " * sp_remain)

        newline = newline.strip() + "\r\n"
        if line.startswith(" "):
            newline = (" " * spaces) + newline

    return newline

# EOF

