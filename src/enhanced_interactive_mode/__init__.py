import inspect
from rlcompleter import Completer

from .pyreadline_patch import apply_patch


def _callable_postfix(self, val, word):
    if callable(val) and not inspect.isclass(val):
        word = word + "("
    return word


def init(*, completion_highlight_color=None):
    Completer._callable_postfix = _callable_postfix
    apply_patch(completion_highlight_color=completion_highlight_color)
