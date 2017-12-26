# -*- coding: utf-8 -*-

"""File system utility functions to simplify file manipulation.

.. moduleauthor:: Seth-David Donald Dworman <sdworman@brandeis.edu>

"""

import contextlib
import json
import os
import re
import shutil
import tempfile

@contextlib.contextmanager
def temp_filename():
    temp_dir = tempfile.mkdtemp()
    try:
        yield temp_dir
    finally:
        shutil.rmtree(temp_dir)

def absolute_filepaths(directory, depth=0, file_pattern=r'.+'):
    """Lists all files joined to directory path.

    Args:
        depth (int): How many subdirectories to explore.
                    A depth of 0 only explores the first subdirectory,
                    while a depth of -1 explores all subdirectories.
        file_pattern (str): Valid regular expression denoting which
                            files to yield in directory exploration.

    """
    file_re = re.compile(file_pattern)
    for x in os.listdir(directory):
        path = os.path.join(directory, x)
        if os.path.isfile(path):
            if file_re.search(path):
                yield path
        elif depth != 0:
            for f in absolute_filepaths(path, depth - 1, file_pattern):
                yield f

def absolute_dirpaths(directory, depth=0, file_pattern=r'.+'):
    """Lists all files joined to directory path.

    Args:
        depth (int): How many subdirectories to explore.
                    A depth of 0 only explores the first subdirectory,
                    while a depth of -1 explores all subdirectories.
        file_pattern (str): Valid regular expression denoting which
                            files to yield in directory exploration.

    """
    file_re = re.compile(file_pattern)
    for x in os.listdir(directory):
        path = os.path.join(directory, x)
        if os.path.isdir(path):
            if file_re.search(path):
                yield path
            if depth != 0:
                for f in absolute_dirpaths(path, depth - 1, file_pattern):
                    yield f

def read_file(filepath):
    """Reads file contents as string using `with` construct.

    """
    with open(filepath, 'r') as f:
        content = f.read()
    return content

def read_json(input_file):
    with open(input_file, 'r') as f:
        return json.load(f)

def write_file(filepath, content, safe=False):
    """Writes a new file using the `with` construct.

    """
    if safe and os.path.exists(filepath):
        return filepath
    with open(filepath, 'w') as f:
        f.write(content)
    return filepath

def write_json(output_file, obj, indent=1, safe=False):
    with open(output_file, 'w') as f:
        f.write(json.dumps(obj, indent=indent))
    return output_file

def append_file(content, filename):
    with open(filename, 'a') as f:
        print>>f, content

def read_list(filepath):
    lines = []
    with open(filepath, 'r') as f:
        for line in f:
            lines.append(line.strip('\n'))
    return lines

def write_list(items, filepath):
    with open(filepath, 'w') as f:
        l = len(items) - 1
        for i, item in enumerate(items):
            f.write(item)
            if i != l:
                f.write('\n')
    return filepath

def add_filename_suffix(filename, suffix):
    filename, file_extension = os.path.splitext(filename)
    new_filename = filename + suffix + file_extension
    return new_filename

def set_filename_extension(filename, new_extension):
    filename, file_extension = os.path.splitext(filename)
    new_filename = filename + new_extension
    return new_filename

def rmAndMakeDir(directory):
    if os.path.exists(directory):
        shutil.rmtree(directory)
    os.mkdir(directory)
    return directory

def truncate(f, n):
    """Truncates/pads a float f to n decimal places without rounding

    """
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])

if __name__ == '__main__':
    pass
    
    

