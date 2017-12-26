# Hive World Editor (Python)

This project is a Python wrapper around the [StormLib C++ API](https://github.com/ladislav-zezula/StormLib) 
and also ports C++ code from the [HiveWE project](https://github.com/stijnherfst/HiveWE) to parse Warcraft III
map files including terrain (war3map.w3e).  

The StormLib wrapper allows reading and writing to MPQ archives, Blizzard's properietary format 
used throughout their games.  Warcraft III map files (.w3x and .w3m) are essentially MPQ archives, 
which allows for potential automatic generation of Warcraft III maps.  

This wrapper exports most of the constants and `S` MPQ functions into Python wrappers as defined in the 
[StormLib header](https://github.com/ladislav-zezula/StormLib/blob/master/src/StormLib.h) by using
regular expressions on the header file.  This allows for smarter completion of StormLib functions
and constants (usually flags) in a Python IDE.  Nevertheless, always be prepared to consult 
the [StormLib documentation](http://www.zezula.net/en/mpq/stormlib.html) on the `S` MPQ functions.


## Requirements

1.  StormLib dynamically linked library compiled for target OS.  
This wrapper uses the macOS DLL, `libStorm.dylib`.  Build instructions and static DLLs are provided
on the [StormLib GitHub repository](https://github.com/ladislav-zezula/StormLib).  
2.  Python 3.6.x (not tested on Python 2.7.x).
3.  Python requirements (use `pip install -r requirements.txt`).



## Usage

An `Archive` class is provided in *archive.py*.  A context manager is used to handle
opening and closing of a provided archive, therefore all archive operations should
occur with the context scope.  Note that strings in Python 3.6.x by default are unicode--
these need to be explicitly encoded as `ascii` when passed to the StormLib API, e.g. `mystring.encode('ascii')`.

Below is an example that extracts all the files from the archive `listfile` into 
an output directory.  

```python
import archive

infile = 'data/test/Test.w3x'
mode = 'r' #use 'w' to enable writing

with archive.open_archive(infile, mode) as a:
    listfile = 'list.txt'
    a.extract_list_file(listfile)
    outdir = 'archive-extracted'
    a.extract_all_files(outdir, listfile)
```

```
$ ls archive-extracted
lists.txt		war3map.w3e		war3map.wts
war3map.doo		war3map.w3i		war3mapMap.blp
war3map.j		war3map.w3r		war3mapMisc.txt
war3map.mmp		war3map.wct		war3mapSkin.txt
war3map.shd		war3map.wpm		war3mapUnits.doo
war3map.w3c		war3map.wtg
```




