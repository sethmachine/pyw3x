"""

"""


import ctypes
import os
import sys

SCRIPT_PATH = os.path.dirname(__file__)
MAC_STORM = os.path.join(SCRIPT_PATH, 'data/storm/libStorm.dylib')
WIN_64_STORM = os.path.join(SCRIPT_PATH, 'data/storm/win-64/Storm.dll')
STORM_DLL = ''

# determine OS
if os.name == 'nt': #assume all Windows is 64 bit, no 32 bit support
    STORM_DLL = WIN_64_STORM
elif os.name == 'posix': #macOS hopefully
    STORM_DLL = MAC_STORM
else:
    sys.stderr.write('Unsupported operating system detected {}.  Use macOS or Windows 64 bit to use StormLib.\n'.format(os.name))

STORM = ctypes.cdll.LoadLibrary(STORM_DLL)
STORM_VERBOSE = False

def _errcheck(result, func, args):
    if STORM_VERBOSE:
        print('ERRCHECK', result, func, args)
    return result

def GetLastError():
    return STORM['GetLastError']()

def SFileSetLocale(lcNewLocale):
    """
    :param lcNewLocale: LCID
    :return: LCID
    """
    func = getattr(STORM, "SFileSetLocale")
    func.errcheck = _errcheck
    return func(lcNewLocale)

def SFileOpenArchive(szMpqName, dwPriority, dwFlags, phMpq):
    """
    :param szMpqName: const TCHAR *
    :param dwPriority: DWORD
    :param dwFlags: DWORD
    :param phMpq: HANDLE *
    :return: bool
    """
    func = getattr(STORM, "SFileOpenArchive")
    func.errcheck = _errcheck
    return func(szMpqName, dwPriority, dwFlags, phMpq)

def SFileCreateArchive(szMpqName, dwCreateFlags, dwMaxFileCount, phMpq):
    """
    :param szMpqName: const TCHAR *
    :param dwCreateFlags: DWORD
    :param dwMaxFileCount: DWORD
    :param phMpq: HANDLE *
    :return: bool
    """
    func = getattr(STORM, "SFileCreateArchive")
    func.errcheck = _errcheck
    return func(szMpqName, dwCreateFlags, dwMaxFileCount, phMpq)

def SFileCreateArchive2(szMpqName, pCreateInfo, phMpq):
    """
    :param szMpqName: const TCHAR *
    :param pCreateInfo: PSFILE_CREATE_MPQ
    :param phMpq: HANDLE *
    :return: bool
    """
    func = getattr(STORM, "SFileCreateArchive2")
    func.errcheck = _errcheck
    return func(szMpqName, pCreateInfo, phMpq)

def SFileSetDownloadCallback(hMpq, DownloadCB, pvUserData):
    """
    :param hMpq: HANDLE
    :param DownloadCB: SFILE_DOWNLOAD_CALLBACK
    :param pvUserData: void *
    :return: bool
    """
    func = getattr(STORM, "SFileSetDownloadCallback")
    func.errcheck = _errcheck
    return func(hMpq, DownloadCB, pvUserData)

def SFileFlushArchive(hMpq):
    """
    :param hMpq: HANDLE
    :return: bool
    """
    func = getattr(STORM, "SFileFlushArchive")
    func.errcheck = _errcheck
    return func(hMpq)

def SFileCloseArchive(hMpq):
    """
    :param hMpq: HANDLE
    :return: bool
    """
    func = getattr(STORM, "SFileCloseArchive")
    func.errcheck = _errcheck
    return func(hMpq)

def SFileAddListFile(hMpq, szListFile):
    """
    :param hMpq: HANDLE
    :param szListFile: const TCHAR *
    :return: int
    """
    func = getattr(STORM, "SFileAddListFile")
    func.errcheck = _errcheck
    return func(hMpq, szListFile)

def SFileSetCompactCallback(hMpq, CompactCB, pvUserData):
    """
    :param hMpq: HANDLE
    :param CompactCB: SFILE_COMPACT_CALLBACK
    :param pvUserData: void *
    :return: bool
    """
    func = getattr(STORM, "SFileSetCompactCallback")
    func.errcheck = _errcheck
    return func(hMpq, CompactCB, pvUserData)

