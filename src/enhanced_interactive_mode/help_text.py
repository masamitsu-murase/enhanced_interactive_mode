import inspect
import pydoc
import re
import textwrap
from .docstring import (
    find_docstring_for_class_attr,
    find_docstring_for_module_variable,
)


TITLE = "Help for %s"
SEPARATOR = "-" * 32


def find_token_name(line, cursor_point):
    token_name_suffix_substr = line[cursor_point:]
    pattern = r"^([_0-9a-zA-Z]*)"
    token_name_suffix_match = re.search(pattern, token_name_suffix_substr)
    token_name_suffix = token_name_suffix_match.group(0)

    token_name_prefix = line[:cursor_point] + token_name_suffix
    pattern = r"([_a-zA-Z][_0-9a-zA-Z]*(\.[_a-zA-Z][_0-9a-zA-Z]*)*)\(?$"
    token_name_match = re.search(pattern, token_name_prefix)
    if token_name_match is None:
        return None

    token_name = token_name_match.group(1)
    if "." in token_name:
        return token_name.rsplit(".", 1)
    else:
        return [None, token_name]


def pydoc_render_doc(value):
    return pydoc.render_doc(value, title=TITLE, renderer=pydoc.plaintext)


def find_help_text_for_class(cls):
    t = pydoc_render_doc(cls)
    class_title = t[: t.index("\n")]

    t = ", ".join(f"{b.__module__}.{b.__name__}" for b in cls.__bases__)
    class_doc = f"class {cls.__module__}.{cls.__name__}({t}):"

    t = inspect.getdoc(cls) or "(No document)"
    class_doc += "\n" + textwrap.indent(t, " " * 4)

    init_doc = pydoc_render_doc(cls.__init__)

    doc = f"{class_title}\n\n{class_doc}\n\n{SEPARATOR}\n{init_doc}"
    return doc


def find_help_text(value, parent, attr_str):
    if inspect.isclass(value):
        return find_help_text_for_class(value)

    if inspect.isclass(parent):
        desc = f"attribute {attr_str} of {parent.__module__}.{parent.__name__}"
        doc = find_docstring_for_class_attr(parent, attr_str)
    elif inspect.ismodule(parent):
        desc = f"variable {attr_str} of {parent.__name__}"
        doc = find_docstring_for_module_variable(parent, attr_str)
    else:
        desc = doc = None

    if doc:
        return TITLE % desc + "\n\n" + textwrap.indent(doc, " " * 4)

    return pydoc_render_doc(value)
