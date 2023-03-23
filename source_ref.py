class SourceRef():
    """ Reference """

    _source = list()

    def __init__(self):
        pass

    def add_line(self, codeline):
        self._source.append(codeline)

    def get_line(self, lineno):
        return self._source[lineno]

    def __str__(self):
        return self._source

