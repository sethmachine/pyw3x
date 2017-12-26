"""

"""

import ctypes
import contextlib
import io
import os

import logger
import stormlib

STORM_LOG = logger.get_log('stormlib')

WAR3MAP_J = 'war3map.j'
WAR3MAP_W3E = 'war3map.w3e'

@contextlib.contextmanager
def open_archive(infile, mode='r'):
    if mode == 'r':
        flags = stormlib.STREAM_FLAG_READ_ONLY
    elif mode == 'w':
        flags = stormlib.STREAM_FLAG_WRITE_SHARE
    handle = ctypes.c_void_p()
    ret = stormlib.SFileOpenArchive(infile.encode('ascii'), 0, flags, ctypes.byref(handle))
    if ret == 0:
        msg = 'Failed to open archive {} with error code {}'.format(infile, ret)
        STORM_LOG.error(msg)
        raise Exception(msg)
    msg = 'Successfully opened archive {}'.format(infile)
    STORM_LOG.debug(msg)
    yield handle
    ret = stormlib.SFileCloseArchive(handle)
    if ret == 0:
        msg = 'Failed to close archive {} with error code {}'.format(infile, ret)
        STORM_LOG.error(msg)
        raise Exception(msg)
    msg = 'Successfully closed archive {}'.format(infile)
    STORM_LOG.debug(msg)

def read_listfile(listfile):
    with open(listfile, 'r') as f:
        for line in f:
            out = line.strip()
            if out:
                yield out

class Archive():
    def __init__(self, infile, handle, mode):
        self.log = logger.get_log(Archive.__name__)
        self.infile = infile
        self.handle = handle
        self.mode = mode

    def compact(self):
        if self.mode != 'w':
            msg = 'Archive is not writable'.format(self.mode)
            self.log.error(msg)
            raise io.UnsupportedOperation(msg)
        success = stormlib.SFileCompactArchive(self.handle, "foof.txt".encode('ascii'), 0)
        return success

    def extract_list_file(self, outfile):
        success = stormlib.SFileExtractFile(self.handle, "(listfile)".encode('ascii'),
                                        outfile.encode('ascii'), stormlib.SFILE_OPEN_FROM_MPQ)
        return success

    def extract_file(self, infile, outfile):
        """

        :param infile: Name of the file to extract
        :param outfile: Name of the local file to write extracted file to
        :return: 1 if successful, 0 otherwise
        """
        success = stormlib.SFileExtractFile(self.handle, infile.encode('ascii'),
                                            outfile.encode('ascii'), stormlib.SFILE_OPEN_FROM_MPQ)
        return success

    def extract_jass(self, outfile):
        return self.extract_file(WAR3MAP_J, outfile)

    def extract_terrain(self, outfile):
        return self.extract_file(WAR3MAP_W3E, outfile)

    def extract_all_files(self, outdir, listfile=None):
        """Extracts all files from the given list file.

        """
        if not listfile:
            pass
        if not os.path.exists(outdir):
            os.mkdir(outdir)
        files = [x for x in read_listfile(listfile)]
        for f in files:
            parent = os.path.dirname(f)
            if parent:
                os.makedirs(os.path.join(outdir, parent))
            outfile = os.path.join(outdir, f)
            self.extract_file(f, outfile)
        return files





if __name__ == '__main__':
    i = 'data/test/Test.w3x'
    mode = 'r'
    with open_archive(i, mode) as handle:
        a = Archive(i, handle, mode)
        a.extract_list_file('foo.txt')
        a.extract_jass('foof.jass')
        a.extract_terrain('foof.w3e')
        a.extract_all_files('extract', 'foo.txt')




