"""

"""

import ctypes
import os

SCRIPT_PATH = os.path.dirname(__file__)

from stormlib_constants import *
from stormlib_functions import *

if __name__ == '__main__':
    i = os.path.join(SCRIPT_PATH, 'data/test/Test.w3x')
    # assert os.path.exists(i)
    handle = ctypes.c_void_p()
    ret = SFileOpenArchive(i.encode('ascii'), 0, STREAM_FLAG_READ_ONLY, ctypes.byref(handle))
    print(ret)
    ret = SFileExtractFile(handle, "(listfile)".encode('ascii'), "list.txt".encode('ascii'), SFILE_OPEN_FROM_MPQ)