import __main__
from _pyrepl import commands, reader
import reprlib

from .help_text import find_help_text, find_token_name


class show_help(commands.Command):
    def do(self):
        r = self.reader

        token_name = find_token_name("".join(r.buffer), r.pos)
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

        help_text = f"{token_str}: {reprlib.repr(value)}\n{help_text}"

        r.msg = help_text
        r.dirty = True


def apply_patch(*, completion_highlight_color=None):
    commands.show_help = show_help
    reader.default_keymap += (
        (r"\<f12>", "show-help"),
    )

    if completion_highlight_color:
        raise ValueError("colorized completion is not supported.")
