

import archive

infile = 'data/test/Test.w3x'
mode = 'r' #use 'w' to enable writing

with archive.open_archive(infile, mode) as a:
    listfile = 'list.txt'
    a.extract_list_file(listfile)
    outdir = 'archive-extracted'
    a.extract_all_files(outdir, listfile)