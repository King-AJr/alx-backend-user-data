#!/usr/bin/env python3
"""
Main file
"""
import inspect
from auth import _hash_password

print(_hash_password("Hello Holberton"))



def check_annotations(target_function):
    signature = inspect.signature(target_function)
    params = signature.parameters
    annotated_params = []
    return_annotation = None

    for param_name, param in params.items():
        if param.annotation != param.empty:
            annotated_params.append(param_name)

    if target_function.__annotations__:
        return_annotation = target_function.__annotations__.get('return', None)

    message = f"{len(annotated_params)} {'thing' if len(annotated_params) == 1 else 'things'} have been annotated\n"

    for param_name in annotated_params:
        param_annotation = target_function.__annotations__.get(param_name, None)
        message += f"parameter {param_name} is annotated as a '{param_annotation.__name__}'\n"

    if return_annotation is not None:
        message += f"function returns a '{return_annotation.__name__}'"

    return message

    return a + len(b)

result = check_annotations(_hash_password)
print(result)

