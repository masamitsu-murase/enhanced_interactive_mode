import ast
import inspect
import textwrap


def find_docstring_for_toplevel_assign_expr_pair(statements, attr_str):
    for assign, expr in zip(statements, statements[1:]):
        if not isinstance(expr, ast.Expr):
            continue

        if isinstance(assign, ast.Assign):
            targets = assign.targets
        elif isinstance(assign, ast.AnnAssign):
            targets = [assign.target]
        else:
            continue

        if not any(
            (
                isinstance(x, ast.Name)
                and x.id == attr_str
                and isinstance(x.ctx, ast.Store)
            )
            for x in targets
        ):
            continue

        if not (
            isinstance(expr.value, ast.Constant)
            and isinstance(expr.value.value, str)
        ):
            continue

        return inspect.cleandoc(expr.value.value)

    for st in statements:
        if isinstance(st, ast.If):
            bodies = st.body + st.orelse
        elif isinstance(st, ast.Try):
            bodies = (
                st.body
                + sum(s.body for s in st.handlers)
                + st.orelse
                + st.finalbody
            )
        else:
            continue

        doc = find_docstring_for_toplevel_assign_expr_pair(bodies, attr_str)
        if doc is not None:
            return doc

    return None


def find_docstring_for_class_attr(class_value, attr_str):
    for cls in inspect.getmro(class_value):
        try:
            source = inspect.getsource(cls)
        except TypeError:
            continue

        source = textwrap.dedent(source)
        cls_ast = ast.parse(source)

        class_def = cls_ast.body[0]
        if not isinstance(class_def, ast.ClassDef):
            continue

        doc = find_docstring_for_toplevel_assign_expr_pair(
            class_def.body, attr_str
        )
        if not doc:
            continue
        return doc

    return None


def find_docstring_for_module_variable(mod, var_str):
    try:
        source = inspect.getsource(mod)
    except TypeError:
        return None

    mod_ast = ast.parse(source)
    if not isinstance(mod_ast, ast.Module):
        return None

    return find_docstring_for_toplevel_assign_expr_pair(mod_ast.body, var_str)
