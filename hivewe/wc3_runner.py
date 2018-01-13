"""

"""

import multiprocessing
import os
import shutil
import subprocess
import uuid

import psutil

WC3_X86_EXE_WIN_10 = "C:\\Program Files (x86)\\Warcraft III\\Warcraft III.exe"
WC3_MAP_DIR_WIN_10 = "C:\\Users\\sdwor\\OneDrive\\Documents\\Warcraft III\\Maps"
OUTDIR = os.path.join(WC3_MAP_DIR_WIN_10, 'wc3-runner')

def _run(args):
    p = subprocess.Popen(args, stdout=subprocess.PIPE, shell=False)
    out, err = p.communicate()
    return out, err

def kill(proc_pid):
    """Taken from SO: https://stackoverflow.com/questions/4789837/how-to-terminate-a-python-subprocess-launched-with-shell-true

    :param proc_pid:
    :return:
    """
    process = psutil.Process(proc_pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()

class Wc3_Runner():
    def __init__(self, wc3_exe=WC3_X86_EXE_WIN_10, wc3_mapdir=WC3_MAP_DIR_WIN_10):
        assert os.path.exists(wc3_exe)
        assert os.path.exists(wc3_mapdir)
        self.exe = wc3_exe
        self.mapdir = wc3_mapdir
        self.wc3_process = None

    def run(self, window=True):
        """Launches Warcraft III Frozen Throne in windowed mode (default).

        WC3 is launched in background process.  Use `self.close()` to terminate.

        :param window:
        :return:
        """
        if self.wc3_process:
            raise ValueError('WC3 Process is already running.')
        args = [self.exe, '-window']
        if not window:
            args.remove('-window')
        proc = multiprocessing.Process(target=_run, args=(args,))
        proc.daemon = True
        proc.start()
        self.wc3_process = proc
        return self.wc3_process

    def run_map(self, infile, outdir, window=True, replace_existing=True):
        """Map file must be located in WC3 User maps directory.  If not it will be copied over in a temp directory.

        WC3 is launched in background process.  Use `self.close()` to terminate.

        :param infile:
        :param window:
        :param outdir: output directory to create if the map file is not in the map directory
        :return:
        """
        if self.wc3_process:
            raise ValueError('WC3 Process is already running.')
        mapfile = infile
        if self.mapdir not in infile:
            outdir = os.path.join(self.mapdir, outdir)
            if not os.path.exists(outdir):
                os.mkdir(outdir)
            bn = os.path.basename(infile)
            outfile = os.path.join(outdir, bn)
            if os.path.exists(outfile) and not replace_existing:
                raise FileExistsError('Map file exists in output directory.  Choose a different output directory.')
            shutil.copyfile(infile, outfile)
            mapfile = outfile
        args = [self.exe, '-window', '-loadfile', mapfile]
        print(' ' .join(args))
        if not window:
            args.remove('-window')
        proc = multiprocessing.Process(target=_run, args=(args,))
        # proc.daemon = True
        proc.start()
        self.wc3_process = proc
        return self.wc3_process

    def close(self):
        """Terminates the process running Warcraft III.

        :return:
        """
        if not self.wc3_process:
            raise ValueError('Warcraft III process not started.')
        kill(self.wc3_process.pid)
        self.wc3_process = None

    def quit(self):
        self.close()

    def exit(self):
        self.close()

    def kill(self):
        self.close()

    def __repr__(self):
        return 'Warcraft III executable: {}\nWarcraft III user map directory: {}'.format(self.exe, self.mapdir)


if __name__ == '__main__':
    w = Wc3_Runner()
    p = w.run_map('data/test/GlacialCopy4.w3x', 'foobar', replace_existing=True)