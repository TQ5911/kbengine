#
# License: BSD
#   https://raw.githubusercontent.com/stonier/py_trees/devel/LICENSE
#

##############################################################################
# Description
##############################################################################

"""
Simple colour definitions and syntax highlighting for the console.

----

**Colour Definitions**

The current list of colour definitions include:

 * ``Regular``: black, red, green, yellow, blue, magenta, cyan, white,
 * ``Bold``: bold, bold_black, bold_red, bold_green, bold_yellow, bold_blue, bold_magenta, bold_cyan, bold_white

These colour definitions can be used in the following way:

.. code-block:: python

   import py_trees.console as console
   print(console.cyan + "    Name" + console.reset + ": " + console.yellow + "Dude" + console.reset)

"""

##############################################################################
# Imports
##############################################################################

import os
import sys
from KBEDebug import *

# python2 is raw-input, python3 is input
try:
    input = raw_input
except NameError:
    pass

##############################################################################
# Keypress
##############################################################################


def read_single_keypress():
    """Waits for a single keypress on stdin.

    This is a silly function to call if you need to do it a lot because it has
    to store stdin's current setup, setup stdin for reading single keystrokes
    then read the single keystroke then revert stdin back after reading the
    keystroke.

    Returns:
        :obj:`int`: the character of the key that was pressed

    Raises:
        KeyboardInterrupt: if CTRL-C was pressed (keycode 0x03)
    """
    return ' '

##############################################################################
# Methods
##############################################################################


def console_has_colours():
    """
    Detects if the console (stdout) has colourising capability.
    """
    if os.environ.get("PY_TREES_DISABLE_COLORS"):
        return False
    # From django.core.management.color.supports_color
    #   https://github.com/django/django/blob/master/django/core/management/color.py
    plat = sys.platform
    supported_platform = plat != 'Pocket PC' and (plat != 'win32' or
                                                  'ANSICON' in os.environ)
    # isatty is not always implemented, #6223.
    is_a_tty = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
    if not supported_platform or not is_a_tty:
        return False
    return True

has_colours = console_has_colours()
""" Whether the loading program has access to colours or not."""

if has_colours:
    # reset = "\x1b[0;0m"
    reset = "\x1b[0m"
    bold = "\x1b[%sm" % '1'
    black, red, green, yellow, blue, magenta, cyan, white = ["\x1b[%sm" % str(i) for i in range(30, 38)]
    bold_black, bold_red, bold_green, bold_yellow, bold_blue, bold_magenta, bold_cyan, bold_white = ["\x1b[%sm" % ('1;' + str(i)) for i in range(30, 38)]
else:
    reset = ""
    bold = ""
    black, red, green, yellow, blue, magenta, cyan, white = ["" for i in range(30, 38)]
    bold_black, bold_red, bold_green, bold_yellow, bold_blue, bold_magenta, bold_cyan, bold_white = ["" for i in range(30, 38)]

colours = [bold,
           black, red, green, yellow, blue, magenta, cyan, white,
           bold_black, bold_red, bold_green, bold_yellow, bold_blue, bold_magenta, bold_cyan, bold_white
           ]
"""List of all available colours."""


def pretty_print(msg, colour=white):
    if has_colours:
        seq = colour + msg + reset
        sys.stdout.write(seq)
    else:
        sys.stdout.write(msg)


def pretty_println(msg, colour=white):
    if has_colours:
        seq = colour + msg + reset
        sys.stdout.write(seq)
        sys.stdout.write("\n")
    else:
        sys.stdout.write(msg)


##############################################################################
# Console
##############################################################################


def debug(msg):
    print(green + msg + reset)


def warning(msg):
    print(yellow + msg + reset)


def info(msg):
    print(msg)


def error(msg):
    print(red + msg + reset)


def logdebug(message):
    '''
    Prefixes ``[DEBUG]`` and colours the message green.

    Args:
        message (:obj:`str`): message to log.
    '''
    INFO_MSG("[DEBUG] " + message)


def loginfo(message):
    '''
    Prefixes ``[ INFO]`` to the message.

    Args:
        message (:obj:`str`): message to log.
    '''
    INFO_MSG("[ INFO] " + message)


def logwarn(message):
    '''
    Prefixes ``[ WARN]`` and colours the message yellow.

    Args:
        message (:obj:`str`): message to log.
    '''
    INFO_MSG( "[ WARN] " + message)


def logerror(message):
    '''
    Prefixes ``[ERROR]`` and colours the message red.

    Args:
        message (:obj:`str`): message to log.
    '''
    INFO_MSG("[ERROR] " + message)


def logfatal(message):
    '''
    Prefixes ``[FATAL]`` and colours the message bold red.

    Args:
        message (:obj:`str`): message to log.
    '''
    INFO_MSG("[FATAL] " + message)


##############################################################################
# Main
##############################################################################

if __name__ == '__main__':
    for colour in colours:
        pretty_print("dude\n", colour)
    logdebug("loginfo message")
    logwarn("logwarn message")
    logerror("logerror message")
    logfatal("logfatal message")
    pretty_print("red\n", red)
    print("some normal text")
    print(cyan + "    Name" + reset + ": " + yellow + "Dude" + reset)