def SFileCompactArchive(hMpq, szListFile, bReserved):
    """
    :param hMpq: HANDLE
    :param szListFile: const TCHAR *
    :param bReserved: bool
    :return: bool
    """
    func = getattr(STORM, "SFileCompactArchive")
    func.errcheck = _errcheck
    return func(hMpq, szListFile, bReserved)

def SFileGetMaxFileCount(hMpq):
    """
    :param hMpq: HANDLE
    :return: DWORD
    """
    func = getattr(STORM, "SFileGetMaxFileCount")
    func.errcheck = _errcheck
    return func(hMpq)

def SFileSetMaxFileCount(hMpq, dwMaxFileCount):
    """
    :param hMpq: HANDLE
    :param dwMaxFileCount: DWORD
    :return: bool
    """
    func = getattr(STORM, "SFileSetMaxFileCount")
    func.errcheck = _errcheck
    return func(hMpq, dwMaxFileCount)

def SFileGetAttributes(hMpq):
    """
    :param hMpq: HANDLE
    :return: DWORD
    """
    func = getattr(STORM, "SFileGetAttributes")
    func.errcheck = _errcheck
    return func(hMpq)

def SFileSetAttributes(hMpq, dwFlags):
    """
    :param hMpq: HANDLE
    :param dwFlags: DWORD
    :return: bool
    """
    func = getattr(STORM, "SFileSetAttributes")
    func.errcheck = _errcheck
    return func(hMpq, dwFlags)

def SFileUpdateFileAttributes(hMpq, szFileName):
    """
    :param hMpq: HANDLE
    :param szFileName: const char *
    :return: bool
    """
    func = getattr(STORM, "SFileUpdateFileAttributes")
    func.errcheck = _errcheck
    return func(hMpq, szFileName)

def SFileOpenPatchArchive(hMpq, szPatchMpqName, szPatchPathPrefix, dwFlags):
    """
    :param hMpq: HANDLE
    :param szPatchMpqName: const TCHAR *
    :param szPatchPathPrefix: const char *
    :param dwFlags: DWORD
    :return: bool
    """
    func = getattr(STORM, "SFileOpenPatchArchive")
    func.errcheck = _errcheck
    return func(hMpq, szPatchMpqName, szPatchPathPrefix, dwFlags)

def SFileIsPatchedArchive(hMpq):
    """
    :param hMpq: HANDLE
    :return: bool
    """
    func = getattr(STORM, "SFileIsPatchedArchive")
    func.errcheck = _errcheck
    return func(hMpq)

def SFileHasFile(hMpq, szFileName):
    """
    :param hMpq: HANDLE
    :param szFileName: const char *
    :return: bool
    """
    func = getattr(STORM, "SFileHasFile")
    func.errcheck = _errcheck
    return func(hMpq, szFileName)

def SFileOpenFileEx(hMpq, szFileName, dwSearchScope, phFile):
    """
    :param hMpq: HANDLE
    :param szFileName: const char *
    :param dwSearchScope: DWORD
    :param phFile: HANDLE *
    :return: bool
    """
    func = getattr(STORM, "SFileOpenFileEx")
    func.errcheck = _errcheck
    return func(hMpq, szFileName, dwSearchScope, phFile)

def SFileGetFileSize(hFile, pdwFileSizeHigh):
    """
    :param hFile: HANDLE
    :param pdwFileSizeHigh: LPDWORD
    :return: DWORD
    """
    func = getattr(STORM, "SFileGetFileSize")
    func.errcheck = _errcheck
    return func(hFile, pdwFileSizeHigh)

def SFileSetFilePointer(hFile, lFilePos, plFilePosHigh, dwMoveMethod):
    """
    :param hFile: HANDLE
    :param lFilePos: LONG
    :param plFilePosHigh: LONG *
    :param dwMoveMethod: DWORD
    :return: DWORD
    """
    func = getattr(STORM, "SFileSetFilePointer")
    func.errcheck = _errcheck
    return func(hFile, lFilePos, plFilePosHigh, dwMoveMethod)

def SFileReadFile(hFile, lpBuffer, dwToRead, pdwRead, lpOverlapped):
    """
    :param hFile: HANDLE
    :param lpBuffer: void *
    :param dwToRead: DWORD
    :param pdwRead: LPDWORD
    :param lpOverlapped: LPOVERLAPPED
    :return: bool
    """
    func = getattr(STORM, "SFileReadFile")
    func.errcheck = _errcheck
    return func(hFile, lpBuffer, dwToRead, pdwRead, lpOverlapped)

