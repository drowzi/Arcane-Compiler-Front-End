import logging
# (note): the purpose of wrapping the logging library in my own function is to be able to disable it when its not needed.
# (another note): you might be able to do this with logging.setLevel
def log(callback):
    """Logs data if DEBUG_MODE is enabled"""
    if (dir().__contains__('logging')):
        def f_wrapper(msg):
            callback(msg)

        return f_wrapper


@log
def logdebug(msg):
    """Debug decorator"""
    return logging.debug


@log
def loginfo(msg):
    """Info decorator"""
    return logging.info


@log
def logwarning(msg):
    """Warning decorator"""
    return logging.warning


@log
def logerror(msg):
    """Error decorator"""
    return logging.error


@log
def logcritical(msg):
    """Critical decorator"""
    return logging.critical