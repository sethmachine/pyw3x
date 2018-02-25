"""

"""

import wc3_runner
import psutil

def kill(proc_pid):
    process = psutil.Process(proc_pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()

if __name__ == '__main__':
    i = 'data/test/GlacialCopy4.w3x'
    outdir = 'foobar'
    w = wc3_runner.Wc3_Runner()
    p = w.run_map(i, outdir)