def SFileCloseFile(hFile):
    """
    :param hFile: HANDLE
    :return: bool
    """
    func = getattr(STORM, "SFileCloseFile")
    func.errcheck = _errcheck
    return func(hFile)

def SFileGetFileInfo(hMpqOrFile, InfoClass, pvFileInfo, cbFileInfo, pcbLengthNeeded):
    """
    :param hMpqOrFile: HANDLE
    :param InfoClass: SFileInfoClass
    :param pvFileInfo: void *
    :param cbFileInfo: DWORD
    :param pcbLengthNeeded: LPDWORD
    :return: bool
    """
    func = getattr(STORM, "SFileGetFileInfo")
    func.errcheck = _errcheck
    return func(hMpqOrFile, InfoClass, pvFileInfo, cbFileInfo, pcbLengthNeeded)

def SFileGetFileName(hFile, szFileName):
    """
    :param hFile: HANDLE
    :param szFileName: char *
    :return: bool
    """
    func = getattr(STORM, "SFileGetFileName")
    func.errcheck = _errcheck
    return func(hFile, szFileName)

def SFileFreeFileInfo(pvFileInfo, InfoClass):
    """
    :param pvFileInfo: void *
    :param InfoClass: SFileInfoClass
    :return: bool
    """
    func = getattr(STORM, "SFileFreeFileInfo")
    func.errcheck = _errcheck
    return func(pvFileInfo, InfoClass)

def SFileExtractFile(hMpq, szToExtract, szExtracted, dwSearchScope):
    """
    :param hMpq: HANDLE
    :param szToExtract: const char *
    :param szExtracted: const TCHAR *
    :param dwSearchScope: DWORD
    :return: bool
    """
    func = getattr(STORM, "SFileExtractFile")
    func.errcheck = _errcheck
    return func(hMpq, szToExtract, szExtracted, dwSearchScope)

def SFileGetFileChecksums(hMpq, szFileName, pdwCrc32, pMD5):
    """
    :param hMpq: HANDLE
    :param szFileName: const char *
    :param pdwCrc32: LPDWORD
    :param pMD5: char *
    :return: bool
    """
    func = getattr(STORM, "SFileGetFileChecksums")
    func.errcheck = _errcheck
    return func(hMpq, szFileName, pdwCrc32, pMD5)

def SFileVerifyFile(hMpq, szFileName, dwFlags):
    """
    :param hMpq: HANDLE
    :param szFileName: const char *
    :param dwFlags: DWORD
    :return: DWORD
    """
    func = getattr(STORM, "SFileVerifyFile")
    func.errcheck = _errcheck
    return func(hMpq, szFileName, dwFlags)

def SFileVerifyRawData(hMpq, dwWhatToVerify, szFileName):
    """
    :param hMpq: HANDLE
    :param dwWhatToVerify: DWORD
    :param szFileName: const char *
    :return: int
    """
    func = getattr(STORM, "SFileVerifyRawData")
    func.errcheck = _errcheck
    return func(hMpq, dwWhatToVerify, szFileName)

def SFileSignArchive(hMpq, dwSignatureType):
    """
    :param hMpq: HANDLE
    :param dwSignatureType: DWORD
    :return: bool
    """
    func = getattr(STORM, "SFileSignArchive")
    func.errcheck = _errcheck
    return func(hMpq, dwSignatureType)

def SFileVerifyArchive(hMpq):
    """
    :param hMpq: HANDLE
    :return: DWORD
    """
    func = getattr(STORM, "SFileVerifyArchive")
    func.errcheck = _errcheck
    return func(hMpq)

def SFileFindFirstFile(hMpq, szMask, lpFindFileData, szListFile):
    """
    :param hMpq: HANDLE
    :param szMask: const char *
    :param lpFindFileData: SFILE_FIND_DATA *
    :param szListFile: const TCHAR *
    :return: HANDLE
    """
    func = getattr(STORM, "SFileFindFirstFile")
    func.errcheck = _errcheck
    return func(hMpq, szMask, lpFindFileData, szListFile)

def SFileFindNextFile(hFind, lpFindFileData):
    """
    :param hFind: HANDLE
    :param lpFindFileData: SFILE_FIND_DATA *
    :return: bool
    """
    func = getattr(STORM, "SFileFindNextFile")
    func.errcheck = _errcheck
    return func(hFind, lpFindFileData)

