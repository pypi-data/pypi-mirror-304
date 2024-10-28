import colorama
from colorama import Fore
from types import FrameType


def addaudithook(*args, **kwargs):  # real signature unknown
    """ Adds a new audit hook callback. """
    pass


def audit(event, *args):  # real signature unknown; restored from __doc__
    """
    audit(event, *args)

    Passes the event to any audit hooks that are attached.
    """
    pass


def breakpointhook(*args, **kws):  # real signature unknown; restored from __doc__
    """
    breakpointhook(*args, **kws)

    This hook function is called by built-in breakpoint().
    """
    pass


def call_tracing(*args, **kwargs):  # real signature unknown
    """
    Call func(*args), while tracing is enabled.

    The tracing state is saved, and restored afterwards.  This is intended
    to be called from a debugger from a checkpoint, to recursively debug
    some other code.
    """
    pass


def displayhook(*args, **kwargs):  # real signature unknown
    """ Print an object to sys.stdout and also save it in builtins._ """
    pass


def excepthook(*args, **kwargs):  # real signature unknown
    """ Handle an exception by displaying it with a traceback on sys.stderr. """
    pass


def exc_info(*args, **kwargs):  # real signature unknown
    """
    Return current exception information: (type, value, traceback).

    Return information about the most recent exception caught by an except
    clause in the current stack frame or in an older stack frame.
    """
    pass


def exit(*args, **kwargs):  # real signature unknown
    """
    Exit the interpreter by raising SystemExit(status).

    If the status is omitted or None, it defaults to zero (i.e., success).
    If the status is an integer, it will be used as the system exit status.
    If it is another kind of object, it will be printed and the system
    exit status will be one (i.e., failure).
    """
    pass


def getallocatedblocks(*args, **kwargs):  # real signature unknown
    """ Return the number of memory blocks currently allocated. """
    pass


def getdefaultencoding(*args, **kwargs):  # real signature unknown
    """ Return the current default encoding used by the Unicode implementation. """
    pass


def getfilesystemencodeerrors(*args, **kwargs):  # real signature unknown
    """ Return the error mode used Unicode to OS filename conversion. """
    pass


def getfilesystemencoding(*args, **kwargs):  # real signature unknown
    """ Return the encoding used to convert Unicode filenames to OS filenames. """
    pass


def getprofile(*args, **kwargs):  # real signature unknown
    """
    Return the profiling function set with sys.setprofile.

    See the profiler chapter in the library manual.
    """
    pass


def getrecursionlimit(*args, **kwargs):  # real signature unknown
    """
    Return the current value of the recursion limit.

    The recursion limit is the maximum depth of the Python interpreter
    stack.  This limit prevents infinite recursion from causing an overflow
    of the C stack and crashing Python.
    """
    pass


def getrefcount():  # real signature unknown; restored from __doc__
    """
    Return the reference count of object.

    The count returned is generally one higher than you might expect,
    because it includes the (temporary) reference as an argument to
    getrefcount().
    """
    pass


def getsizeof(p_object, default=None):  # real signature unknown; restored from __doc__
    """
    getsizeof(object [, default]) -> int

    Return the size of object in bytes.
    """
    return 0


def getswitchinterval(*args, **kwargs):  # real signature unknown
    """ Return the current thread switch interval; see sys.setswitchinterval(). """
    pass


def gettrace(*args, **kwargs):  # real signature unknown
    """
    Return the global debug tracing function set with sys.settrace.

    See the debugger chapter in the library manual.
    """
    pass
