"""Generates Python StormLib API from the StormLib header and dynamic linked library.


import ctypes

MAC_STORM = 'data/storm/libStorm.dylib'

STORM = ctypes.cdll.LoadLibrary(MAC_STORM)
STORM_VERBOSE = True

def _errcheck(result, func, args):
    if STORM_VERBOSE:
        print ('ERRCHECK', result, func, args)
    return result

"""



import ctypes
import json
import os
import re

from pyw3x.stormlib_constants import *

STORM_LIB_HEADER = 'data/storm/StormLib.h'
MAC_STORM = 'data/storm/libStorm.dylib'

HEADER_DEFINE_RE = re.compile(r'^#define\s+(?P<name>\S+)\s+(?P<value>[a-z0-9]+)', re.UNICODE | re.IGNORECASE)

HEADER_FUNC_RE = re.compile(r'^(?P<ret>\S+)\s+(?P<api>\S+)\s+(?P<name>S[^\(]+)\((?P<args>[^\)]+)', re.UNICODE)

def storm_lib_header_to_constants(infile=STORM_LIB_HEADER, outfile='stormlib_constants.py'):
    data = []
    with open(infile, 'r') as f:
        for line in f:
            match = HEADER_DEFINE_RE.search(line)
            if match:
                data.append((match.group('name'), match.group('value')))
    out = '\n'.join(['{} = {}'.format(name, value) for (name,value) in data])
    with open(outfile, 'w') as f:
        f.write(out)
    return out

def argstr_to_param(argstr):
    parts = argstr.split()
    name = parts[-1].strip()
    out = ':param {}: {}'.format(name, ' '.join(parts[:-1]))
    return out

def match_to_pyfunc(match, api_name):
    argslist = match.group('args').split(', ')
    argslist = [x.strip() for x in argslist]
    funcargs = []
    for argstr in argslist:
        parts = argstr.split()
        name = parts[-1].strip()
        funcargs.append(name)
    s = 'def {}({}):'.format(match.group('name').strip(), ', '.join(funcargs))
    s += '\n    """\n'
    params = ['    ' + argstr_to_param(x) for x in argslist]
    s += '\n'.join(params)
    s += '\n    :return: {}'.format(match.group('ret'))
    s += '\n    """'
    s += '\n    '
    s += 'func = getattr({}, "{}")'.format(api_name, match.group('name').strip())
    s += '\n    '
    s += 'func.errcheck = _errcheck'
    s += '\n    '
    s += 'return func({})'.format(', '.join(funcargs))
    return s

def export_storm_lib_functions(infile=STORM_LIB_HEADER, outfile='stormlib_functions.py', dll=MAC_STORM):
    """

    :param infile:
    :param outfile:
    :param dll:
    :return:
    """
    data = []
    with open(infile, 'r') as f:
        for line in f:
            match = HEADER_FUNC_RE.search(line)
            if match:
                data.append(match_to_pyfunc(match, 'STORM'))
    with open(outfile, 'w') as f:
        f.write('\n\n'.join(data))




if __name__ == '__main__':
    pass
    # export_storm_lib_functions()
    # s = ctypes.cdll.LoadLibrary(MAC_STORM)