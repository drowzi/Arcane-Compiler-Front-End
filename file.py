import os
import subprocess
from constants import *
from arc_error import *
from arc_logger import get_log_handle

filelogger = get_log_handle('file')

class Cache():

    def __init__(self, input):
        self._cache = list(input.read())

    def add(self, byte):
        if len(byte) > 1:
            for c in list(byte):
                self.add(c)
        else:
            self._cache.append(byte)

    def clr(self, s_index=0, e_index=None):
        if e_index is None:
            e_index=self._cache.size()
        del self._cache[s_index:e_index]

    def get(self, s_index, e_index):
        return ''.join(self._cache[s_index:e_index])

    def size(self):
        return len(self._cache)

    def __str__(self):
        return "{0}".format(self.get(0, self.size()))

class InFile():

    _currentc = 0
    _currentl = 0
    _eof = 0

    def __init__(self, path, name):
        self._filepath = os.path.join(path, name)
        self._filein = open(self._filepath, 'r')
        self._cache = Cache(self._filein)
        #self._logref = logging
        self._f_reset_pos()
        if(self._file_is_empty()):
            raise ARCFileEmpty("file is empty.")
        filelogger.debug("Successfully opened read stream for file - {}".format(self._filepath))

    def readc(self):
        self.inc_c()
        current = self._filein.read(1)
        if(current is NL):
            self.inc_l()
        if(current is ''):
            self._eof = 1
        return current

    def readln(self):
        current = out = ""
        while(current is not NL ):
            current = self.readc()
            out += current
        return out

    def lookahead(self, amt=1):
        peek = self._currentc + amt
        if peek > self._cache.size():
            filelogger.warning("Lookahead requested a max index({0}) out of range of cache.size({1}), returned cache.size.".format(peek, self._cache.size()))
            peek = self._cache.size()
        return self._cache.get(self._currentc, peek)

    def lookbehind(self, amt=1):
        peek = self._currentc - amt
        if peek < 0:
            filelogger.warning("Lookbehind requested an index({0}) less than 0, returned 0.".format(peek))
            peek = 0
        return self._cache.get(peek, self._currentc)

    def next(self):
        return self._cache.get(self._currentc, self._currentc+1)

    def eof(self):
        return self._eof

    def inc_c(self, amt=1):
        self._currentc = self._currentc + amt

    def inc_l(self, amt=1):
        self._currentl = self._currentl + amt

    def _file_is_empty(self):
        return os.stat(self._filepath).st_size == 0

    def getfilepath(self):
        return self._filepath

    def getcache(self):
        return self._cache

    def _f_reset_pos(self):
        self._filein.seek(0, 0)

    def close(self):
        self._filein.close()

    def closed(self):
        return self._filein.closed

    def __str__(self):
        return "path={0}\ncurrent_char={1}\ncurrent_line={2}".format(self._filepath, self._currentc, self._currentl)

class OutFile():

    def __init__(self, path, name):
        self._filename = name
        self._filepath = os.path.join(path, name)
        self._fileout = open(self._filepath, 'w')
        filelogger.debug("Successfully opened write stream for c output.")

    def emit(self, bytes):
        self._fileout.write(bytes)

    def emitln(self):
        self.emit(NL)

    def exec(self):
        try:
            subprocess.call(['gcc', self._filename])
        except:
            raise ARCFailedToExecute("file {} failed to execute.".format(self._filename))

    def close(self):
        self._fileout.close()

    def closed(self):
        return self._fileout.closed

    def __str__(self):
        return "path={0}".format(self._filepath)