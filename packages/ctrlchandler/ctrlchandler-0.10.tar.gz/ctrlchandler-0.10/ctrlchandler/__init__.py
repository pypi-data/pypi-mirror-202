import ctypes
import os
import sys
from ctypes import wintypes
from functools import wraps, partial
import inspect
from copy import deepcopy

_kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)


def copy_func(f):
    if callable(f):
        if inspect.ismethod(f) or inspect.isfunction(f):
            g = lambda *args, **kwargs: f(*args, **kwargs)
            t = list(filter(lambda prop: not ("__" in prop), dir(f)))
            i = 0
            while i < len(t):
                setattr(g, t[i], getattr(f, t[i]))
                i += 1
            return g
    dcoi = deepcopy([f])
    return dcoi[0]


class FlexiblePartialOwnName:
    def __init__(
        self, func, funcname: str, this_args_first: bool = True, *args, **kwargs
    ):
        self.this_args_first = this_args_first
        self.funcname = funcname
        try:
            self.f = copy_func(func)
        except Exception:
            self.f = func
        try:
            self.args = copy_func(list(args))
        except Exception:
            self.args = args

        try:
            self.kwargs = copy_func(kwargs)
        except Exception:
            try:
                self.kwargs = kwargs.copy()
            except Exception:
                self.kwargs = kwargs

    def __call__(self, *args, **kwargs):
        newdic = {}
        newdic.update(self.kwargs)
        newdic.update(kwargs)
        if self.this_args_first:
            return self.f(*self.args, *args, **newdic)

        else:
            return self.f(*args, *self.args, **newdic)

    def __str__(self):
        return self.funcname

    def __repr__(self):
        return self.funcname


def ctrlcdecorator(f_py=None, returncode=0):
    assert callable(f_py) or f_py is None

    def _decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if "returncode" in kwargs:
                del kwargs["returncode"]
            _ = func(*args[1:], **kwargs)
            try:
                sys.exit(returncode)
            finally:
                os._exit(returncode)

        return wrapper

    return _decorator(f_py) if callable(f_py) else _decorator


def _check_bool(result, func, args):
    if not result:
        raise ctypes.WinError(ctypes.get_last_error())
    return args


def set_console_ctrl_handler(returncode, func, *args, **kwargs):
    # based on https://stackoverflow.com/a/19907688/15096247
    handler = FlexiblePartialOwnName(func, "", True, *args, **kwargs)
    handler = partial(ctrlcdecorator(handler, returncode))
    if handler not in _console_ctrl_handlers:
        h = _HandlerRoutine(handler)
        _kernel32.SetConsoleCtrlHandler(h, True)
        _console_ctrl_handlers[handler] = h


_HandlerRoutine = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.DWORD)

_kernel32.SetConsoleCtrlHandler.errcheck = _check_bool
_kernel32.SetConsoleCtrlHandler.argtypes = (_HandlerRoutine, wintypes.BOOL)

_console_ctrl_handlers = {}

