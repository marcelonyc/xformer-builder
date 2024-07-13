from RestrictedPython import compile_restricted
from RestrictedPython.Guards import (
    safe_builtins,
    guarded_iter_unpack_sequence,
    guarded_unpack_sequence,
)
import ast
from typing import Dict
from RestrictedPython.Eval import default_guarded_getitem


def parse_xformer_code(code):
    xformer = ast.parse(code)
    if len(xformer.body) == 0:
        return None

    last_statement = xformer.body[-1]
    if isinstance(last_statement, ast.Expr):
        xformer.body = [
            ast.FunctionDef(
                name="xformer_code",
                args=ast.arguments(
                    posonlyargs=[],
                    args=[],
                    kwonlyargs=[],
                    kw_defaults=[],
                    defaults=[],
                ),
                decorator_list=[],
                type_ignores=[],
                body=[
                    *xformer.body[:-1],
                    ast.Return(
                        value=last_statement.value,
                        lineno=last_statement.lineno,
                    ),
                ],
                lineno=0,
            )
        ]
    else:
        raise TypeError("Last line in the Xformer code must be an expression.")

    return ast.unparse(xformer)


# Custom attribute guards
def guarded_getattr(obj, name):
    if name in ["zfill"]:
        raise NotImplementedError(f"{name} is not allowed")
    return getattr(obj, name)


def guarded_setattr(obj, name, value):
    raise NotImplementedError("Setting attributes is not allowed")


def guarded_import(name: str, *args, **kwargs):
    if name not in ["datetime"]:
        raise ImportError(f"Cannot import {name}.")

    return __import__(name, *args, **kwargs)


def safe_execute(code, data, other_columns) -> Dict:
    # Compile the code in restricted mode
    try:
        parsed_code = parse_xformer_code(code)
    except Exception as e:
        return {"status": "failed", "result": f"Code parse failed: {e}"}

    try:
        byte_code = compile_restricted(
            parsed_code,
            filename="<inline code>",
            mode="exec",
        )
    except Exception as e:
        return {"status": "failed", "result": f"Code compilation failed: {e}"}

    # Define restricted built-ins and globals
    safe_builtins["__import__"] = guarded_import

    safe_globals = {
        "__builtins__": safe_builtins,
        "_getiter_": iter,
        "_getitem_": default_guarded_getitem,
        "_getattr_": guarded_getattr,
        "_setattr_": guarded_setattr,
        "_iter_unpack_sequence_": guarded_iter_unpack_sequence,
        "_unpack_sequence_": guarded_unpack_sequence,
        "data": data,
        "columns": other_columns,
    }

    # Safe locals dictionary
    safe_locals = {}

    # Execute the compiled byte code in a restricted environment
    exec_out = exec(byte_code, safe_globals, safe_locals)
    try:
        exec_result = {
            "status": "success",
            "result": safe_locals["xformer_code"](),
        }
    except Exception as e:
        exec_result = {
            "status": "failed",
            "result": f"Syntax isn't excepted {e}",
        }
    return exec_result
