from json import dump
from adaptivecard._typing import DefaultNone



def try_get_pixel_string(s: int | str, name: str):
    """Attempts to convert `s` by calling get_pixel_string. Raises if it can't"""
    msg = f"'{name}' must be an int or a numeric string ending with 'px', got '{s}' instead"
    try:
        return get_pixel_string(s)
    except (TypeError, ValueError) as e:
        raise e.__class__(msg)


def get_pixel_string(s: int | str):
    """Returns a string-formatted version of s ("{s}px"). Leaves s unchanged if s is DefaultNone."""
    if s is DefaultNone:
        pass
    elif isinstance(s, str):
        if not s.replace('px', '').isdecimal():
            raise ValueError("invalid pixel string")
        s = s.replace('px', '') + 'px'
    elif isinstance(s, int):
        s = str(s) + 'px'
    else:
        raise TypeError("invalid type")
    return s


def camel_to_snake(s: str):
    l = list(s)
    for i, char in enumerate(l):
        if (lower_char := char.lower()) != char:
            l[i] = "_" + lower_char if i > 0 else lower_char
    return "".join(l)


def snake_to_camel(s: str):
    """Returns a snake-cased version of the string."""
    l = s.split("_")
    for i, word in enumerate(l):
        if i > 0:
            l[i] = word.capitalize()
    return "".join(l)


def get_schema_path(definition: dict):
    if "anyOf" in definition:
        for x in definition["anyOf"]:
            p = get_schema_path(x)
            if p is not None:
                return p
    elif "properties" in definition:
        return definition["properties"]


def save_json(path: str, obj: dict, indent: int = 4):
    if not isinstance(indent, int):
        raise TypeError
    with open(path, 'w') as f:
        dump(obj, f, indent=indent)
