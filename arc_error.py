class ARCUnexpected(Exception):
    pass

class ARCUnfinished(Exception):
    pass

class ARCFileNotFound(Exception):
    pass

class ARCFailedToExecute(Exception):
    pass

class ARCFileEmpty(Exception):
    pass

class ARCLexSecondInstance(Exception):
    pass

class ARCLexInputNotSet(Exception):
    pass

class ARCLexLastTokenOutOfRange(Exception):
    pass

class ARCUtilError(Exception):
    pass

class ARCSyntaxError(Exception):
    pass