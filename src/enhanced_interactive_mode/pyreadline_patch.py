import __main__
import math
import pydoc
import readline
import reprlib

from pyreadline.console.ansi import AnsiState
from pyreadline.modes.basemode import BaseMode, commonprefix

from .help_text import find_help_text, find_token_name

SEPARATOR = "=" * 32
console_completion_highlight_color = "white"


def show_help(self: BaseMode, e):
    token_name = find_token_name(
        self.l_buffer.get_line_text(), self.l_buffer.point
    )
    if token_name is None:
        return

    obj_str, attr_str = token_name
    if obj_str is None:
        token_str = attr_str
    else:
        token_str = f"{obj_str}.{attr_str}"

    try:
        value = eval(token_str, __main__.__dict__)
        if obj_str is not None:
            parent = eval(obj_str, __main__.__dict__)
        else:
            parent = None
    except Exception:
        return

    help_text = find_help_text(value, parent, attr_str)
    if not help_text:
        return

    help_text = (
        f"\n{token_str}: {reprlib.repr(value)}\n"
        + f"{SEPARATOR}\n{help_text}\n{SEPARATOR}\n"
    )

    _, height = self.console.size()
    if help_text.count("\n") > height + 5:
        pydoc.pager(help_text)
    else:
        self.console.write(help_text)
    self._print_prompt()
    self.finalize()


def _display_completions(self, completions):
    if not completions:
        return
    self.console.write("\n")

    prefix = commonprefix(completions)
    wmax = max(map(len, completions))
    w, h = self.console.size()
    cols = max(1, int((w - 1) / (wmax + 1)))
    rows = int(math.ceil(float(len(completions)) / cols))
    for row in range(rows):
        s = ""
        for col in range(cols):
            i = col * rows + row
            if i < len(completions):
                cmd = completions[i]
                self.console.write(cmd[: len(prefix)])
                highlighted = cmd[len(prefix) : len(prefix) + 1]
                if highlighted:
                    self.console.write_color(
                        highlighted,
                        attr=AnsiState(
                            color=console_completion_highlight_color
                        ),
                    )
                rest = cmd.ljust(wmax + 1)[len(prefix) + len(highlighted) :]
                self.console.write(rest)
        self.console.write("\n")
    self._print_prompt()


def apply_patch(*, completion_highlight_color=None):
    BaseMode.show_help = show_help
    BaseMode._display_completions = _display_completions
    readline.parse_and_bind("F12: show-help")
    if completion_highlight_color:
        global console_completion_highlight_color
        console_completion_highlight_color = completion_highlight_color
