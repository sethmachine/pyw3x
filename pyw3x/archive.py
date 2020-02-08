"""

"""

import ctypes
import contextlib
import io
import os

import pyw3x.logger as logger
import pyw3x.stormlib as stormlib

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
    yield Archive(infile, handle, mode)
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

def write_listfile(data, outfile):
    with open(outfile, 'w') as f:
        f.write('\n'.join(data))
        f.write('\n')

class Archive():
    def __init__(self, infile, handle, mode):
        self.log = logger.get_log(Archive.__name__)
        self.infile = infile
        self.handle = handle
        self.mode = mode

    def compact(self, listfile):
        if self.mode != 'w':
            msg = 'Archive is not writable'.format(self.mode)
            self.log.error(msg)
            raise io.UnsupportedOperation(msg)
        if listfile is None:
            success = stormlib.SFileCompactArchive(self.handle, None, 0)
        else:
            success = stormlib.SFileCompactArchive(self.handle, listfile.encode('ascii'), 0)
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
                nested_dir = os.path.join(outdir, parent)
                if not os.path.exists(nested_dir):
                    os.makedirs(nested_dir)
            outfile = os.path.join(outdir, f)
            self.extract_file(f, outfile)
        return files

    def add_file(self, infile, name, replace_existing=True):
        """Adds a local file to the archive with the given name.

        By default, if there is a file in the archive with `name`, it gets replaced by
        the new file.

        Note when adding a new file name to the archive that did not exist before,
        the list file must be updated with the new file in order to allow compaction of the archive to succeed.

        :param infile:
        :param name:
        :param replace_existing:
        :return:
        """
        flags = stormlib.MPQ_FILE_COMPRESS
        if replace_existing:
            flags += stormlib.MPQ_FILE_REPLACEEXISTING
        compression = stormlib.MPQ_COMPRESSION_ZLIB
        success = stormlib.SFileAddFileEx(self.handle, infile.encode('ascii'), name.encode('ascii'), flags,
                                          compression, compression)
        return success


def add_file_example():
    i = 'data/test/Test-new.w3x'
    addme = 'data/test/foo.txt'
    listfile = 'data/test/list-new5555.txt'
    outdir = 'data/test/extract-new4'
    with open_archive(i, 'r') as a:
        a.extract_list_file(listfile)
        files = [x for x in read_listfile(listfile)]
        if addme not in files:
            files.append(addme)
        write_listfile(files, listfile)
    # with open_archive(i, 'w') as a:
    #     a.add_file(addme, addme)
    #     a.extract_all_files(outdir, listfile)
    #     if not a.compact(listfile):
    #         print('Failed to compact')


if __name__ == '__main__':
    # add_file_example()
    infile = '/users/sethmachine/desktop/amplayer5beta.scx'
    with open_archive(infile, 'r') as a:
        # a = Archive(infile, handle, 'r')
        a.extract_file('staredit\\scenario.chk', 'bar/foof.chk')
        # a.extract_list_file('data/sc-listfile.txt')
    #
    # i = 'data/test/Test-new.w3x'
    # # mode = 'w'
    # # with open_archive(i, 'w') as handle:
    # #     a = Archive(i, handle, 'w')
    # #     # if not a.add_file('readme.md', 'readme.md'):
    # #     #     print('Failed to add file')
    # #     listfile = 'list.txt'
    # #     if not a.extract_list_file(listfile):
    # #         print('Failed to extract list file')
    # #     # print(stormlib.STORM['GetLastError']())
    # #     if not a.compact(listfile):
    # #         print('Failed to compact')
    # #
    # with open_archive(i, 'r') as handle:
    #     a = Archive(i, handle, 'r')
    #     a.extract_list_file('foo.txt')
    #     a.extract_all_files('extract', 'foo.txt')




