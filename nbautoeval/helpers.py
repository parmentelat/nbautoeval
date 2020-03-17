
from types import FunctionType, BuiltinFunctionType, BuiltinMethodType

default_font_size='small'
default_header_font_size='medium'


# helpers 
def commas(iterable):
    if isinstance(iterable, dict):
        return ", ".join(f"{k}={custom_repr(v)}" for k, v in iterable.items())
    elif isinstance(iterable, str):
        return str
    else:
        return ", ".join([custom_repr(x) for x in iterable])


def custom_repr(x):
    if isinstance(x, (type, FunctionType, BuiltinFunctionType, BuiltinMethodType)):
        return x.__name__
    elif isinstance(x, set):
        return "{" + commas(x) + "}"
    else:
        return repr(x)


def truncate(message: str, width):
    # width <= 0 means do not truncate
    if width <= 0:
        return message
    truncated = message if len(message) <= width \
        else message[:width-3]+'...'
    return truncated