def SFileFindClose(hFind):
    """
    :param hFind: HANDLE
    :return: bool
    """
    func = getattr(STORM, "SFileFindClose")
    func.errcheck = _errcheck
    return func(hFind)

def SListFileFindFirstFile(hMpq, szListFile, szMask, lpFindFileData):
    """
    :param hMpq: HANDLE
    :param szListFile: const TCHAR *
    :param szMask: const char *
    :param lpFindFileData: SFILE_FIND_DATA *
    :return: HANDLE
    """
    func = getattr(STORM, "SListFileFindFirstFile")
    func.errcheck = _errcheck
    return func(hMpq, szListFile, szMask, lpFindFileData)

def SListFileFindNextFile(hFind, lpFindFileData):
    """
    :param hFind: HANDLE
    :param lpFindFileData: SFILE_FIND_DATA *
    :return: bool
    """
    func = getattr(STORM, "SListFileFindNextFile")
    func.errcheck = _errcheck
    return func(hFind, lpFindFileData)

def SListFileFindClose(hFind):
    """
    :param hFind: HANDLE
    :return: bool
    """
    func = getattr(STORM, "SListFileFindClose")
    func.errcheck = _errcheck
    return func(hFind)

def SFileEnumLocales(hMpq, szFileName, plcLocales, pdwMaxLocales, dwSearchScope):
    """
    :param hMpq: HANDLE
    :param szFileName: const char *
    :param plcLocales: LCID *
    :param pdwMaxLocales: LPDWORD
    :param dwSearchScope: DWORD
    :return: int
    """
    func = getattr(STORM, "SFileEnumLocales")
    func.errcheck = _errcheck
    return func(hMpq, szFileName, plcLocales, pdwMaxLocales, dwSearchScope)

def SFileCreateFile(hMpq, szArchivedName, FileTime, dwFileSize, lcLocale, dwFlags, phFile):
    """
    :param hMpq: HANDLE
    :param szArchivedName: const char *
    :param FileTime: ULONGLONG
    :param dwFileSize: DWORD
    :param lcLocale: LCID
    :param dwFlags: DWORD
    :param phFile: HANDLE *
    :return: bool
    """
    func = getattr(STORM, "SFileCreateFile")
    func.errcheck = _errcheck
    return func(hMpq, szArchivedName, FileTime, dwFileSize, lcLocale, dwFlags, phFile)

def SFileWriteFile(hFile, pvData, dwSize, dwCompression):
    """
    :param hFile: HANDLE
    :param pvData: const void *
    :param dwSize: DWORD
    :param dwCompression: DWORD
    :return: bool
    """
    func = getattr(STORM, "SFileWriteFile")
    func.errcheck = _errcheck
    return func(hFile, pvData, dwSize, dwCompression)

def SFileFinishFile(hFile):
    """
    :param hFile: HANDLE
    :return: bool
    """
    func = getattr(STORM, "SFileFinishFile")
    func.errcheck = _errcheck
    return func(hFile)

def SFileAddFileEx(hMpq, szFileName, szArchivedName, dwFlags, dwCompression, dwCompressionNext):
    """
    :param hMpq: HANDLE
    :param szFileName: const TCHAR *
    :param szArchivedName: const char *
    :param dwFlags: DWORD
    :param dwCompression: DWORD
    :param dwCompressionNext: DWORD
    :return: bool
    """
    func = getattr(STORM, "SFileAddFileEx")
    func.errcheck = _errcheck
    return func(hMpq, szFileName, szArchivedName, dwFlags, dwCompression, dwCompressionNext)

def SFileAddFile(hMpq, szFileName, szArchivedName, dwFlags):
    """
    :param hMpq: HANDLE
    :param szFileName: const TCHAR *
    :param szArchivedName: const char *
    :param dwFlags: DWORD
    :return: bool
    """
    func = getattr(STORM, "SFileAddFile")
    func.errcheck = _errcheck
    return func(hMpq, szFileName, szArchivedName, dwFlags)

def SFileAddWave(hMpq, szFileName, szArchivedName, dwFlags, dwQuality):
    """
    :param hMpq: HANDLE
    :param szFileName: const TCHAR *
    :param szArchivedName: const char *
    :param dwFlags: DWORD
    :param dwQuality: DWORD
    :return: bool
    """
    func = getattr(STORM, "SFileAddWave")
    func.errcheck = _errcheck
    return func(hMpq, szFileName, szArchivedName, dwFlags, dwQuality)

