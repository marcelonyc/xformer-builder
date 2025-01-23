from RestrictedPython import compile_restricted
from RestrictedPython.Guards import (
    safe_builtins,
    guarded_iter_unpack_sequence,
    guarded_unpack_sequence,
)
import ast
from typing import Dict
from RestrictedPython.Eval import default_guarded_getitem


def parse_xformer_code(code) -> ast.unparse:
    """
    Parses the given Xformer code and transforms it into a valid Python function.

    Args:
        code (str): The Xformer code to parse.

    Returns:
        str: The transformed Python code.

    Raises:
        TypeError: If the last line in the Xformer code is not an expression.
    """
    xformer = ast.parse(code)
    if len(xformer.body) == 0:
        return None

    last_code_line = xformer.body[-1]
    if isinstance(last_code_line, ast.Expr):
        xformer.body = [
            ast.FunctionDef(
                name="xformer_code",
                lineno=0,
                type_ignores=[],
                body=[
                    *xformer.body[:-1],
                    ast.Return(
                        value=last_code_line.value,
                        lineno=last_code_line.lineno,
                    ),
                ],
                decorator_list=[],
                args=ast.arguments(
                    posonlyargs=[],
                    args=[],
                    kwonlyargs=[],
                    kw_defaults=[],
                    defaults=[],
                ),
            )
        ]
    else:
        raise TypeError("Last line in the Xformer code must be an expression.")

    return ast.unparse(xformer)


# Custom attribute guards
def guarded_getattr(obj, name):
    """
    Safely retrieves an attribute from an object, while guarding against certain restricted attribute names.

    Args:
        obj: The object from which to retrieve the attribute.
        name: The name of the attribute to retrieve.

    Returns:
        The value of the attribute.

    Raises:
        NotImplementedError: If the attribute name is restricted and not allowed.
    """
    if name in ["zfill"]:
        raise NotImplementedError(f"{name} is not allowed")
    return getattr(obj, name)


def guarded_setattr(obj, name, value):
    raise NotImplementedError("Setting attributes is not allowed")


def guarded_import(name: str, *args, **kwargs):
    """
    Safely imports a module by name.

    Args:
        name (str): The name of the module to import.
        *args: Additional positional arguments to pass to the `__import__` function.
        **kwargs: Additional keyword arguments to pass to the `__import__` function.

    Returns:
        module: The imported module.

    Raises:
        ImportError: If the specified module is not allowed to be imported.
    """
    if name not in ["datetime"]:
        raise ImportError(f"Cannot import {name}.")

    return __import__(name, *args, **kwargs)


def safe_execute(code, data, other_columns) -> Dict:
    """
    Executes the given code in a restricted environment and returns the result.

    Args:
        code (str): The code to be executed.
        data (object): The data object to be used in the code execution.
        other_columns (list): The list of other columns to be used in the code execution.

    Returns:
        dict: A dictionary containing the execution status and result. The dictionary has the following keys:
            - "status" (str): The execution status, which can be "success" or "failed".
            - "result" (object): The result of the code execution. If the execution status is "success", this will be the
              result of calling the "xformer_code" function defined in the code. If the execution status is "failed",
              this will be an error message indicating the reason for the failure.
    """
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
