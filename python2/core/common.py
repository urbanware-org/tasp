#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# ============================================================================
# TaSp - Consitent file indentation tool
# Common core module
# Copyright (C) 2018 by Ralf Kilian
# Distributed under the MIT License (https://opensource.org/licenses/MIT)
#
# Website: http://www.urbanware.org
# GitHub: https://github.com/urbanware-org/tasp
# ============================================================================

__version__ = "2.0.10"

import os
import paval as pv

def confirm_notice():
    """
        Display a notice which must be confirmed by the user to proceed.
    """
    proceed = False
    notice_text = """           o      o                     o              88
           8      8                                    88
           8      8 .oPYo. oPYo. odYo. o8 odYo. .oPYo. 88
           8  db  8 .oooo8 8  '' 8' '8  8 8' '8 8    8 88
           'b.PY.d' 8    8 8     8   8  8 8   8 8    8
            '8  8'  'YooP8 8     8   8  8 8   8 'YooP8 88
                                                .    8
                                                'oooP'

Please use this tool with care to avoid data damage or loss!

There is no function to undo the changes done by this tool, so you
should be aware of what you are doing. Improper use (e. g. modifying
files inside system directories) will corrupt your system!

If you wish to proceed, type the word 'CONFIRM' (in uppercase, without
any quotes or spaces) and press <Return>. Otherwise, the process will
be cancelled."""

    print_text_box("", notice_text)
    choice = raw_input("> ")

    if choice == "CONFIRM":
        choice = "Proceeding."
        proceed = True
    else:
        choice = "cancelled."
    print "\n%s\n" % choice

    return proceed

def get_files(directory, file_ext, recursive=False):
    """
        Get the requested files inside the given directory.
    """
    pv.path(directory, "input", False, True)
    pv.string(file_ext, "file extension", False, None)

    list_files = []
    directory = os.path.abspath(directory)
    list_files = __get_files(directory, file_ext, recursive, list_files)
    list_files.sort()

    return list_files

def get_version():
    """
        Return the version of this module.
    """
    return __version__

def __get_files(directory, file_ext, recursive, list_files):
    """
        Core method that gets the requested files.
    """
    list_dirs = []
    for item in os.listdir(directory):
        path = os.path.join(directory, item)
        if os.path.isfile(path):
            if path.lower().endswith(file_ext.lower()):
                list_files.append(path)
        else:
            list_dirs.append(path)
    if recursive:
        for directory in list_dirs:
            __get_files(directory, file_ext, True, list_files)

    return list_files

def print_text_box(heading, text):
    """
        Print a text message outlined with an ASCII character frame.
    """
    heading = heading.strip()
    if len(heading) > 72:
        raise Exception("The text box heading must not be longer than 72 " \
                        "characters.")
    if text == "":
        raise Exception("The text box text must not be empty.")

    text_box = "\n+" + ("-" * 76) + "+" + \
               "\n|" + (" " * 76) + "|"
    if not heading == "":
        padding = int((72 - len(heading)) / 2)
        heading = (" " * (padding + 2) + heading).ljust(76, " ")
        text_box += ("\n|%s|\n|" + (" " * 76) + "|") % heading
    list_text = text.split("\n")
    for text in list_text:
        list_words = text.split(" ")
        count = 1
        line = ""
        for word in list_words:
            if len(line + word + " ") > 73:
                text_box += "\n|  " + line.ljust(74, " ") + "|"
                line = word + " "
            else:
                line = line + word + " "
            count += 1
            if count > len(list_words):
                text_box +=  "\n|  " + line.ljust(74, " ") + "|"
    text_box += "\n|" + (" " * 76) + "|" \
                "\n+" + ("-" * 76) + "+\n"

    print text_box

# EOF

