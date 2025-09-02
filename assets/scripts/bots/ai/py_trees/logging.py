#!/usr/bin/env python
#
# License: BSD
#   https://raw.githubusercontent.com/stonier/py_trees/devel/LICENSE
#
##############################################################################
# Documentation
##############################################################################

"""
.. module:: loggers
   :synopsis: Logging facilities in py_trees.

Oh my spaghettified magnificence,
Bless my noggin with a tickle from your noodly appendages!
"""

##############################################################################
# Imports
##############################################################################

from enum import IntEnum

from . import console

##############################################################################
# Logging
##############################################################################

# I'd really prefer to use python logging facilities, but rospy logging
# on top of python logging kills it.
#
# Could still use it here, and would actually be useful if I could
# integrate it with nosetests, but for now, this will do.
# Note, you can get colour with python logging, but its tricky;
#
#   http://stackoverflow.com/questions/384076/how-can-i-color-python-logging-output
#
# python way:
#
#     import logging
#         logging.getLogger("py_trees.Behaviour")
#         logging.basicConfig(level=logging.DEBUG)
#
##############################################################################
# Level
##############################################################################


# levels
class Level(IntEnum):
    """
    An enumerator representing the logging level.
    Not valid if you override with your own loggers.
    """

    _ERROR = 0b00000001
    ERROR  = _ERROR

    _WARN  = 0b00000010
    WARN   = _ERROR + _WARN

    _INFO  = 0b00000100
    INFO   = _ERROR + _WARN + _INFO

    _DEBUG = 0b00001000
    DEBUG  = _ERROR + _WARN + _INFO + _DEBUG

    _TRACE = 0b00010000
    TRACE  = _TRACE

    @classmethod
    def getRealLevel(cls, orgLvlNum):
        """ 0: debug, 1: info, 2: warning, 3: error, 4: trace(only) """
        if orgLvlNum == 0:
            return cls.DEBUG
        elif orgLvlNum == 1:
            return cls.INFO
        elif orgLvlNum == 2:
            return cls.WARN
        elif orgLvlNum == 3:
            return cls.ERROR
        elif orgLvlNum == 4:
            return cls.TRACE
        else:
            # DEFAULT VALUE
            return cls.INFO

# module variable

##############################################################################
# Logger Class
##############################################################################


class Logger(object):
    """
    :cvar override: whether or not the default python logger has been overridden.
    :vartype override: bool
    """

    def __init__(self, name=None, owner=None):
        self.prefix = ''
        self.owner = owner

    @property
    def level(self):
        return self.owner.logLevel

    def debug(self, msg):
        if self.level & Level._DEBUG:
            console.logdebug(self.prefix + msg)

    def info(self, msg):
        if self.level & Level._INFO:
            console.loginfo(self.prefix + msg)

    def warning(self, msg):
        if self.level & Level._WARN:
            console.logwarn(self.prefix + msg)

    def error(self, msg):
        if self.level & Level._ERROR:
            console.logerror(self.prefix + msg)