def SFileRemoveFile(hMpq, szFileName, dwSearchScope):
    """
    :param hMpq: HANDLE
    :param szFileName: const char *
    :param dwSearchScope: DWORD
    :return: bool
    """
    func = getattr(STORM, "SFileRemoveFile")
    func.errcheck = _errcheck
    return func(hMpq, szFileName, dwSearchScope)

def SFileRenameFile(hMpq, szOldFileName, szNewFileName):
    """
    :param hMpq: HANDLE
    :param szOldFileName: const char *
    :param szNewFileName: const char *
    :return: bool
    """
    func = getattr(STORM, "SFileRenameFile")
    func.errcheck = _errcheck
    return func(hMpq, szOldFileName, szNewFileName)

def SFileSetFileLocale(hFile, lcNewLocale):
    """
    :param hFile: HANDLE
    :param lcNewLocale: LCID
    :return: bool
    """
    func = getattr(STORM, "SFileSetFileLocale")
    func.errcheck = _errcheck
    return func(hFile, lcNewLocale)

def SFileSetDataCompression(DataCompression):
    """
    :param DataCompression: DWORD
    :return: bool
    """
    func = getattr(STORM, "SFileSetDataCompression")
    func.errcheck = _errcheck
    return func(DataCompression)

def SFileSetAddFileCallback(hMpq, AddFileCB, pvUserData):
    """
    :param hMpq: HANDLE
    :param AddFileCB: SFILE_ADDFILE_CALLBACK
    :param pvUserData: void *
    :return: bool
    """
    func = getattr(STORM, "SFileSetAddFileCallback")
    func.errcheck = _errcheck
    return func(hMpq, AddFileCB, pvUserData)

def SCompImplode(pvOutBuffer, pcbOutBuffer, pvInBuffer, cbInBuffer):
    """
    :param pvOutBuffer: void *
    :param pcbOutBuffer: int *
    :param pvInBuffer: void *
    :param cbInBuffer: int
    :return: int
    """
    func = getattr(STORM, "SCompImplode")
    func.errcheck = _errcheck
    return func(pvOutBuffer, pcbOutBuffer, pvInBuffer, cbInBuffer)

def SCompExplode(pvOutBuffer, pcbOutBuffer, pvInBuffer, cbInBuffer):
    """
    :param pvOutBuffer: void *
    :param pcbOutBuffer: int *
    :param pvInBuffer: void *
    :param cbInBuffer: int
    :return: int
    """
    func = getattr(STORM, "SCompExplode")
    func.errcheck = _errcheck
    return func(pvOutBuffer, pcbOutBuffer, pvInBuffer, cbInBuffer)

def SCompCompress(pvOutBuffer, pcbOutBuffer, pvInBuffer, cbInBuffer, uCompressionMask, nCmpType, nCmpLevel):
    """
    :param pvOutBuffer: void *
    :param pcbOutBuffer: int *
    :param pvInBuffer: void *
    :param cbInBuffer: int
    :param uCompressionMask: unsigned
    :param nCmpType: int
    :param nCmpLevel: int
    :return: int
    """
    func = getattr(STORM, "SCompCompress")
    func.errcheck = _errcheck
    return func(pvOutBuffer, pcbOutBuffer, pvInBuffer, cbInBuffer, uCompressionMask, nCmpType, nCmpLevel)

def SCompDecompress(pvOutBuffer, pcbOutBuffer, pvInBuffer, cbInBuffer):
    """
    :param pvOutBuffer: void *
    :param pcbOutBuffer: int *
    :param pvInBuffer: void *
    :param cbInBuffer: int
    :return: int
    """
    func = getattr(STORM, "SCompDecompress")
    func.errcheck = _errcheck
    return func(pvOutBuffer, pcbOutBuffer, pvInBuffer, cbInBuffer)

def SCompDecompress2(pvOutBuffer, pcbOutBuffer, pvInBuffer, cbInBuffer):
    """
    :param pvOutBuffer: void *
    :param pcbOutBuffer: int *
    :param pvInBuffer: void *
    :param cbInBuffer: int
    :return: int
    """
    func = getattr(STORM, "SCompDecompress2")
    func.errcheck = _errcheck
    return func(pvOutBuffer, pcbOutBuffer, pvInBuffer, cbInBuffer)