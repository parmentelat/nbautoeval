# -*- coding: utf-8 -*-

# pylint: disable=c0111, r1705


import copy
import pprint
import itertools
from collections.abc import Iterable, Iterator

from nbautoeval.rendering import commas, truncate_str

####################
# From June 2016, this class should not need to be used directly
# as Args would allow to build it with a nicer interface
class ArgsTupleDict:
    """
    The most general form of a function argument list is made
    of a tuple and a dictionary

    Example:
    my_input = ArgsTupleDict( (1,2), {'a': []})
    my_input.call (foo)
    would then return the result of
    foo (1, 2, a=[])
    """
    def __init__(self, _args=None, _keywords=None):
        # expecting a tuple or a list
        self.args = _args if _args is not None else tuple()
        # expecting a dictionary
        self.keywords = _keywords if _keywords is not None else {}
        # can be overridden later on using 'render_function_name'
        self.function_name = None
        # can be overridden later on using 'render_prefix'
        self.prefix = ""
        self.postfix = ""
        # default - no way to set this on the constructor
        # because layout=x is already captured in _keywords
        self.layout = None

    def __repr__(self):
        result = f"<Args {self.prefix}{self.function_name}{self.args}{self.postfix} "
        if self.keywords:
            result += ("Keywords:" + 
                       ",".join(f"{k}={v}" for (k, v) in self.keywords.items()))
        result += ">"
        return result

    def set_layout(self, layout):
        # used when rendering - in example or correction
        # in general this is defined in the Exercise instance
        # but can also be overridden here
        self.layout = layout

    def call(self, function, debug=False):
        if debug:
            print(f"calling {function.__name__} *{self.args} **{self.keywords}")
        return function(*self.args, **self.keywords)

    def init_obj(self, klass, debug=False):
        if debug:
            print(f"creating object in class {klass.__name__}, *{self.args} **{self.keywords}")
        return klass(*self.args, **self.keywords)

    def call_obj(self, obj, methodname, debug=False):
        if debug:
            print(f"calling method {methodname} on object {obj} *{self.args} **{self.keywords}")
        method = getattr(obj, methodname)
        return method(*self.args, **self.keywords)

    def clone(self, copy_mode):
        "clone this input for safety"
        if copy_mode == 'shallow':
            return copy.copy(self)
        elif copy_mode == 'deep':
            return copy.deepcopy(self)
        else:
            return self

    def render_function_name(self, function_name):
        """
        if called, arguments will be rendered like this
        function_name (arg1, ... argn)
        instead of just
        arg1, .. argn
        """
        self.function_name = function_name

    def render_prefix(self, prefix):
        """
        if called, arguments will be rendered with this prefix prepended
        """
        self.prefix = prefix

    def render_postfix(self, postfix):
        """
        if called, arguments will be rendered with this postfix appended
        """
        self.postfix = postfix

    def layout_void(self, width):                # pylint: disable=r0201, w0613
        return ""

    def layout_truncate(self, width):
        """
        render a list of arguments on a single line, truncated
        remember that width <= 0 means no truncation
        """
        text = commas(self.args)
        if self.keywords:
            text += ", " + commas(self.keywords)
        if self.function_name:
            text = f"{self.function_name}({text})"
        text = self.prefix + text + self.postfix
        return truncate_str(text, width)

    def layout_pprint(self, width):
        """
        render a list of arguments in pprint mode
        """
        # try to render with no width limit, if it fits it's OK
        simple_case = self.layout_truncate(width=0)
        if len(simple_case) <= width:
            return simple_case
        else:
            pass
        # else
        indent = 2
        sep = indent*' '
        html = "<pre>"
        html += self.prefix
        if self.function_name:
            html += self.function_name + "(\n"
        def indent_pformat(pformat_result):
            return sep + pformat_result.replace("\n", "\n"+sep)
        args_tokens = [
            pprint.pformat(arg, width=width-indent, indent=indent)
            for arg in self.args]
        keyword_tokens = [
            f"{k}={pprint.pformat(v, width=width-indent, indent=indent)}"
            for (k, v) in self.keywords.items()]
        tokens = [indent_pformat(x) for x in args_tokens + keyword_tokens]
        html += (",\n").join(tokens)
        if self.function_name:
            html += ")\n"
        html += self.postfix
        html += "</pre>"
        return html

# simplified for when no keywords are required
class Args(ArgsTupleDict):
    """
    In most cases though, we do not use keywords so it is more convenient to
    just pass a list of arguments

    Example:
    my_input = Args (1, 2, 3)
    my_input.call(foo)
    would then return the result of
    foo(1, 2, 3)

    Like for ArgKeywords it is preferable to set the layout
    using the separate set_leyout method
    """
    def __init__(self, *args, **kwds):
        # it is NOT *args here, this is intentional
        ArgsTupleDict.__init__(self, args, kwds)


class GeneratorArgs(Args):
    """
    GenArgs is like Args but designed for use 
    with an ExerciseGenerator
    
    See exercises/squares.py for an example of how to use it
    """
    def __init__(self, *args, islice=None, **kwds):
        super().__init__(*args, **kwds)
        self.islice = islice


    def call(self, function, debug=False):
        # call() already has it's contents converted
        # to a list because comparison of results alreqdy has taken place
        iterable = super().call(function)
        if not isinstance(iterable, Iterable):
            raise TypeError(f"not an iterable! received a {type(iterable).__name__} instance: {iterable}")
        if not self.islice:
            return iterable
        return list(itertools.islice(iterable, *self.islice))


    # hacky / made in a rush...
    # handles iterator when part of self.args
    def duplicate(self, copy_mode):
        copy1, copy2 = type(self)(), type(self)()
        for att in ('keywords', 'function_name', 'prefix', 'postfix',
                    'layout'):
            setattr(copy1, att, copy.copy(getattr(self, att)))
            setattr(copy2, att, copy.copy(getattr(self, att)))
        a1, a2 = [], [] 
        for arg in self.args:
            if not isinstance(arg, Iterator):
                a1.append(copy.copy(arg))
                a2.append(copy.copy(arg))
            else:
                c1, c2 = itertools.tee(arg, 2)
                a1.append(c1)
                a2.append(c2)
        copy1.args = tuple(a1)
        copy2.args = tuple(a2)
        return copy1, copy2


    def pretty_slice(self):
        if not self.islice:
            return "all results"
        if len(self.islice) == 1:
            end, = self.islice
            return f"iters → {end}"
        if len(self.islice) == 2:
            beg, end = self.islice
            return f"iters {beg} → {end}"
        if len(self.islice) == 3:
            beg, end, step = self.islice
            return f"iters {beg} → {end} / {step}"
        return f"ERROR: unknown islice {self.islice}"


    def layout_islice(self, width):
        inherited = super().layout_pprint(width)
        if self.islice is None:
            return inherited
        if inherited.startswith("<pre>"):
            patched = inherited.replace("<pre>", f"<pre> {self.pretty_slice()}\n")
        else:
            patched = "<pre>\n"
            patched += inherited + "\n"
            patched += self.pretty_slice() + "\n"
            patched += "</pre>"
        return patched